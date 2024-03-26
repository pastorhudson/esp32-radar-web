import os
import json
from urllib.request import urlopen, Request


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

    # Directory to save the downloaded assets
    download_dir = f"../{repo}-latest-release-bin-assets"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

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

    print("All .bin assets downloaded.")


if __name__ == "__main__":
    # Example usage
    download_latest_release_bin_assets("FormationFlight", "FormationFlight")
