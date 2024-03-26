import time
from scripts.download_assets import download_latest_release_bin_assets
from scripts.generate_manifests import generate_manifests


def update():
    while True:
        download_latest_release_bin_assets("FormationFlight", "FormationFlight")
        generate_manifests()
        time.sleep(3600)


if __name__ == "__main__":
    update()
