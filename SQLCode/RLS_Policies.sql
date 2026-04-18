-- =============================================================
-- RLS Policies for StuBud
-- Run in: Supabase Dashboard → SQL Editor → New Query
-- =============================================================
-- Identity check used in policies:
--   auth.jwt() ->> 'nyu_email'      identifies the current user
--   auth.jwt() ->> 'account_role'   distinguishes admin vs student
-- =============================================================


-- -------------------------------------------------------------
-- STEP 1: Enable RLS on all tables
-- -------------------------------------------------------------
ALTER TABLE student                ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_available_time ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_course         ENABLE ROW LEVEL SECURITY;
ALTER TABLE course                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE location               ENABLE ROW LEVEL SECURITY;
ALTER TABLE meeting                ENABLE ROW LEVEL SECURITY;
ALTER TABLE meeting_request        ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback               ENABLE ROW LEVEL SECURITY;
ALTER TABLE invitation             ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_material         ENABLE ROW LEVEL SECURITY;


-- -------------------------------------------------------------
-- STEP 2: Allow SELECT on every table (all authenticated users)
-- -------------------------------------------------------------
CREATE POLICY "read all"  ON student                FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON student_available_time FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON student_course         FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON course                 FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON location               FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON meeting                FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON meeting_request        FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON feedback               FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON invitation             FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "read all"  ON study_material         FOR SELECT TO anon, authenticated USING (true);


-- -------------------------------------------------------------
-- STEP 3: Student self-service write policies
-- -------------------------------------------------------------
CREATE POLICY "insert own record"
  ON feedback FOR INSERT TO authenticated
  WITH CHECK (nyu_email = auth.jwt() ->> 'nyu_email');

CREATE POLICY "insert own record"
  ON invitation FOR INSERT TO authenticated
  WITH CHECK (nyu_email = auth.jwt() ->> 'nyu_email');

CREATE POLICY "insert own record"
  ON meeting_request FOR INSERT TO authenticated
  WITH CHECK (nyu_email = auth.jwt() ->> 'nyu_email');

CREATE POLICY "insert own record"
  ON student_available_time FOR INSERT TO authenticated
  WITH CHECK (nyu_email = auth.jwt() ->> 'nyu_email');

CREATE POLICY "insert own record"
  ON study_material FOR INSERT TO authenticated
  WITH CHECK (true);

CREATE POLICY "update own row"
  ON student FOR UPDATE TO authenticated
  USING  (nyu_email = auth.jwt() ->> 'nyu_email')
  WITH CHECK (nyu_email = auth.jwt() ->> 'nyu_email');

CREATE POLICY "delete own rows"
  ON student_available_time FOR DELETE TO authenticated
  USING (nyu_email = auth.jwt() ->> 'nyu_email');

CREATE POLICY "insert own rows"
  ON student_course FOR INSERT TO authenticated
  WITH CHECK (nyu_email = auth.jwt() ->> 'nyu_email');

CREATE POLICY "delete own rows"
  ON student_course FOR DELETE TO authenticated
  USING (nyu_email = auth.jwt() ->> 'nyu_email');


-- -------------------------------------------------------------
-- STEP 4: Admin write policies
--         account_role = 'admin' in the JWT grants full control
-- -------------------------------------------------------------
CREATE POLICY "admin delete student"
  ON student FOR DELETE TO authenticated
  USING (auth.jwt() ->> 'account_role' = 'admin');

CREATE POLICY "admin delete meeting_request"
  ON meeting_request FOR DELETE TO authenticated
  USING (auth.jwt() ->> 'account_role' = 'admin');

CREATE POLICY "admin delete feedback"
  ON feedback FOR DELETE TO authenticated
  USING (auth.jwt() ->> 'account_role' = 'admin');

CREATE POLICY "admin delete meeting"
  ON meeting FOR DELETE TO authenticated
  USING (auth.jwt() ->> 'account_role' = 'admin');

CREATE POLICY "admin update meeting"
  ON meeting FOR UPDATE TO authenticated
  USING  (auth.jwt() ->> 'account_role' = 'admin')
  WITH CHECK (auth.jwt() ->> 'account_role' = 'admin');

CREATE POLICY "admin update course"
  ON course FOR UPDATE TO authenticated
  USING  (auth.jwt() ->> 'account_role' = 'admin')
  WITH CHECK (auth.jwt() ->> 'account_role' = 'admin');

CREATE POLICY "admin update location"
  ON location FOR UPDATE TO authenticated
  USING  (auth.jwt() ->> 'account_role' = 'admin')
  WITH CHECK (auth.jwt() ->> 'account_role' = 'admin');

--- exception invitation functionality

CREATE POLICY "delete own record"
 ON invitation FOR DELETE TO authenticated
 USING (nyu_email = auth.jwt() ->> 'nyu_email');
