import os
import requests

# ==============================
# PUT YOUR NEW FREESOUND API KEY HERE
# ==============================
API_KEY = "KsLgyzi4i81Wuaps8Ycmaf8BlOFUgFddWBEQFZ29"

headers = {
    "Authorization": f"Token {API_KEY}"
}

SEARCH_URL = "https://freesound.org/apiv2/search/text/"

params = {
    "query": "bicycle bell",
    "filter": "duration:[0 TO 10]",
    "fields": "id,name,license,previews",
    "page_size": 50
}

mp3_folder = "bicycle_bell_mp3"
os.makedirs(mp3_folder, exist_ok=True)

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
        print("Error:", response.text)
        break

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        print("No more sounds found.")
        break

    for sound in data["results"]:

        preview_url = sound["previews"]["preview-hq-mp3"]

        filename = os.path.join(
            mp3_folder,
            f"bicycle_bell_{count:03d}.mp3"
        )

        print(f"Downloading {filename}")

        audio = requests.get(preview_url)

        with open(filename, "wb") as f:
            f.write(audio.content)

        count += 1

    if data["next"] is None:
        break

    page += 1

print("\n=========================")
print(f"Downloaded {count-1} MP3 files")
print("Saved to:", mp3_folder)
print("=========================")