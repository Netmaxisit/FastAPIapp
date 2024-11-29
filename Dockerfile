# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies needed to build some Python packages
RUN apt-get update && apt-get install -y gcc libpq-dev

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install FastAPI and Uvicorn dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app with Uvicorn on port 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
