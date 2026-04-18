from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_cors import CORS
import sys
import os

# Add backend directory to path for imports
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.profile_routes import profile_bp
from routes.public_routes import public_bp
from routes.groups_and_feedbacks import groups_feedback_bp
from routes.invitation_routes import invitation_bp
from services.db import supabase

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/materials/<path:filename>')
def serve_material(filename):
    """Serve study materials from static/materials."""
    return send_from_directory(os.path.join(app.static_folder, 'materials'), filename)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(public_bp)
app.register_blueprint(groups_feedback_bp)
app.register_blueprint(invitation_bp)


# Template rendering routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    """Signup page"""
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard_page():
    """Dashboard page - requires authentication"""
    return render_template('dashboard.html')


@app.route('/profile')
def profile_page():
    """Profile page"""
    return render_template('profile.html')


@app.route('/groups')
def groups_page():
    """Groups list page"""
    return render_template('groups.html')


@app.route('/create-group')
def create_group_page():
    """Create group page"""
    return render_template('create-group.html')


@app.route('/group-details')
def group_details_page():
    """Group details page"""
    return render_template('group-details.html')


@app.route('/group-feedback')
def group_feedback_page():
    """Group feedback page"""
    return render_template('group-feedback.html')


@app.route('/join-group')
def join_group_page():
    """Join group page"""
    return render_template('join-group.html')


@app.route('/students')
def students_page():
    """Students list page"""
    return render_template('students.html')


@app.route('/student-info')
def student_info_page():
    """Student info page"""
    return render_template('student-info.html')


@app.route('/logout')
def logout():
    """Logout - clears token"""
    return redirect('/')


@app.route('/admin-login')
def admin_login_page():
    """Admin login page"""
    return render_template('admin-login.html')


@app.route('/admin-dashboard')
def admin_dashboard_page():
    """Admin dashboard page"""
    return render_template('admin-dashboard.html')


@app.route('/admin-groups')
def admin_groups_page():
    """Admin groups page"""
    return render_template('admin-groups.html')


@app.route('/admin-group-info')
def admin_group_info_page():
    """Admin group info page"""
    return render_template('admin-group-info.html')


@app.route('/admin-students')
def admin_students_page():
    """Admin students page"""
    return render_template('admin-students.html')


@app.route('/admin-student-info')
def admin_student_info_page():
    """Admin student info page"""
    return render_template('admin-student-info.html')


@app.route('/join-success')
def join_success_page():
    """Join success page"""
    return render_template('join-success.html')


@app.route('/study-materials')
def study_materials_page():
    """Study materials page"""
    return render_template('study-materials.html')


@app.route('/group-invitation')
def group_invitation_page():
    """Group invitation page"""
    return render_template('group_invitation.html')


@app.route('/my-invitations')
def my_invitations_page():
    """My invitations page"""
    return render_template('my_invitations.html')


# API endpoint for getting students (used by students.html)
@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students from database"""
    try:
        response = supabase.table('student').select('*').execute()
        students = [
            {k: v for k, v in student.items() if k != 'hashed_password'}
            for student in (response.data or [])
        ]
        return students, 200
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/api/student', methods=['GET'])
def get_student_by_email():
    """Get a single student by NYU email"""
    nyu_email = request.args.get('nyu_email')
    if not nyu_email:
        return {'error': 'nyu_email is required'}, 400

    try:
        response = supabase.table('student').select('*').eq('nyu_email', nyu_email).limit(1).execute()
        if not response.data:
            return {'error': 'Student not found'}, 404
        student = {k: v for k, v in response.data[0].items() if k != 'hashed_password'}
        return student, 200
    except Exception as e:
        return {'error': str(e)}, 500


# API endpoint for getting students (non-API route for compatibility)
@app.route('/students-api', methods=['GET'])
def api_students():
    """Alternative API endpoint for getting students"""
    try:
        response = supabase.table('student').select('*').execute()
        students = [
            {k: v for k, v in student.items() if k != 'hashed_password'}
            for student in (response.data or [])
        ]
        return students, 200
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
