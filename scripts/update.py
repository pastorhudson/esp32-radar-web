import os
import json
from urllib.request import urlopen, Request

root_dir = '/app/storage/FormationFlight-latest-release-bin-assets/'
version = "5.0"
device_types = []


def format_label(file_name):
    # Extracts device type and additional info from the file name
    try:
        parts = file_name.replace('diy_', '')
    except Exception as e:
        parts = file_name
    try:
        parts = parts.replace('433', '433MHz')
        parts = parts.replace('868', '868MHz')
        parts = parts.replace('915', '915MHz')
        parts = parts.replace('2400', '2.4GHz')

    except Exception as e:
        parts = parts
    parts = parts.replace('.bin', '').split('_')
    device_base = parts[0] if len(parts) > 1 else "unknown"
    if 'lilygo' in parts[1] and 't_beam' not in parts[1]:
        if len(parts[1]) > 6:
            parts[1] = f"Lilygo v{parts[1][6]}.{parts[1][7:]}"
        else:
            parts[1] = f"Lilygo"
    elif 'Heltec' in parts[1]:
        parts[4] = f"v{parts[4][0]}.{parts[4][1]}"

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
            "path": os.path.join("/app/storage/FormationFlight-latest-release-bin-assets", file_name),
            "offset": 0  # Assuming a single binary without specific offsets
        }]}]
    }

    manifest_filename = f"/app/storage/manifest_{device_name}.json"
    with open(manifest_filename, 'w') as manifest_file:
        json.dump(manifest, manifest_file, indent=2)

    device_types.append({"value": device_name, "label": label})
    print(f"Manifest for {device_name} ({label}) created.")


def generate_manifests():
    for file_name in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.bin'):
            create_manifest(file_path)
    sorted_devices = sorted(device_types, key=lambda x: x['label'])
    js_content = "const deviceTypes = " + json.dumps(sorted_devices) + ";"
    with open("/app/storage/device_types.js", "w") as js_file:
        js_file.write(js_content)


def download_latest_release_bin_assets(user, repo):
    # GitHub API URL for the latest release
    api_url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"

    # Create a request and open a connection to the GitHub API
    request = Request(api_url)
    with urlopen(request) as response:
        # Ensure that the request was successful
        if response.status != 200:
            raise Exception(f"GitHub API request failed with status code {response.status}")

        # Parse the JSON response
        data = json.loads(response.read().decode())

    # Extracting release version and release notes
    release_version = data.get('tag_name', 'N/A')
    release_notes = data.get('body', 'No release notes available.')

    # Directory to save the downloaded assets
    download_dir = f"/app/storage/{repo}-latest-release-bin-assets"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Path for the release.txt file
    release_file_path = os.path.join(download_dir, "release.txt")
    with open(release_file_path, 'w') as release_file:
        # Writing release version and notes to the file
        release_file.write(f"Release Version: {release_version}\n\nRelease Notes:\n{release_notes}\n")

    # Loop through each asset in the latest release
    for asset in data['assets']:
        asset_url = asset['browser_download_url']
        asset_name = asset['name']

        # Check if the file is a .bin file before downloading
        if asset_name.endswith('.bin'):
            print(f"Downloading {asset_name}...")

            # Create a request for the asset and open a connection
            asset_request = Request(asset_url)
            with urlopen(asset_request) as asset_response, open(os.path.join(download_dir, asset_name), 'wb') as f:
                # Write the content to a file in chunks
                while chunk := asset_response.read(8192):
                    f.write(chunk)

            print(f"Downloaded {asset_name} to {os.path.join(download_dir, asset_name)}")
        else:
            print(f"Skipping {asset_name}, not a .bin file.")

    print("All .bin assets downloaded and release info saved.")


def update():
    print("Downloading Latest FormationFlight Firmware")
    download_latest_release_bin_assets("FormationFlight", "FormationFlight")
    print("Generating install Manifests")
    generate_manifests()


if __name__ == "__main__":
    update()
