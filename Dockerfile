# # Use Python 3.9.10 slim version as a starting point
# FROM python:3.9.10-slim-buster

# # Set our working directory inside the container to /app
# WORKDIR /app

# # Copy the list of required Python packages from our project to the container
# COPY requirements.txt ./

# # Install all the Python packages listed in requirements.txt
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copy all of our project's files into the /app directory in the container
# COPY . .

# # Expose port 3000 to allow external connections
# EXPOSE 3000

# # Define the default command to run when the container starts
# # Start our Flask application and make it accessible from all network interfaces on port 3000
# CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]



# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY app.py .

# Copy any additional files, such as .env
# COPY .env .

# Expose the port that your app runs on
EXPOSE 5000

# Set the command to run your application
