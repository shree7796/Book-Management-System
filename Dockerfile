# Use a slim Python image
FROM python:3.11-slim

# Install utilities needed for the start.sh script (like 'nc' for netcat)
# Note: Installing full 'bash' is common in dev environments for easier debugging.
RUN apt-get update && apt-get install -y --no-install-recommends bash netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Set environment variable for unbuffered output
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code and the startup script
COPY ./app /app/app
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Command to run the application using the startup script
CMD ["/start.sh"]