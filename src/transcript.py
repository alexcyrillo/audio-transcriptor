import os
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

def compression(audio_path):
    # Carrega o áudio original
    audio = AudioSegment.from_file(audio_path)
    
    # Define o tamanho do pedaço (15 minutos em milissegundos)
    chunk_ms = 15 * 60 * 1000 
    chunk_paths = []
    
    # Divide e exporta pedaços temporários
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_name = f"temp_part_{i}.mp3"
        chunk.export(chunk_name, format="mp3", bitrate="64k")
        chunk_paths.append(chunk_name)
    
    return chunk_paths # Retorna lista de caminhos para load_audio usar

def clean_temp_files():
  for i in range(100):
    if os.path.exists(f"temp_part_{i}.mp3"):
      os.remove(f"temp_part_{i}.mp3")

def save_transcription(transcription, file_name):
  if not os.path.exists("transcriptions"):
    os.makedirs("transcriptions")

  file_path = f"transcriptions/{file_name}.txt"

  if os.path.exists(file_path):
    os.remove(file_path)
  f = open(file_path, "x", encoding="utf-8")
  f.write(transcription)
  f.close()

def load_audio(audio_path):
  audio = open(audio_path, "rb")
  return audio

def transcriptor(audio_file):
  client = OpenAI(
      api_key=os.getenv("OPENAI_API_KEY"),
  )

  transcript = client.audio.transcriptions.create(
    model="gpt-4o-transcribe",
    file=audio_file
  )

  audio_file.close()

  return transcript.text