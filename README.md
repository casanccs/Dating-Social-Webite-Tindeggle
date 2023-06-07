# How to run with Docker-Compose
1. In this directory, use command:  
    $ docker compose up --build


# How to run with Dockerfile
1. Build the Docker Image in this directory with:  
    $ docker build -t tindeggle .
2. Build the Docker Container with:  
    $ docker run -dp 8000:8000 tindeggle

# How to Install Locally
1. Create virtual environment
2. Install dependencies using:  
    $ pip install -r requirements.txt
3. Run server by using this command in parent directory:
    $ python manage.py runserver
# How to use
1. Create account with profile pictures and interests.
2. Look for people to "match" with.
3. Chat with the people you have matched with once you match with someone, or with random people.