-- Step 1
DROP DATABASE IF EXISTS mentorship_app;
CREATE DATABASE mentorship_app;
ALTER USER django_bot WITH PASSWORD 'temppass';


-- Step 2: Need to be logged into me

--connect to the database before the following commands
\c mentorship_app

GRANT ALL ON SCHEMA public TO django_bot;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO django_bot;
