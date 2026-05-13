# Use a lightweight Python image for the backend
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that Flask uses
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Start the Flask app
CMD ["python", "app.py"]
