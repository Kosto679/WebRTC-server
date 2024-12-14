import asyncio
import json
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer
import yaml

# Parse configuration from the YAML file
def load_config(config_file):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

# Keep track of peer connections
pcs = set()

class LivestreamTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, player):
        super().__init__()
        self.player = player

    async def recv(self):
        """
        Receive and forward video frames from the livestream source.
        """
        frame = await self.player.video.recv()
        return frame

async def signaling_handler(websocket, path, livestream_url):
    """
    Handle WebSocket signaling messages.
    """
    pc = RTCPeerConnection()
    pcs.add(pc)

    # Attach a livestream track to the peer connection
    player = MediaPlayer(livestream_url)
    video_track = LivestreamTrack(player)
    pc.addTrack(video_track)

    async def send_answer():
        # Create and send SDP answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        await websocket.send(
            json.dumps({"type": pc.localDescription.type, "sdp": pc.localDescription.sdp})
        )

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "offer":
                # Process SDP offer
                offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
                await pc.setRemoteDescription(offer)

                # Create and send an SDP answer
                await send_answer()

            elif data["type"] == "candidate":
                # Add ICE candidate
                candidate = data.get("candidate")
                if candidate:
                    await pc.addIceCandidate(candidate)

    except websockets.ConnectionClosed:
        print("Connection closed")

    finally:
        # Cleanup
        await pc.close()
        pcs.discard(pc)

async def main():
    """
    Start the WebSocket signaling server.
    """
    # Load configuration
    config = load_config("config.yaml")
    host = config["server"]["host"]
    port = config["server"]["port"]
    livestream_url = config["livestream"]["url"]

    # Start the WebSocket server
    server = await websockets.serve(lambda ws, path: signaling_handler(ws, path, livestream_url), host, port)
    print(f"Signaling server started on ws://{host}:{port}")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped")
