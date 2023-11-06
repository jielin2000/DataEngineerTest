# DataEngineerTest

# Prerequisites
- Docker
- Docker Compose

# Getting Started
Follow the steps below to set up and run the project.

1. Clone the repository
2. Create volume **road_link_data** with
   ```
   docker volume create road_link_data
   ```
4. Create network **road_link_network**
   ```
   docker network create road_link_network
   ```
5. Build and run docker compose
   ```
   docker-compose up --build
   ```
Upon building the docker-compose, it will spin up 3 containers:
- **dataengineertest-db-1** : runs using postgres image where database is hosted 
- **dataengineertest-etl-1** : runs python file that loads sample_file.txt into database by creating table named road_links and inserting data into the table
- **jupyter_notebook** : access jupyter notebook file that connects to database and display visualizations of the data

To access the database through sql commands
```
# Run docker image and connect to it
docker exec -it dataengineertest-db-1 bash

# Enter the database
psql postgres://user1:12345@localhost:5432/roaddata

```
