FROM python:3.9
# useful to get log
ENV PYTHONUNBUFFERED 1
# Working directory inside container
WORKDIR /app
# copy local file to container directory
COPY requirements.txt /app/requirements.txt
# RUN is used to execute commands during the build process of the Docker image.
RUN pip install -r requirements.txt
# copy all the file "." under admin to container
COPY . /app
# CMD is used to specify the default command to run when a container based on the image is started.
# This specifies the host and port on which the development server will listen for incoming connections.
# CMD python manage.py runserver 0.0.0.0:8000