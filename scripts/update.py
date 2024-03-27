import os
import json
from urllib.request import urlopen, Request

root_dir = '/app/storage/FormationFlight-latest-release-bin-assets/'
version = "5.0"
device_types = [{"value": "none", "label": "->Select Target"}]  # Initialize with "Select Target"

def format_label(file_name):
    """
    Extracts device type and additional info from the file name and formats the label.

    :param file_name: the name of the file
    :return: the formatted label extracted from the file name
    """
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
    """
    :param file_path: The file path of the binary file that the manifest will be created for.
    :return: None

    This method creates a manifest file for a given binary file. The manifest contains information about the device, such as its name, version, and chipset.

    The method first extracts the file name from the file path. It then extracts the device name and label from the file name using the `os.path.splitext` function. The label is formatted
    * using the `format_label` function.

    The method determines the chipset of the device based on the label. If the label contains the substring '8266', the chipset is set to "ESP8266". If the label contains the substrings
    * '32' or 'lilygo', the chipset is set to "ESP32". If the label contains the substring 'expresslrs', the chipset is set to "ESP8285".

    The manifest is a dictionary with the following structure:
    {
        "name": "FormationFlight for {label}",
        "version": version,
        "builds": [
            {
                "chipFamily": chipset,
                "parts": [
                    {
                        "path": os.path.join("/app/storage/FormationFlight-latest-release-bin-assets", file_name),
                        "offset": 0
                    }
                ]
            }
        ]
    }

    The manifest is saved to a JSON file with the name "manifest_{device_name}.json" in the '/app/storage' directory using `json.dump`. The file is opened in write mode ('w').

    The device name and label are appended to the `device_types` list as a dictionary with the keys "value" and "label".

    A message is printed to the console indicating that the manifest has been created for the device.

    Example usage:
    create_manifest('/path/to/binary_file.bin')
    """
    file_name = os.path.basename(file_path)
    device_name, _ = os.path.splitext(file_name)
    label = format_label(file_name)
    chipset = ""

    if any(substring in label for substring in ['8266']):
        chipset = "ESP8266"
    elif any(substring in label for substring in ['32', 'lilygo']):
        chipset = 'ESP32'
    elif any(substring in label for substring in ['expresslrs']):
        chipset = "ESP8266"
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
    """
    Generate manifests for binary files in a directory and create a JavaScript file containing sorted device types.

    :return: None

    """
    for file_name in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.bin'):
            create_manifest(file_path)
    sorted_devices = sorted(device_types, key=lambda x: x['label'])
    js_content = "const deviceTypes = " + json.dumps(sorted_devices) + ";"
    with open("/app/storage/device_types.js", "w") as js_file:
        js_file.write(js_content)


def download_latest_release_bin_assets(user, repo):
    """
    :param user: Username of the GitHub account that owns the repository.
    :param repo: Name of the GitHub repository.
    :return: None

    This method downloads the latest binary assets (.bin files) from the given GitHub repository's latest release. It also saves the release version and release notes in a release.txt file
    *.

    The method performs the following steps:
    1. Constructs the GitHub API URL for the latest release using the username and repository name provided.
    2. Creates a request and opens a connection to the GitHub API.
    3. Checks the response status to ensure a successful request.
    4. Parses the JSON response to extract the release version and release notes.
    5. Creates a directory to save the downloaded assets if it doesn't already exist.
    6. Writes the release version and notes to a release.txt file.
    7. Iterates through each asset in the latest release.
    8. Checks if the asset is a .bin file.
    9. Downloads the .bin file by creating a request and opening a connection to the asset URL.
    10. Writes the content of the asset to a file in chunks.
    11. Outputs the progress of downloading each asset.
    12. Outputs the path of each downloaded asset.
    13. Outputs a message indicating that all .bin assets have been downloaded and the release info is saved.
    """
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
    """
    Update Method
    -------------

    Description:
        This method is used to update the FormationFlight Firmware by downloading the latest release binary assets and generating install manifests.

    :return: None

    Example:
        update()
    """
    print("Downloading Latest FormationFlight Firmware")
    download_latest_release_bin_assets("FormationFlight", "FormationFlight")
    print("Generating install Manifests")
    generate_manifests()


if __name__ == "__main__":
    update()
