import os
from TTS.api import TTS
from pydub import AudioSegment

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RAW_WAV = os.path.join(OUTPUT_DIR, "raw.wav")
FINAL_WAV = os.path.join(OUTPUT_DIR, "voice.wav")

# ---------------- MALE VOICE MODEL ----------------
tts = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    progress_bar=False
)

# ---------------- PITCH SHIFT ----------------
def change_pitch(input_wav, output_wav, semitones):
    audio = AudioSegment.from_wav(input_wav)
    new_rate = int(audio.frame_rate * (2.0 ** (semitones / 12.0)))
    pitched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate})
    pitched = pitched.set_frame_rate(22050)
    pitched.export(output_wav, format="wav")

# ---------------- MAIN GENERATOR ----------------
def generate_voice(text, speed=1.0, pitch=0):

    # safety limits
    speed = max(0.6, min(speed, 1.3))
    pitch = max(-5, min(pitch, 5))

    # Step 1: base voice
    tts.tts_to_file(
        text=text,
        file_path=RAW_WAV,
        speed=speed
    )

    # Step 2: pitch control
    if pitch != 0:
        change_pitch(RAW_WAV, FINAL_WAV, pitch)
    else:
        os.replace(RAW_WAV, FINAL_WAV)

    return FINAL_WAV
