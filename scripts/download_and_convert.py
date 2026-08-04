import os
import requests
from pydub import AudioSegment

# ==============================
# PUT YOUR FREESOUND API KEY HERE
# ==============================
API_KEY = "KsLgyzi4i81Wuaps8Ycmaf8BlOFUgFddWBEQFZ29"

headers = {
    "Authorization": f"Token {API_KEY}"
}

SEARCH_URL = "https://freesound.org/apiv2/search/text/"

params = {
    "query": "bicycle bell",
    "filter": "duration:[0 TO 10]",
    "fields": "id,name,previews",
    "page_size": 50
}

mp3_folder = "bicycle_bell_mp3"
wav_folder = "bicycle_bell_wav"

os.makedirs(mp3_folder, exist_ok=True)
os.makedirs(wav_folder, exist_ok=True)

page = 1
count = 1

while True:

    params["page"] = page

    response = requests.get(
        SEARCH_URL,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print(response.text)
        break

    data = response.json()

    for sound in data["results"]:

        preview = sound["previews"]["preview-hq-mp3"]

        mp3_file = os.path.join(
            mp3_folder,
            f"bicycle_bell_{count:03d}.mp3"
        )

        wav_file = os.path.join(
            wav_folder,
            f"bicycle_bell_{count:03d}.wav"
        )

        print(f"Downloading {count}")

        audio = requests.get(preview)

        with open(mp3_file, "wb") as f:
            f.write(audio.content)

        print("Converting to WAV...")

        sound_mp3 = AudioSegment.from_mp3(mp3_file)

        sound_mp3 = sound_mp3.set_channels(1)
        sound_mp3 = sound_mp3.set_frame_rate(16000)

        sound_mp3.export(
            wav_file,
            format="wav"
        )

        count += 1

    if data["next"] is None:
        break

    page += 1

print()
print("=========================")
print(f"Downloaded {count-1} sounds")
print("MP3 folder :", mp3_folder)
print("WAV folder :", wav_folder)
print("=========================")