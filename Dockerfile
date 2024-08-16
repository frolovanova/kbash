# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /opt

# Copy the Python script into the container
COPY startup.py /opt/startup.py

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "/opt/startup.py"]

