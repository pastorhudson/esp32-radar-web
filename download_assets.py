import requests
import os


def download_latest_release_bin_assets(user, repo):
    # GitHub API URL for the latest release
    api_url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"

    # Send a GET request to the GitHub API
    response = requests.get(api_url)
    response.raise_for_status()  # Check for errors

    # Parse the JSON response
    data = response.json()

    # Directory to save the downloaded assets
    download_dir = f"{repo}-latest-release-bin-assets"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Loop through each asset in the latest release
    for asset in data['assets']:
        asset_url = asset['browser_download_url']
        asset_name = asset['name']

        # Check if the file is a .bin file before downloading
        if asset_name.endswith('.bin'):
            print(f"Downloading {asset_name}...")
            asset_response = requests.get(asset_url, stream=True)
            asset_path = os.path.join(download_dir, asset_name)

            with open(asset_path, 'wb') as f:
                for chunk in asset_response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Downloaded {asset_name} to {asset_path}")
        else:
            print(f"Skipping {asset_name}, not a .bin file.")

    print("All .bin assets downloaded.")


# Example usage
# Replace 'FormationFlight' with the GitHub username and 'FormationFlight' with the repository name
download_latest_release_bin_assets("FormationFlight", "FormationFlight")
