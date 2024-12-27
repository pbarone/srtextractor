from faster_whisper import WhisperModel
from audio_extract import extract_audio
import os

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")


videofile =  r"\\10.0.0.145\media\TV\90 Day\90 Day Fiance - Love in Paradise\S02\90 Day Fiance - Love in Paradise - S02E05 - Translating the Truth WEBRip-720p.mkv"

audiofile = "./audio.mp3"

#extract_audio(input_path=videofile, output_path=audiofile)

segments, info = model.transcribe(videofile, beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

#delete audiofile
#os.remove(audiofile)
