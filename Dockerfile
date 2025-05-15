FROM python:3.10-slim

WORKDIR /

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Copy your main handler script
COPY rp_handler.py /

# Start the container
CMD ["python3", "-u", "rp_handler.py"]
