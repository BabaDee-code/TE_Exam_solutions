# Use the official image as a parent image
FROM mcr.microsoft.com/devcontainers/python:3.11

# Set the working directory
WORKDIR /workspace

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .