import os
import json

root_dir = '/app/www/storage/FormationFlight-latest-release-bin-assets/'
version = "5.0"
device_types = []


def format_label(file_name):
    # Extracts device type and additional info from the file name
    try:
        parts = file_name.replace('diy_', '')
    except Exception as e:
        parts = file_name

    parts = parts.replace('.bin', '').split('_')
    device_base = parts[0] if len(parts) > 1 else "unknown"
    if 'lilygo' in parts[1]:
        if len(parts[1]) >= 5:
            parts[1] = f"Lilygo v{parts[1][6]}.{parts[1][:7]}"

    additional_info = " ".join(parts[1:])  # Handles any additional info like frequency
    label = f"{device_base.capitalize()} {additional_info}".strip()
    return label if label else file_name


def create_manifest(file_path):
    file_name = os.path.basename(file_path)
    device_name, _ = os.path.splitext(file_name)
    label = format_label(file_name)
    chipset = ""

    if any(substring in label for substring in ['8266']):
        chipset = "ESP8266"
    elif any(substring in label for substring in ['32', 'lilygo']):
        chipset = 'ESP32'
    elif any(substring in label for substring in ['expresslrs']):
        chipset = "ESP8285"
    manifest = {
        "name": f"FormationFlight for {label}",
        "version": version,
        "builds": [{"chipFamily": chipset, "parts": [{
            "path": os.path.join("/storage/FormationFlight-latest-release-bin-assets", file_name),
            "offset": 0  # Assuming a single binary without specific offsets
        }]}]
    }

    manifest_filename = f"/app/www/storage/manifest_{device_name}.json"
    with open(manifest_filename, 'w') as manifest_file:
        json.dump(manifest, manifest_file, indent=2)

    device_types.append({"value": device_name, "label": label})
    print(f"Manifest for {device_name} ({label}) created.")


def generate_manifests():

    for file_name in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.bin'):
            create_manifest(file_path)

    js_content = "const deviceTypes = " + json.dumps(device_types) + ";"
    with open("/app/www/storage/device_types.js", "w") as js_file:
        js_file.write(js_content)


if __name__ == "__main__":
    generate_manifests()
