FROM python:3.15.2-alpine

WORKDIR /app

# copy the requirements file in the workdir
COPY requirements.txt /app/

# install the Python requirements
RUN pip install -r requirements.txt

# copy the app files and directories
COPY booking/ /app/

# start movie.py when the container is started
CMD  ["python3", "booking.py"]
