# Use the official Python lightweight image
FROM python:3.13-slim

WORKDIR /app

COPY . /app

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install -r requirements.txt  

EXPOSE 8080

# Run the FastMCP server
CMD ["python", "server.py"]