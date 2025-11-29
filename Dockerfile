# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirement file
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port for Hugging Face Space
EXPOSE 7860

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]
