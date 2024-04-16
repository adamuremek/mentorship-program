FROM python:3.12.1-slim-bookworm

# Set the working directory inside the container
WORKDIR /mentorship_program

# Prevent python caching pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Disable buffering stdout & stderr
ENV PYTHONNUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip
# Copy requirements.txt into the working directory
COPY requirements.txt .
# Install project requirements
RUN pip install -r requirements.txt

# Install requirements to get specific Postgres version
RUN apt-get update && apt-get install -y wget gnupg2

# Add PostgreSQL repository
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client-15

# Install netcat to check if databse is running
RUN apt-get install -y netcat-openbsd

# Saml requirements
RUN apt-get install -y xmlsec1

# Create static directory
RUN mkdir /static

# Copy entrypoint script into the container 
COPY ./entrypoint.sh /entrypoint.sh

# Replace Windows newlines with Unix
RUN sed -i 's/\r$//g' /entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /entrypoint.sh

# Copy the project into the container
COPY . .

# Specify the script to run when starting the container
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /mentorship_program/mentorship_program_project

CMD ["gunicorn", "-w", "4", "mentorship_program_project.wsgi:application", "--bind", "0.0.0.0:8000"]