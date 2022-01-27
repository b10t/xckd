import os
from pathlib import Path

from dotenv import load_dotenv

from fetch_comic import fetch_random_comic
from fetch_vk_api import upload_comic_to_wall_vk


if __name__ == '__main__':
    load_dotenv()

    vk_token_id = os.getenv('VK_TOKEN_ID', '')
    vk_group_id = os.getenv('VK_GROUP_ID', '')

    path_to_images = os.getenv('PATH_TO_IMAGES', './images/')
    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    comic_file_name, commentary_comic = fetch_random_comic(path_to_images)

    upload_comic_to_wall_vk(
        vk_token_id,
        vk_group_id,
        comic_file_name,
        commentary_comic)

    os.remove(comic_file_name)
