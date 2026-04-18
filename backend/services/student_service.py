from flask import g, has_request_context

from services.db import supabase


def _get_db():
    if has_request_context() and hasattr(g, "db"):
        return g.db
    return supabase


def fetch_student_or_none(nyu_email):
    response = (
        _get_db()
        .table("student")
        .select("nyu_email, first_name, last_name, hashed_password, account_role")
        .eq("nyu_email", nyu_email)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def fetch_profile_bundle(nyu_email):
    db = _get_db()

    student_response = (
        db.table("student")
        .select("nyu_email, first_name, last_name, account_role")
        .eq("nyu_email", nyu_email)
        .limit(1)
        .execute()
    )

    if not student_response.data:
        return None

    course_response = (
        db.table("student_course")
        .select("course_id, course:course_id(course_id, course_name)")
        .eq("nyu_email", nyu_email)
        .order("course_id")
        .execute()
    )

    available_time_response = (
        db.table("student_available_time")
        .select("time_id, week_day, start_time, end_time")
        .eq("nyu_email", nyu_email)
        .order("week_day")
        .order("start_time")
        .execute()
    )

    return {
        "student": student_response.data[0],
        "courses": [
            {
                "course_id": row["course_id"],
                "course_name": row["course"]["course_name"] if row.get("course") else None,
            }
            for row in course_response.data
        ],
        "available_times": available_time_response.data,
    }


def get_next_time_id():
    response = (
        _get_db()
        .table("student_available_time")
        .select("time_id")
        .order("time_id", desc=True)
        .limit(1)
        .execute()
    )
    if not response.data:
        return 1
    return response.data[0]["time_id"] + 1


def replace_courses(nyu_email, course_ids):
    db = _get_db()
    db.table("student_course").delete().eq("nyu_email", nyu_email).execute()

    unique_course_ids = []
    for course_id in course_ids:
        if course_id not in unique_course_ids:
            unique_course_ids.append(course_id)

    if unique_course_ids:
        payload = [
            {"nyu_email": nyu_email, "course_id": int(course_id)}
            for course_id in unique_course_ids
        ]
        db.table("student_course").insert(payload).execute()


def replace_available_times(nyu_email, available_times):
    db = _get_db()
    db.table("student_available_time").delete().eq("nyu_email", nyu_email).execute()

    if not available_times:
        return

    payload = []
    for idx, time_slot in enumerate(available_times):
        payload.append(
            {
                "time_id": get_next_time_id() + idx,
                "nyu_email": nyu_email,
                "week_day": time_slot["week_day"],
                "start_time": time_slot["start_time"],
                "end_time": time_slot["end_time"],
            }
        )

    if payload:
        db.table("student_available_time").insert(payload).execute()
