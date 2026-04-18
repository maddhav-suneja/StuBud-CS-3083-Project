from flask import Blueprint, g, jsonify, request

from services.auth import require_auth
from services.responses import error_response
from services.student_service import fetch_profile_bundle

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/api/dashboard", methods=["GET"])
@require_auth
def get_dashboard():
    profile = fetch_profile_bundle(request.user_email)
    if not profile:
        return error_response("Student not found", 404)

    meeting_request_response = (
        g.db.table("meeting_request")
        .select("meeting_id")
        .eq("nyu_email", request.user_email)
        .execute()
    )

    joined_groups = []

    for row in meeting_request_response.data:
        meeting_id = row.get("meeting_id")
        if not meeting_id:
            continue

        meeting_response = (
            g.db.table("meeting")
            .select(
                """
                meeting_id,
                start_time,
                end_time,
                meeting_note,
                num_of_students,
                course_id,
                location_id
            """
            )
            .eq("meeting_id", meeting_id)
            .limit(1)
            .execute()
        )

        if not meeting_response.data:
            continue

        meeting = meeting_response.data[0]

        course = {}
        if meeting.get("course_id"):
            course_response = (
                g.db.table("course")
                .select("course_id, course_name")
                .eq("course_id", meeting["course_id"])
                .limit(1)
                .execute()
            )
            if course_response.data:
                course = course_response.data[0]

        location = {}
        if meeting.get("location_id"):
            location_response = (
                g.db.table("location")
                .select("location_id, building, room, capacity")
                .eq("location_id", meeting["location_id"])
                .limit(1)
                .execute()
            )
            if location_response.data:
                location = location_response.data[0]

        joined_groups.append(
            {
                "meeting_id": meeting.get("meeting_id"),
                "start_time": meeting.get("start_time"),
                "end_time": meeting.get("end_time"),
                "meeting_note": meeting.get("meeting_note"),
                "num_of_students": meeting.get("num_of_students"),
                "course_id": course.get("course_id"),
                "course_name": course.get("course_name"),
                "location_id": location.get("location_id"),
                "building": location.get("building"),
                "room": location.get("room"),
            }
        )

    upcoming_groups = sorted(
        joined_groups,
        key=lambda group: group["start_time"] or "",
    )

    dashboard = {
        "student": profile["student"],
        "courses": profile["courses"],
        "available_times": profile["available_times"],
        "joined_groups": upcoming_groups,
        "stats": {
            "course_count": len(profile["courses"]),
            "joined_group_count": len(upcoming_groups),
        },
    }

    return jsonify(dashboard), 200
