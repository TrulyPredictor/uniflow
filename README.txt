Navigate to the directory containing the Dockerfile in the terminal.

Run the following command to build the Docker image:
docker build -t uniflow-app .
This will create a Docker image named uniflow-app.

Run Docker Container:

Run the Docker container with the following command:
docker run -it uniflow-app
The -it option allows you to interact with the container.

Docker will start your Uniflow application and execute the entry command specified in the CMD.