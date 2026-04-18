-- Supabase SQL trigger to delete related student rows before deleting a student
-- Paste this into your Supabase SQL editor and run it.

CREATE OR REPLACE FUNCTION public.cascade_delete_student()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  -- remove any availability rows tied to the student
  DELETE FROM public.student_available_time
  WHERE nyu_email = OLD.nyu_email;

  -- remove any meeting join records tied to the student
  DELETE FROM public.meeting_request
  WHERE nyu_email = OLD.nyu_email;

  -- remove any feedback tied to the student
  DELETE FROM public.feedback
  WHERE nyu_email = OLD.nyu_email;

  RETURN OLD;
END;
$$;

DROP TRIGGER IF EXISTS delete_student_cleanup ON public.student;
CREATE TRIGGER delete_student_cleanup
BEFORE DELETE ON public.student
FOR EACH ROW
EXECUTE FUNCTION public.cascade_delete_student();

-- Standalone SQL command to retrieve the correct student count per meeting once.
SELECT m.meeting_id,
       COALESCE(cnt.correct_num_of_students, 0) AS correct_num_of_students
FROM public.meeting AS m
LEFT JOIN (
  SELECT meeting_id, COUNT(*) AS correct_num_of_students
  FROM public.meeting_request
  GROUP BY meeting_id
) AS cnt ON cnt.meeting_id = m.meeting_id;

-- Update the meeting table with the correct student counts.
UPDATE public.meeting
SET num_of_students = COALESCE(cnt.correct_num_of_students, 0)
FROM (
  SELECT meeting_id, COUNT(*) AS correct_num_of_students
  FROM public.meeting_request
  GROUP BY meeting_id
) AS cnt
WHERE public.meeting.meeting_id = cnt.meeting_id;

-- For meetings with no requests, set to 0
UPDATE public.meeting
SET num_of_students = 0
WHERE meeting_id NOT IN (SELECT DISTINCT meeting_id FROM public.meeting_request);

-- Create a trigger to increment meeting.num_of_students by 1 when a student joins.
CREATE OR REPLACE FUNCTION public.increment_meeting_student_count()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE public.meeting
  SET num_of_students = num_of_students + 1
  WHERE meeting_id = NEW.meeting_id;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS meeting_request_insert_increment_count ON public.meeting_request;
CREATE TRIGGER meeting_request_insert_increment_count
AFTER INSERT ON public.meeting_request
FOR EACH ROW
EXECUTE FUNCTION public.increment_meeting_student_count();
