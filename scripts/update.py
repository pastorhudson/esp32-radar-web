import time
from download_assets import download_latest_release_bin_assets
from generate_manifests import generate_manifests


def update():
    while True:
        print("Downloading Latest FormationFlight Firmware")
        download_latest_release_bin_assets("FormationFlight", "FormationFlight")
        print("Generating install Manifests")
        generate_manifests()
        time.sleep(60)


if __name__ == "__main__":
    update()
