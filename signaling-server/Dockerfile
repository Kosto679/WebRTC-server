# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY server.py config.yaml requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the signaling server
EXPOSE 8080

# Set the default command to run the server
CMD ["python", "server.py"]
