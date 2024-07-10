# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory
WORKDIR /app

ENV DB_USER="pulmoscanai"
ENV DB_PASSWORD="pulmo"
ENV DB_HOST="34.155.61.153"
ENV DB_NAME="PulmoScanAI"
ENV GCS_BUCKET_NAME="pulmobucket_models"

# Copy the requirements file into the container
COPY ./app/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./pulmoscanai.json /app/service_account_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service_account_key.json"


# Copy the current directory contents into the container at /app
COPY . /app

# Install supervisor to manage both services
RUN apt-get update && apt-get install -y supervisor

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the necessary ports
EXPOSE 8000 8501

# Command to run when the container starts
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]