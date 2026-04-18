from flask import Blueprint, g, jsonify, request

from services.auth import hash_password, require_auth
from services.responses import error_response
from services.student_service import (
    fetch_profile_bundle,
    replace_available_times,
    replace_courses,
)

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/api/profile", methods=["GET"])
@require_auth
def get_profile():
    profile = fetch_profile_bundle(request.user_email)
    if not profile:
        return error_response("Student not found", 404)
    return jsonify(profile), 200


@profile_bp.route("/api/profile", methods=["PATCH"])
@require_auth
def update_profile():
    data = request.get_json(silent=True) or {}
    student_updates = {}

    if "first_name" in data:
        student_updates["first_name"] = (data.get("first_name") or "").strip()
    if "last_name" in data:
        student_updates["last_name"] = (data.get("last_name") or "").strip()
    if data.get("password"):
        student_updates["hashed_password"] = hash_password(data["password"])

    if "first_name" in student_updates and not student_updates["first_name"]:
        return error_response("first_name cannot be empty")
    if "last_name" in student_updates and not student_updates["last_name"]:
        return error_response("last_name cannot be empty")

    try:
        if student_updates:
            (
                g.db.table("student")
                .update(student_updates)
                .eq("nyu_email", request.user_email)
                .execute()
            )

        if "course_ids" in data:
            replace_courses(request.user_email, data.get("course_ids") or [])

        if "available_times" in data:
            replace_available_times(request.user_email, data.get("available_times") or [])
    except KeyError:
        return error_response("available_times entries must include week_day, start_time, and end_time")
    except Exception as exc:
        return error_response(f"Unable to update profile: {exc}", 500)

    updated_profile = fetch_profile_bundle(request.user_email)
    return jsonify(updated_profile), 200
