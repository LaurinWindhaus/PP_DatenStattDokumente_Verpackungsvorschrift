# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install prerequisites for the Microsoft ODBC Driver
RUN apt-get update && apt-get install -y gnupg2 curl unixodbc-dev

# Download and install the Microsoft ODBC Driver for SQL Server (Ubuntu)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# COPY ./app /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=80"]