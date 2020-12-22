HOW TO RUN

1 - Build the Docker image:
    docker build -t my-python-app .

2 - Run the Docker image:
    docker run -p 8080:8080 -it --rm --name my-running-app my-python-app

3 - Open the next URLs for verifying that all works fine:
    http://localhost:8080/ping
    http://localhost:8080/dummy
