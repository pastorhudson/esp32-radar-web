import os
import json

root_dir = './FormationFlight-latest-release-bin-assets/'
version = "3.02"
device_types = []

def format_label(file_name):
    # Extracts device type and additional info from the file name
    parts = file_name.replace('.bin', '').split('_')
    device_base = parts[1] if len(parts) > 1 else "unknown"
    additional_info = " ".join(parts[2:])  # Handles any additional info like frequency
    label = f"{device_base.capitalize()} {additional_info}".strip()
    return label if label else file_name

def create_manifest(file_path):
    file_name = os.path.basename(file_path)
    device_name, _ = os.path.splitext(file_name)
    label = format_label(file_name)
    manifest = {
        "name": f"FormationFlight for {label}",
        "version": version,
        "builds": [{"chipFamily": "ESP32", "parts": [{
            "path": os.path.join("firmware", "FormationFlight." + version.replace(".", ""), file_name),
            "offset": 0  # Assuming a single binary without specific offsets
        }]}]
    }

    manifest_filename = f"manifest_{device_name}.json"
    with open(manifest_filename, 'w') as manifest_file:
        json.dump(manifest, manifest_file, indent=2)

    device_types.append({"value": device_name, "label": label})
    print(f"Manifest for {device_name} ({label}) created.")

for file_name in os.listdir(root_dir):
    file_path = os.path.join(root_dir, file_name)
    if os.path.isfile(file_path) and file_name.endswith('.bin'):
        create_manifest(file_path)

js_content = "const deviceTypes = " + json.dumps(device_types) + ";"
with open("device_types.js", "w") as js_file:
    js_file.write(js_content)
