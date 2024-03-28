# Database Dockerfile

# Use an official PostgreSQL as a parent image
FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase

# Expose the PostgreSQL port
EXPOSE 5432

# Add initialization scripts
ADD init.sql /docker-entrypoint-initdb.d/

# Start PostgreSQL service
CMD ["postgres"]
