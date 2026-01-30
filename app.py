from flask import Flask, request, jsonify, send_file
from generate import generate_voice
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ---------------- TTS API ----------------
@app.route("/api/tts", methods=["POST"])
def tts_api():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "text field is required"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "text cannot be empty"}), 400

    # optional params
    try:
        speed = float(data.get("speed", 1.0))
        pitch = float(data.get("pitch", 0))
    except ValueError:
        return jsonify({"error": "speed and pitch must be numbers"}), 400

    # emotion preset (optional)
    emotion = data.get("emotion")
    if emotion == "sad":
        speed, pitch = 0.8, -2
    elif emotion == "calm":
        speed, pitch = 0.9, -1
    elif emotion == "angry":
        speed, pitch = 1.2, 2
    elif emotion == "happy":
        speed, pitch = 1.15, 1

    audio_path = generate_voice(
        text=text,
        speed=speed,
        pitch=pitch
    )

    return jsonify({
        "status": "success",
        "voice": "male_1",
        "speed": speed,
        "pitch": pitch,
        "play_url": "/api/audio",
        "download_url": "/api/audio/download"
    })

# ---------------- PLAY AUDIO ----------------
@app.route("/api/audio", methods=["GET"])
def play_audio():
    path = os.path.join("output", "voice.wav")
    return send_file(path, mimetype="audio/wav", as_attachment=False)

# ---------------- DOWNLOAD AUDIO ----------------
@app.route("/api/audio/download", methods=["GET"])
def download_audio():
    path = os.path.join("output", "voice.wav")
    return send_file(path, mimetype="audio/wav", as_attachment=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
