#!/bin/bash

# Example of using videotestsrc for a test video stream.
# Replace this with a webcam source like v4l2src on Linux.

SIGNALING_SERVER="ws://your-server-address:8080/ws" # Replace with your signaling server URL
STUN_SERVER="stun://stun.l.google.com:19302" # Example STUN server
SIGNALING_NAME="gstream-client"

# GStreamer pipeline to stream video to the WebRTC signaling server
gst-launch-1.0 -v \
    videotestsrc ! videoconvert ! video/x-raw,width=640,height=480,framerate=30/1 ! queue ! x264enc bitrate=5000 speed-preset=ultrafast ! h264parse ! rtph264pay ! queue ! \
    webrtcbin bundle-policy=max-bundle \
        stun-server=$STUN_SERVER \
        signaling-server=$SIGNALING_SERVER \
        signaling-name=$SIGNALING_NAME
