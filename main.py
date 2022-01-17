import os
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from dotenv import load_dotenv

from download_and_save_images import download_image


def get_file_name_from_url(url):
    """Получает имя файла из url.
    Args:
        url (str): Ссылка на файл
    Returns:
        str: Расширение файла
    """
    return os.path.basename(unquote(urlsplit(url).path))


def fetch_comic(path_to_images):
    """Загружает коммиксы."""
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()

    comic_content = response.json()
    download_image(
        comic_content['img'],
        os.path.join(
            path_to_images,
            get_file_name_from_url(comic_content['img'])))

    # if comic_content['links']['flickr']['original']:
    #     for index, url in enumerate(
    #             comic_content['links']['flickr']['original'], 1):

    #         response = requests.get(url)
    #         response.raise_for_status()

    #         download_image(
    #             url,
    #             os.path.join(path_to_images, 'spacex%s.jpg' % index))
    #     break


if __name__ == '__main__':
    load_dotenv()
    path_to_images = os.getenv('PATH_TO_IMAGES', './Files/')
    timeout = int(os.getenv('TIMEOUT', 86400))

    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    fetch_comic(path_to_images)

    # while True:
    #     fetch_spacex_last_launch(path_to_images)

    #     time.sleep(timeout)
