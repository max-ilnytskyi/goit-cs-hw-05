import argparse
import asyncio
import os
from pathlib import Path
import shutil
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(src_path: Path, dest_folder: Path):
    try:
        ext = src_path.suffix.lstrip(".").lower() or "unknown"
        target_subfolder = dest_folder / ext
        target_subfolder.mkdir(parents=True, exist_ok=True)

        dest_path = target_subfolder / src_path.name

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy2, src_path, dest_path)
        logging.info(f"Copied {src_path} to {dest_path}")

    except Exception as e:
        logging.error(f"Error copying file {src_path}: {e}")


async def read_folder(src_folder: Path, dest_folder: Path):
    tasks = []

    for root, _, files in os.walk(src_folder):
        for file_name in files:
            file_path = Path(root) / file_name
            tasks.append(copy_file(file_path, dest_folder))

    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(
        description="Sort files by extensions into subdirectories asynchronously."
    )
    parser.add_argument("source", type=str, help="Source folder path")
    parser.add_argument("destination", type=str, help="Destination folder path")

    args = parser.parse_args()

    src_folder = Path(args.source).resolve()
    dest_folder = Path(args.destination).resolve()

    if not src_folder.is_dir():
        logging.error(f"Source folder does not exist: {src_folder}")
        return

    dest_folder.mkdir(parents=True, exist_ok=True)
    logging.info(f"Starting file sorting from {src_folder} to {dest_folder}")

    try:
        asyncio.run(read_folder(src_folder, dest_folder))
        logging.info("File sorting completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
