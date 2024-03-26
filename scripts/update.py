import time
from scripts.download_assets import download_latest_release_bin_assets
from scripts.generate_manifests import generate_manifests
import os


def update():
    os.system("pip install -r requirements.txt")
    download_latest_release_bin_assets("FormationFlight", "FormationFlight")
    generate_manifests()


if __name__ == "__main__":
    update()
