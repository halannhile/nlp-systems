# Use the official Python image from the Docker Hub as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        graphviz \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download and install the spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the app code into the container at /app
COPY . .

# Expose the port that Streamlit listens on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app_streamlit.py"]
