-- =============================================================
-- GRANT / REVOKE Privilege Statements for StuBud
-- Database: Supabase (PostgreSQL)
--
-- Roles used:
--   anon        – unauthenticated visitors (no login)
--   authenticated – any logged-in student or admin
--   service_role  – backend server (bypasses RLS; developer-only)
--
-- These statements define the *maximum* privileges each role may
-- exercise.  Row Level Security (RLS) policies in RLS_Policies.sql
-- then further restrict which specific rows are visible or writable.
-- =============================================================


-- -------------------------------------------------------------
-- STEP 1: Revoke defaults so we start from a clean slate
-- -------------------------------------------------------------
REVOKE ALL ON student                FROM anon, authenticated;
REVOKE ALL ON student_available_time FROM anon, authenticated;
REVOKE ALL ON student_course         FROM anon, authenticated;
REVOKE ALL ON course                 FROM anon, authenticated;
REVOKE ALL ON location               FROM anon, authenticated;
REVOKE ALL ON meeting                FROM anon, authenticated;
REVOKE ALL ON meeting_request        FROM anon, authenticated;
REVOKE ALL ON feedback               FROM anon, authenticated;
REVOKE ALL ON invitation             FROM anon, authenticated;
REVOKE ALL ON study_material         FROM anon, authenticated;


-- -------------------------------------------------------------
-- STEP 2: Read-only access for unauthenticated visitors (anon)
--         RLS "read all" policies allow public browsing of
--         non-sensitive tables such as courses and locations.
-- -------------------------------------------------------------
GRANT SELECT ON course        TO anon;
GRANT SELECT ON location      TO anon;
GRANT SELECT ON meeting       TO anon;


-- -------------------------------------------------------------
-- STEP 3: Authenticated student privileges
--         Every logged-in user can read all tables.
--         Write access is limited to tables students own.
-- -------------------------------------------------------------

-- SELECT on every table
GRANT SELECT ON student                TO authenticated;
GRANT SELECT ON student_available_time TO authenticated;
GRANT SELECT ON student_course         TO authenticated;
GRANT SELECT ON course                 TO authenticated;
GRANT SELECT ON location               TO authenticated;
GRANT SELECT ON meeting                TO authenticated;
GRANT SELECT ON meeting_request        TO authenticated;
GRANT SELECT ON feedback               TO authenticated;
GRANT SELECT ON invitation             TO authenticated;
GRANT SELECT ON study_material         TO authenticated;

-- Students manage their own profile row
GRANT UPDATE ON student TO authenticated;

-- Students manage their own availability slots
GRANT INSERT, DELETE ON student_available_time TO authenticated;

-- Students enroll in / drop courses
GRANT INSERT, DELETE ON student_course TO authenticated;

-- Students submit feedback for meetings they attended
GRANT INSERT ON feedback TO authenticated;

-- Students send and withdraw invitations
GRANT INSERT, DELETE ON invitation TO authenticated;

-- Students request meetings
GRANT INSERT ON meeting_request TO authenticated;

-- Students upload study materials
GRANT INSERT ON study_material TO authenticated;


-- -------------------------------------------------------------
-- STEP 4: Revoke write access that students must NOT have
--         Admins perform these operations via the service_role
--         client, which bypasses RLS entirely.
-- -------------------------------------------------------------
REVOKE INSERT, UPDATE, DELETE ON course   FROM authenticated;
REVOKE INSERT, UPDATE, DELETE ON location FROM authenticated;
REVOKE INSERT, UPDATE, DELETE ON meeting  FROM authenticated;

-- Students cannot delete other students' records
REVOKE DELETE ON student            FROM authenticated;
REVOKE DELETE ON meeting_request    FROM authenticated;
REVOKE DELETE ON feedback           FROM authenticated;
REVOKE DELETE ON study_material     FROM authenticated;


-- -------------------------------------------------------------
-- STEP 5: service_role gets full access (developer / admin ops)
--         service_role is used exclusively by the Flask backend
--         for auth operations (signup, login) that occur before
--         a user token exists, and for admin management actions.
-- -------------------------------------------------------------
GRANT ALL ON student                TO service_role;
GRANT ALL ON student_available_time TO service_role;
GRANT ALL ON student_course         TO service_role;
GRANT ALL ON course                 TO service_role;
GRANT ALL ON location               TO service_role;
GRANT ALL ON meeting                TO service_role;
GRANT ALL ON meeting_request        TO service_role;
GRANT ALL ON feedback               TO service_role;
GRANT ALL ON invitation             TO service_role;
GRANT ALL ON study_material         TO service_role;
GRANT USAGE, SELECT ON SEQUENCE study_material_study_material_id_seq TO service_role;
