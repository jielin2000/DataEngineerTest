# Use the official Python image as the base image
FROM python:3.9

# Install PostgreSQL client and other required packages
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install psycopg2-binary pandas matplotlib jupyter

# Create a directory for your application code
WORKDIR /app

# Copy your application files to the container
COPY requirements.txt /app/
COPY dataprocessing.py /app/

# Install your Python dependencies
RUN pip install -r requirements.txt

# Expose the PostgreSQL default port (5432)
EXPOSE 5432

# Entry point for your script
CMD ["python", "dataprocessing.py"]

