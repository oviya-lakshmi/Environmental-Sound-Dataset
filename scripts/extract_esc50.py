import os
import shutil
import pandas as pd

# ==========================================================
# CHANGE THESE PATHS
# ==========================================================

ESC50_PATH = r"C:\esc_datasets\ESC-50"

CSV_FILE = os.path.join(ESC50_PATH, "meta", "esc50.csv")
AUDIO_FOLDER = os.path.join(ESC50_PATH, "audio")

# Your GitHub repository
OUTPUT_FOLDER = r"C:\Environmental-Sound-Dataset\dataset\audio"

# ==========================================================


CATEGORY_MAP = {

    "crying_baby": "baby_cry",

    "dog": "dog_bark",

    "cat": "cat_meow",

    "glass_breaking": "Glass_Breaking",

    "door_wood_knock": "Door_Knock",

    "thunderstorm": "Thunder",

    "clock_alarm": "clock_alarm",

    "car_horn": "car_horn",

    "airplane": "Airplane"
}


df = pd.read_csv(CSV_FILE)

print(f"Total files in ESC-50 : {len(df)}")
print("-" * 40)

for esc_category, folder in CATEGORY_MAP.items():

    subset = df[df["category"] == esc_category]

    destination = os.path.join(OUTPUT_FOLDER, folder)

    os.makedirs(destination, exist_ok=True)

    count = 1

    for _, row in subset.iterrows():

        source = os.path.join(AUDIO_FOLDER, row["filename"])

        new_name = f"esc50_{folder.lower()}_{count:03d}.wav"

        target = os.path.join(destination, new_name)

        shutil.copy2(source, target)

        count += 1

    print(f"{folder:20s} -> {count-1} files copied")

print("\nExtraction Completed Successfully!")