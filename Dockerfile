FROM python:3.10-slim

WORKDIR /

# Create a 10GB dummy file before copying your script
RUN dd if=/dev/zero of=/large_dummy_file bs=1M count=10240

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Copy your main handler script
COPY rp_handler.py /

# Start the container
CMD ["python3", "-u", "rp_handler.py"]
