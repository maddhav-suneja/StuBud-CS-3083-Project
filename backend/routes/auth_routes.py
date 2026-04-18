from flask import Blueprint, g, jsonify, request

from services.auth import build_token, hash_password, sanitize_student, verify_password
from services.db import supabase
from services.responses import error_response
from services.student_service import fetch_student_or_none

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    nyu_email = (data.get("nyu_email") or "").strip().lower()
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    password = data.get("password") or ""

    if not nyu_email or not first_name or not last_name or not password:
        return error_response("nyu_email, first_name, last_name, and password are required")

    if "@nyu.edu" not in nyu_email:
        return error_response("Please use a valid NYU email address")

    existing_student = fetch_student_or_none(nyu_email)
    if existing_student:
        return error_response("An account with this email already exists", 409)

    student_payload = {
        "nyu_email": nyu_email,
        "first_name": first_name,
        "last_name": last_name,
        "hashed_password": hash_password(password),
        "account_role": "student",
    }

    try:
        created_student = supabase.table("student").insert(student_payload).execute()
    except Exception as exc:
        return error_response(f"Unable to create account: {exc}", 500)

    token = build_token(student_payload)

    return (
        jsonify(
            {
                "message": "Signup successful",
                "token": token,
                "student": sanitize_student(created_student.data[0]),
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    nyu_email = (data.get("nyu_email") or "").strip().lower()
    password = data.get("password") or ""

    if not nyu_email or not password:
        return error_response("nyu_email and password are required")

    student = fetch_student_or_none(nyu_email)
    if not student or not verify_password(password, student["hashed_password"]):
        return error_response("Invalid email or password", 401)

    token = build_token(student)

    return (
        jsonify(
            {
                "message": "Login successful",
                "token": token,
                "student": sanitize_student(student),
            }
        ),
        200,
    )
