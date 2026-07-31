import kagglehub
import pandas as pd
import shutil
from pathlib import Path

# ============================================================
# 1. Download UrbanSound8K
# ============================================================

print("Downloading UrbanSound8K...")
print("This may take a long time because the dataset is several GB.")

dataset_path = Path(
    kagglehub.dataset_download("llll00/urbansound8k")
)

print("\nDataset downloaded to:")
print(dataset_path)


# ============================================================
# 2. Locate metadata
# ============================================================

metadata_path = dataset_path / "UrbanSound8K" / "metadata" / "UrbanSound8K.csv"

# Some Kaggle versions may not have the extra UrbanSound8K folder.
# Try the alternative location if necessary.

if not metadata_path.exists():

    metadata_path = dataset_path / "metadata" / "UrbanSound8K.csv"


if not metadata_path.exists():
    print("\nERROR: UrbanSound8K.csv was not found.")
    print("Dataset location:", dataset_path)
    exit()


print("\nMetadata found:")
print(metadata_path)


# ============================================================
# 3. Read metadata
# ============================================================

df = pd.read_csv(metadata_path)

print("\nTotal audio files in metadata:", len(df))


# ============================================================
# 4. Select only Car Horn
# ============================================================

car_horn = df[df["class"] == "car_horn"].copy()

print("Car Horn files found:", len(car_horn))


# ============================================================
# 5. Create your project folder
# ============================================================

output_path = Path(
    r"C:\Environmental-Sound-Dataset\dataset\audio\car_horn"
)

output_path.mkdir(parents=True, exist_ok=True)

print("\nCopying Car Horn files to:")
print(output_path)


# ============================================================
# 6. Find and copy the Car Horn audio files
# ============================================================

copied = 0
missing = 0

for _, row in car_horn.iterrows():

    filename = row["slice_file_name"]
    fold = int(row["fold"])

    # Normal UrbanSound8K structure
    source = dataset_path / "UrbanSound8K" / "audio" / f"fold{fold}" / filename

    # Alternative structure
    if not source.exists():
        source = dataset_path / "audio" / f"fold{fold}" / filename

    destination = output_path / filename

    if source.exists():

        shutil.copy2(source, destination)

        copied += 1

        if copied % 50 == 0:
            print(f"Copied {copied} files...")

    else:

        print("MISSING:", source)
        missing += 1


# ============================================================
# 7. Final result
# ============================================================

print("\n========================================")
print("CAR HORN EXTRACTION COMPLETE")
print("========================================")

print("Expected Car Horn files :", len(car_horn))
print("Successfully copied     :", copied)
print("Missing files           :", missing)

print("\nDestination:")
print(output_path)

print("\nDone!")