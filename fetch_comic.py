
import os
from random import randint
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from dotenv import load_dotenv

from download_and_save_images import download_image


def get_extension_from_url(url):
    """Получает расширение файла из url.
    Args:
        url (str): Ссылка на файл
    Returns:
        str: Расширение файла
    """
    return os.path.splitext(unquote(urlsplit(url).path))[1]


def fetch_random_comic(path_to_images):
    """Загружает случайный коммикс.

    Args:
        path_to_images (str): Путь к файлу, в какой необходимо
                             сохранить изображение
    Returns:
        str: Путь к файлу, в какой сохранили изображение
    """
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()

    comic_number = randint(1, response.json()['num'])

    response = requests.get(f'https://xkcd.com/{comic_number}/info.0.json')
    response.raise_for_status()

    comic_content = response.json()

    comic_file_name = os.path.join(
        path_to_images,
        'comic' + get_extension_from_url(comic_content['img']))

    download_image(
        comic_content['img'],
        comic_file_name)

    return comic_file_name


if __name__ == '__main__':
    load_dotenv()

    path_to_images = os.getenv('PATH_TO_IMAGES', './images/')
    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    print(fetch_random_comic(path_to_images))
