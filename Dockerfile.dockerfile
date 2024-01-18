# Use an official Python runtime as a parent image
FROM python:3.8

LABEL maintainer="850053197@qq.com"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY  uniflow /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
