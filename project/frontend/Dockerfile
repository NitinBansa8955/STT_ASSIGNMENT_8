# Using official Python 3.9 slim base image because slim version reduces image size while maintaining core functionality

FROM python:3.9-slim

WORKDIR /app

# Copying dependency specifications
COPY requirements.txt .

# Installing application dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Running application server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9567"]