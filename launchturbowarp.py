import os
import yaml

def launch_tw_server_cmd() -> None:
    # go to the server path
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    os.chdir(config["server_path"])

    # run the server using "npm ci" and "npm run dev"
    os.system("npm ci")
    os.system("npm run dev")