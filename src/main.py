from transcript import clean_temp_files, compression, load_audio, save_transcription, transcriptor
from pathlib import Path

def main():
  audio_path = input("Arraste o arquivo de audio\n")

  transcription = ""
  audio_path_clean = audio_path.strip("'").strip('"')
  file_name = Path(audio_path_clean).stem

  audios_paths = compression(audio_path_clean)

  for i, el in enumerate(audios_paths):
    print(f"Realizando transcricao ({i+1}/{len(audios_paths)})")
    audio_name = Path(el)
    audio = load_audio(audio_name)
    transcription += transcriptor(audio) + " "

  save_transcription(transcription, file_name)

  clean_temp_files()

if __name__ == "__main__":
  main()
