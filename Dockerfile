# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the environment variable to indicate that Flask should run in production mode
ENV FLASK_ENV=production

# Run the Flask application
# flask --app src/app.py run
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]