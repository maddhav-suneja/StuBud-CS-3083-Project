from datetime import date

from flask import Blueprint, g, jsonify, request

from services.auth import require_auth
from services.db import supabase
from services.responses import error_response

invitation_bp = Blueprint("invitation", __name__)


@invitation_bp.route("/api/invitations", methods=["POST"])
@require_auth
def send_invitation():
    """
    Send an invitation to a student for a selected meeting/group.
    Requires bearer token authentication.
    """
    data = request.get_json(silent=True) or {}

    nyu_email = (data.get("nyu_email") or "").strip().lower()
    meeting_id = data.get("meeting_id")

    if not nyu_email or not meeting_id:
        return error_response("nyu_email and meeting_id are required", 400)

    if not nyu_email.endswith("@nyu.edu"):
        return error_response("Please enter a valid NYU email address", 400)

    try:
        # Check invited student exists
        student_response = (
            supabase.table("student")
            .select("nyu_email")
            .eq("nyu_email", nyu_email)
            .limit(1)
            .execute()
        )

        if not student_response.data:
            return error_response("Student with this NYU email does not exist", 404)

        # Check meeting exists
        meeting_response = (
            supabase.table("meeting")
            .select("meeting_id")
            .eq("meeting_id", meeting_id)
            .limit(1)
            .execute()
        )

        if not meeting_response.data:
            return error_response("Selected group does not exist", 404)

        # Prevent duplicate invitation
        existing_invitation = (
            supabase.table("invitation")
            .select("invitation_id")
            .eq("nyu_email", nyu_email)
            .eq("meeting_id", meeting_id)
            .limit(1)
            .execute()
        )

        if existing_invitation.data:
            return error_response("This student has already been invited to the selected group", 409)

        # Insert invitation
        insert_response = (
            supabase.table("invitation")
            .insert({
                "nyu_email": nyu_email,
                "meeting_id": meeting_id,
                "sent_date": date.today().isoformat()
            })
            .execute()
        )

        return jsonify({
            "message": "Invitation sent successfully",
            "invitation": insert_response.data[0] if insert_response.data else None
        }), 201

    except Exception as exc:
        return error_response(f"Failed to send invitation: {exc}", 500)


@invitation_bp.route("/api/my-invitations", methods=["GET"])
@require_auth
def get_my_invitations():
    try:
        response = (
            supabase.table("invitation")
            .select(
                "invitation_id, sent_date, meeting_id, "
                "meeting:meeting_id(meeting_id, start_time, end_time, meeting_note, num_of_students, "
                "course:course_id(course_name), location:location_id(building, room))"
            )
            .eq("nyu_email", request.user_email)
            .execute()
        )

        invitations = []
        for row in response.data or []:
            meeting = row.get("meeting") or {}
            course = meeting.get("course") or {}
            location = meeting.get("location") or {}
            invitations.append({
                "invitation_id": row.get("invitation_id"),
                "sent_date": row.get("sent_date"),
                "meeting_id": row.get("meeting_id"),
                "start_time": meeting.get("start_time"),
                "end_time": meeting.get("end_time"),
                "meeting_note": meeting.get("meeting_note"),
                "num_of_students": meeting.get("num_of_students"),
                "course_name": course.get("course_name"),
                "building": location.get("building"),
                "room": location.get("room"),
            })

        return jsonify(invitations), 200
    except Exception as exc:
        return error_response(f"Failed to fetch invitations: {exc}", 500)


@invitation_bp.route("/api/invitations/respond", methods=["POST"])
@require_auth
def respond_to_invitation():
    data = request.get_json(silent=True) or {}
    meeting_id = data.get("meeting_id")
    action = data.get("action")

    if not meeting_id or action not in ("accept", "decline"):
        return error_response("meeting_id and action (accept or decline) are required", 400)

    try:
        invitation = (
            supabase.table("invitation")
            .select("invitation_id")
            .eq("nyu_email", request.user_email)
            .eq("meeting_id", meeting_id)
            .limit(1)
            .execute()
        )

        if not invitation.data:
            return error_response("Invitation not found", 404)

        if action == "accept":
            existing = (
                g.db.table("meeting_request")
                .select("meeting_id")
                .eq("nyu_email", request.user_email)
                .eq("meeting_id", meeting_id)
                .execute()
            )
            if not existing.data:
                g.db.table("meeting_request").insert({
                    "nyu_email": request.user_email,
                    "meeting_id": meeting_id,
                }).execute()

        g.db.table("invitation").delete().eq("nyu_email", request.user_email).eq("meeting_id", meeting_id).execute()

        verb = "accepted" if action == "accept" else "declined"
        return jsonify({"message": f"Invitation {verb} successfully"}), 200
    except Exception as exc:
        return error_response(f"Failed to respond to invitation: {exc}", 500)