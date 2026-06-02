# Use official Python runtime as base image
FROM ubuntu:22.04

RUN apt-get update -qy
RUN apt-get install -y python3 python3-pip

# Set working directory in container
WORKDIR /app

# Install dependencies
RUN pip3 install Flask flask-cors requests

# Copy the application files
COPY ./src /app/

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
