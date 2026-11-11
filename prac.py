import json
from pathlib import Path

config = Path("config.json")

if config.exists():
    print("Config file exists.")
    with open(config, "r") as f:
        data = json.load(f)
        # print(data)
else:
    print("Config not exists.")

f = data["categories"]
print(f["Documents"])


fold = Path("E:\\UpWork_Prac\\organizer")

for file in fold.iterdir():
    print(file.name)