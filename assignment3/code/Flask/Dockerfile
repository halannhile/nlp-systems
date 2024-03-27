# Use the official Python image as a base image
FROM python:3.8-slim

# Install spaCy and download the English language model
RUN pip install spacy && \
    python -m spacy download en_core_web_sm


# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code into the container
COPY . .

# Expose the port on which the Flask application will run
EXPOSE 5000

# Set the command to run the Flask application when the container starts
CMD ["python", "app_flask.py"]
