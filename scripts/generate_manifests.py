import os
import json

root_dir = '/app/www/storage/FormationFlight-latest-release-bin-assets/'
version = "5.0"
device_types = []


def format_label(file_name):
    # Extracts device type and additional info from the file name
    parts = file_name.replace('.bin', '').split('_')
    device_base = parts[1] if len(parts) > 1 else "unknown"

    if 'lilygo' in file_name.lower():
        try:
            version_index = parts.index([part for part in parts if 'lilygo' in part.lower()][0])
            version = f"v{parts[version_index][6:]}.{parts[version_index + 1]}"
            frequency = parts[version_index + 2]
            if frequency == "433":
                frequency_label = "433mhz"
            elif frequency == "868":
                frequency_label = "868mhz"
            elif frequency == "915":
                frequency_label = "915mhz"
            else:
                frequency_label = ""
            label = f"Lora Lilygo {version} {frequency_label}"
        except (IndexError, ValueError):
            # Fallback in case the expected pattern is not found
            label = "Lora Lilygo Unknown Version"
    elif 'expresslrs' in file_name.lower():
        # Assuming any expresslrs file with "2400" is for 2.4ghz
        if "2400" in file_name:
            label = "Express LRS Rx 2.4ghz"
        else:
            # Default expresslrs labeling
            additional_info = " ".join(parts[2:])  # Handles any additional info like frequency
            label = f"Express LRS Rx {additional_info}"
    else:
        additional_info = " ".join(parts[2:])  # Handles any additional info
        label = f"{device_base.capitalize()} {additional_info}".strip()

    return label



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
