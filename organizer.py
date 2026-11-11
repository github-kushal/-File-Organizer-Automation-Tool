from pathlib import Path    
import logging
import json
import sys


# 1. Create a custom logger
logger = logging.getLogger("organizer_logger")
logger.setLevel(logging.DEBUG)  # Capture all logs from DEBUG level and above


file_handler = logging.FileHandler("app.log", mode="a")  # Appends to a file

# 3. Set levels for individual handlers and above
file_handler.setLevel(logging.DEBUG)   # File captures everything (DEBUG+)

# 4. Create a standard format for log messages
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(log_format)

# 5. Add handlers to the logger
logger.addHandler(file_handler)



class Organizer:
    confi = Path(__file__).resolve().parent / "config.json"

    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)

    def organize_files(self):
        if not self.folder_path.exists() or not self.folder_path.is_dir():
            logger.error("Invalid folder path provided.")
            return

        try:
            with open(self.confi, "r") as conf:
                config_data = json.load(conf)
            categories = config_data["categories"]

            for file in self.folder_path.iterdir():
                if file.is_file():
                    ext = file.suffix.lower()
                    category = None

                    for category_name, extensions in categories.items():
                        if ext in extensions:
                            category = category_name
                            break

                    if category is None:
                        logger.info("Skipped unsupported file: %s", file.name)
                        continue

                    destination_folder = self.folder_path / category
                    destination_folder.mkdir(parents=True, exist_ok=True)

                    destination = destination_folder / file.name

                    if destination.exists():
                        logger.warning("File already exists in destination: %s", file.name)
                        continue

                    try:
                        file.rename(destination)

                        logger.info(
                            "Moved %s to %s.",
                            file.name,
                            category
                        )

                    except OSError:
                        logger.exception("Failed to move %s.", file.name)
                        continue 

        except FileNotFoundError:
            logger.error("Configuration file not found.")

        except json.JSONDecodeError:
            logger.error("Configuration file contains invalid JSON.")

        except OSError:
            logger.exception("Could not read the configuration file.")


if len(sys.argv) > 1:
    folder_path = sys.argv[1]  
    org = Organizer(Path(folder_path))
    org.organize_files()
else:
    logger.critical("No folder path provided. Please provide a folder path as a command-line argument.")
    print("No folder path provided. Please provide a folder path as a command-line argument.")
