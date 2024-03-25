import os
import json

root_dir = './firmware/ESP32 Radar'
version = "3.02"
device_types = []  # This will now hold dictionaries with 'value' and 'label' keys


def format_label(device_name):
    # Assuming device_name format is like 'lilygo10_433'
    parts = device_name.split('_')
    if len(parts) == 2 and parts[0].startswith('lilygo'):
        version = parts[0][6:7] + '.' + parts[0][7:]
        mhz = parts[1]
        return f"Lilygo TTGO v{version} {mhz}mhz"
    return device_name  # Default case


def create_manifest_for_directory(subdir):
    device_name = os.path.basename(subdir)
    label = format_label(device_name)
    manifest = {
        "name": f"ESP32 Radar for {label}",
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

    device_types.append({"value": device_name, "label": label})
    print(f"Manifest for {device_name} ({label}) created.")


for subdir_name in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir_name)
    if os.path.isdir(subdir_path):
        create_manifest_for_directory(subdir_path)

js_content = "const deviceTypes = " + json.dumps(device_types) + ";"
with open("device_types.js", "w") as js_file:
    js_file.write(js_content)
