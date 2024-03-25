import os
import json

# The root directory of your firmware files
root_dir = 'firmware/ESP32 Radar'
version = "3.02"  # Adjust this as necessary
device_types = []  # List to hold all the device types


def create_manifest_for_directory(subdir):
    device_name = os.path.basename(subdir)
    manifest = {
        "name": f"ESP32 Radar for {device_name}",
        "version": version,
        "builds": [{"chipFamily": "ESP32", "parts": []}]
    }

    offsets = [4096, 32768, 53248, 65536, 1376256]
    file_list = sorted(os.listdir(subdir))

    for i, file_name in enumerate(file_list):
        part = {
            "path": os.path.join("firmware", "ESP32 Radar." + version.replace(".", ""), "ESP32 Radar", device_name,
                                 file_name),
            "offset": offsets[i]
        }
        manifest["builds"][0]["parts"].append(part)

    manifest_filename = f"manifest_{device_name}.json"
    with open(manifest_filename, 'w') as manifest_file:
        json.dump(manifest, manifest_file, indent=2)

    # Adding device type for JS file
    device_types.append(device_name)
    print(f"Manifest for {device_name} created.")


for subdir_name in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir_name)
    if os.path.isdir(subdir_path):
        create_manifest_for_directory(subdir_path)

# After all manifests are created, generate a JS file
js_content = f"const deviceTypes = {json.dumps(device_types)};"
with open("device_types.js", "w") as js_file:
    js_file.write(js_content)
