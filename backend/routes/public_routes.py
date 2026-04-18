from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from config import SUPABASE_URL
from services.auth import require_auth
from services.db import supabase

public_bp = Blueprint("public", __name__)


@public_bp.route("/api/groups", methods=["GET"])
def get_groups():
    response = (
        supabase.table("meeting")
        .select(
            """
            meeting_id,
            start_time,
            end_time,
            meeting_note,
            num_of_students,
            course:course_id(course_id, course_name),
            location:location_id(location_id, building, room)
        """
        )
        .order("start_time")
        .execute()
    )

    groups = []
    for row in response.data:
        groups.append(
            {
                "meeting_id": row["meeting_id"],
                "start_time": row["start_time"],
                "end_time": row["end_time"],
                "meeting_note": row["meeting_note"],
                "num_of_students": row["num_of_students"],
                "course_id": row["course"]["course_id"] if row.get("course") else None,
                "course_name": row["course"]["course_name"] if row.get("course") else None,
                "location_id": row["location"]["location_id"] if row.get("location") else None,
                "building": row["location"]["building"] if row.get("location") else None,
                "room": row["location"]["room"] if row.get("location") else None,
            }
        )

    return jsonify(groups), 200


@public_bp.route("/api/study-materials", methods=["GET"])
def get_study_materials():
    meeting_id = request.args.get("meeting_id")
    if not meeting_id:
        return jsonify({"error": "meeting_id is required"}), 400

    response = (
        supabase.table("study_material")
        .select("study_material_id, meeting_id, file_name, file_path")
        .eq("meeting_id", meeting_id)
        .execute()
    )

    return jsonify(response.data or []), 200


@public_bp.route("/api/study-materials/upload", methods=["POST"])
@require_auth
def upload_study_material():
    meeting_id = request.form.get("meeting_id")
    file = request.files.get("file")

    if not meeting_id:
        return jsonify({"error": "meeting_id is required"}), 400
    if not file or not file.filename:
        return jsonify({"error": "file is required"}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"error": "Invalid file name"}), 400

    storage_path = f"{meeting_id}/{filename}"
    file_bytes = file.read()
    file_type = file.content_type or "application/octet-stream"

    upload_result = supabase.storage.from_("materials").upload(storage_path, file_bytes, {'content-type': file_type})
    if upload_result is None or (isinstance(upload_result, dict) and upload_result.get("error")):
        error = upload_result.get("error") if isinstance(upload_result, dict) else None
        message = error.get("message") if isinstance(error, dict) else str(error or "Upload failed")
        return jsonify({"error": message}), 500

    # Create public URL for download (assuming bucket is public)
    if SUPABASE_URL:
        file_url = f"{SUPABASE_URL}/storage/v1/object/public/materials/{storage_path}"
    else:
        file_url = storage_path  # Fallback

    material_record = {
        "meeting_id": int(meeting_id),
        "file_name": filename,
        "file_path": file_url,
    }

    response = supabase.table("study_material").insert(material_record).execute()


    inserted = response.data[0] if response.data else material_record
    return jsonify({"message": "Upload successful", "material": inserted}), 201


@public_bp.route("/api/group-students", methods=["GET"])
def get_group_students():
    meeting_id = request.args.get("meeting_id")
    if not meeting_id:
        return jsonify({"error": "meeting_id is required"}), 400

    meeting_request_response = (
        supabase.table("meeting_request")
        .select("nyu_email")
        .eq("meeting_id", meeting_id)
        .execute()
    )

    if not meeting_request_response.data:
        return jsonify([]), 200

    emails = [row["nyu_email"] for row in meeting_request_response.data if row.get("nyu_email")]
    if not emails:
        return jsonify([]), 200

    student_response = (
        supabase.table("student")
        .select("nyu_email, first_name, last_name")
        .in_("nyu_email", emails)
        .execute()
    )

    students = []
    for student in student_response.data or []:
        full_name = " ".join(
            part.strip() for part in [student.get("first_name", ""), student.get("last_name", "")] if part
        ).strip()
        students.append(
            {
                "nyu_email": student.get("nyu_email"),
                "name": full_name or student.get("nyu_email"),
            }
        )

    return jsonify(students), 200


@public_bp.route("/courses", methods=["GET"])
def get_courses():
    response = (
        supabase.table("course")
        .select("course_id, course_name")
        .order("course_name")
        .execute()
    )
    return jsonify(response.data), 200
