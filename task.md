# Demo

Build a simple chatbot that answers student queries about their class schedule. 
The chatbot should be able to handle common questions from a student. This can include questions such as:

- Who is my advisor?
- Which courses am I taking in Fall 2024?
- Who are the instructors?
- When and where are the courses held?
- How many credits are the courses worth? 
- Credits of each course and total credits

etc...

### Database Schema

*Postgres/Supabase*

**WARNING**: *This schema is for context only and is not meant to be run.*

*Table order and constraints may not be valid for execution.*

`
id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
created_at timestamp with time zone NOT NULL DEFAULT now(),
student_id text DEFAULT ''::text,
student_name text DEFAULT ''::text,
advisor_name text DEFAULT ''::text,
course_code text DEFAULT ''::text,
course_name text DEFAULT ''::text,
term text DEFAULT ''::text,
instructor_name text DEFAULT ''::text,
days text DEFAULT ''::text,
time text DEFAULT ''::text,
building text DEFAULT ''::text,
room_number text DEFAULT ''::text,
credits text DEFAULT ''::text,
CONSTRAINT student_schedule_pkey PRIMARY KEY (id)
`




