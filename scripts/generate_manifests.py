import os
import json


# The root directory of your firmware files
root_dir = '../firmware/ESP32 Radar'
version = "3.02"  # Version of your firmware, adjust as necessary

# Function to create a manifest for a given subdirectory
def create_manifest_for_directory(subdir):
    # Extracting the device name from the path (e.g., 'lilygo10_433')
    device_name = os.path.basename(subdir)
    manifest = {
        "name": f"ESP32 Radar for {device_name}",
        "version": version,
        "builds": [
            {
                "chipFamily": "ESP32",
                "parts": []
            }
        ]
    }

    # Offsets for each file, assuming a specific order. Adjust if necessary.
    offsets = [4096, 32768, 53248, 65536, 1376256]
    file_list = sorted(os.listdir(subdir))  # Sorting to ensure order is consistent

    for i, file_name in enumerate(file_list):
        part = {
            "path": os.path.join("firmware", "ESP32 Radar." + version.replace(".", ""), "ESP32 Radar", device_name, file_name),
            "offset": offsets[i]
        }
        manifest["builds"][0]["parts"].append(part)

    # Generating the manifest filename
    manifest_filename = f"../manifest_{device_name}.json"
    with open(manifest_filename, 'w') as manifest_file:
        json.dump(manifest, manifest_file, indent=2)
    print(f"Manifest for {device_name} created.")

# Main script execution
for subdir_name in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir_name)
    if os.path.isdir(subdir_path):
        create_manifest_for_directory(subdir_path)
