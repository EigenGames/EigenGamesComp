# Use official Python image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy all files from the framework directory into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Autonome will use
EXPOSE 3000

# Start the AI server
CMD ["python", "app.py"]
