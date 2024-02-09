CREATE USER django_bot;
CREATE DATABASE mentorship_app;
GRANT ALL PRIVILEGES ON DATABASE mentorship_app TO django_bot;
ALTER USER django_bot WITH PASSWORD 'jango bot is best bot replace me later :)';
ALTER USER django_bot WITH SUPERUSER; --TODO: need to figure out a way to make this work without su
ALTER DATABASE mentorship_app OWNER TO django_bot;
