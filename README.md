## Prerequisites

Before you begin, make sure you have Docker installed on your machine. If you don't have Docker installed, you can follow the instructions at [Get Docker](https://docs.docker.com/get-docker/).

For those unfamiliar with Docker, you can find more information in the [Docker Documentation](https://docs.docker.com/manuals/). 

## Getting Started

1. **Clone the repository:**
    
    ```
    git clone https://github.com/adamuremek/mentorship-program.git
    cd mentorship-program
    ```

2. **Run Docker Compose:**
    
    The first build may take a while as it downloads project dependencies.

    ```
    docker compose up --build
    ```

    To run in the background, use:

    ```
    docker compose up -d --build
    ```


3. **Access the website:**
    
    Open your browser and navigate to [http://localhost:8000/](http://localhost:8000/)
    
4. **Access the database:**
	
	By default, the database can be accessed at:
	- Host: `localhost`
	- Port: `7654`
	- Database: `development`
	- User: `user`
	- Password: `password`

	These values can be changed in `/docker/.env`
	
	**Note:** By default, the database is flushed on every run to provide a clean slate for development. This means all data in the database will be deleted when the containers start. If you wish to retain data between runs, you can comment out the corresponding line in the `/docker/entrypoint.sh` script.



## Other Useful Commands

- To stop the containers, run:

	```
	docker compose down
	```

- To view output from the containers:

	```
	docker compose logs
	```
- To execute a command in a container
	
	```
	docker compose exec SERVICE COMMAND
	```
	For example:
	```
	docker compose exec web python manage.py makemigrations
	```
	
