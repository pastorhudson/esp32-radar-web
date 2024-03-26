from scripts.download_assets import download_latest_release_bin_assets
from scripts.generate_manifests import generate_manifests


def update():
    download_latest_release_bin_assets("FormationFlight", "FormationFlight")
    generate_manifests()


if __name__ == "__main__":
    update()
