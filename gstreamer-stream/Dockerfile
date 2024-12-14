# Use a base Ubuntu image
FROM ubuntu:20.04

# Set non-interactive mode to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the timezone (change if necessary)
ENV TZ=Etc/UTC

# Update and install the necessary packages, including GStreamer and plugins
RUN apt-get update && apt-get install -y \
    tzdata \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install WebSocket and signaling server libraries
RUN pip3 install websockets

# Set the working directory
WORKDIR /app

# Copy the GStreamer pipeline script into the container
COPY ./stream_video.sh /app/stream_video.sh

# Make the script executable
RUN chmod +x /app/stream_video.sh

# Set the default command to run the script
CMD ["./stream_video.sh"]
