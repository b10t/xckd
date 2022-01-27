import requests


class VkResponseError(TypeError):
    """Класс-исключение для отображения ошибок от VK API.

    Args:
        TypeError (BaseException): Исключение
    """
    pass


def get_response_from_vk_api(response):
    """Обрабатывает ответ от VK API.

    Args:
        response (str): Ответ с данными от VK API

    Returns:
        str: Ответ с данными от VK API
    """
    if 'error' in response:
        raise(VkResponseError(response['error']['error_msg']))

    return response


def upload_comic_to_wall_vk(vk_token_id,
                            vk_group_id,
                            comic_file_name,
                            comic_commentary):
    """Загружает комикс на стену во Вконтакте.

    Args:
        vk_token_id (str): TOKEN VK API ID
        vk_group_id (str): ID group VK API
        comic_file_name (str): Путь к файлу комикса
        comic_commentary (str): Комментарий к комиксу
    """
    upload_server_url = get_wall_upload_server(
        vk_token_id,
        vk_group_id
    )

    upload_content = fetch_upload_comic(
        upload_server_url,
        comic_file_name
    )

    wall_photo_content = save_wall_photo(
        vk_token_id,
        vk_group_id,
        upload_content
    )

    post_comic_to_group(
        vk_token_id,
        vk_group_id,
        comic_commentary,
        wall_photo_content
    )


def get_wall_upload_server(vk_token_id, vk_group_id):
    """Получает сервер загрузки Вконтакте.

    Args:
        vk_token_id (str): TOKEN VK API ID
        vk_group_id (str): ID group VK API

    Returns:
        str: Url сервера загрузки.
    """
    url = 'https://api.vk.com/method/photos.getWallUploadServer'

    params = {
        'access_token': vk_token_id,
        'group_id': vk_group_id,
        'v': '5.131'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return get_response_from_vk_api(response.json())['response']['upload_url']


def fetch_upload_comic(upload_server_url, comic_file_name):
    """Загружает комикс на сервер Вконтакте.

    Args:
        upload_server_url (str): Url сервера загрузки
        comic_file_name (str): Путь к файлу комикса

    Returns:
        str: Данные по загруженому комиксу
    """
    with open(comic_file_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_server_url, files=files)
        response.raise_for_status()

        return get_response_from_vk_api(response.json())


def save_wall_photo(vk_token_id, vk_group_id, upload_content):
    """Сохраняет комикс на стене Вконтакте.

    Args:
        vk_token_id (str): TOKEN VK API ID
        vk_group_id (str): ID group VK API
        upload_content (str): Данные по загруженому комиксу

    Returns:
        str: Данные по сохранённому комиксу
    """
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'access_token': vk_token_id,
        'group_id': vk_group_id,
        'server': upload_content['server'],
        'photo': upload_content['photo'],
        'hash': upload_content['hash'],
        'v': '5.131'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return get_response_from_vk_api(response.json())['response'][0]


def post_comic_to_group(vk_token_id, vk_group_id, message, attachments):
    """Отправляет сохранённый комикс на стену.

    Args:
        vk_token_id (str): TOKEN VK API ID
        vk_group_id (str): ID group VK API
        message (str): Сообщение к публикуемому комиксу
        attachments (str): Данные по сохранённому комиксу
    """
    url = 'https://api.vk.com/method/wall.post'

    params = {
        'access_token': vk_token_id,
        'owner_id': f'-{vk_group_id}',
        'from_group': 0,
        'message': message,
        'attachments': f'photo{attachments["owner_id"]}_{attachments["id"]}',
        'v': '5.131'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
