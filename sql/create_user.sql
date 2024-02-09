CREATE USER django_bot;
CREATE DATABASE mentorship_app;
GRANT ALL PRIVILEGES ON DATABASE mentorship_app TO django_bot;
ALTER USER django_bot WITH PASSWORD 'jango bot is best bot replace me later :)';
ALTER DATABASE mentorship_app OWNER TO django_bot;
