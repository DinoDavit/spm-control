from pathlib import Path
import yaml


def test_scan_yaml_loads():
    config_path = Path("config_files/scan.yaml")

    with config_path.open("r") as file:
        config = yaml.safe_load(file)

    scan_config = config["scan"]

    print("z_focus:", scan_config["z_focus"])
    print("xlim:", scan_config["xlim"])
    print("ylim:", scan_config["ylim"])
    print("resolution:", scan_config["resolution"])
    print("show_plot:", scan_config["show_plot"])
    print("intensity_histograms:", scan_config["intensity_histograms"])
    print("limit_plot:", scan_config["limit_plot"])
    print("vmin:", scan_config["vmin"])
    print("vmax:", scan_config["vmax"])
    print("folder_path:", scan_config["folder_path"])

    assert "z_focus" in scan_config
    assert "xlim" in scan_config
    assert "ylim" in scan_config
    assert "resolution" in scan_config
    assert "folder_path" in scan_config


if __name__ == "__main__":
    test_scan_yaml_loads()