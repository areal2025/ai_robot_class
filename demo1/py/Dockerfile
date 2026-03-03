FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    libgl1 \
    libosmesa6 \
    net-tools \
    websockify \
    python3-pip \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir pybullet numpy websockets

# Create app directory
WORKDIR /app

# Copy files
COPY server.py /app/
COPY start.sh /app/

RUN chmod +x /app/start.sh

# Expose ports
EXPOSE 8765 6080

# Start
CMD ["/app/start.sh"]
