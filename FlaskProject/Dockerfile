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
