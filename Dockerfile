FROM python:3.10-slim

WORKDIR /
RUN pip install --no-cache-dir runpod==1.7.6
COPY rp_handler.py /

# Start the container
CMD ["python3", "-u", "rp_handler.py"]
