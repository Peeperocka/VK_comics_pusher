import os
import random
import requests

from pathlib import Path
from dotenv import load_dotenv


def handle_vk_response(response_data):

    if 'error' in response_data:
        error = response_data['error']
        raise requests.HTTPError(
            error['error_code'],
            error['error_msg'],
        )


def download_img(url, filepath):
    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_comic(comics_num):
    url = f'https://xkcd.com/{comics_num}/info.0.json'
    filename = 'images/img.png'

    response = requests.get(url)
    response.raise_for_status()

    image_data = response.json()

    download_img(image_data['img'], filename)
    return image_data['alt']


def get_last_comics_num():
    url = 'https://xkcd.com/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    return response.json()['num']


def get_download_url(group_id, access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'

    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': 5.154,
    }

    response = requests.get(url, params)
    response.raise_for_status()
    response_data = response.json()
    handle_vk_response(response_data)

    return response_data['response']['upload_url']


def push_image_to_server(filepath, upload_url):
    with open(filepath, 'rb') as f:

        files = {
            'photo': f
        }

        response = requests.post(upload_url, files=files)

    response.raise_for_status()
    response_data = response.json()
    handle_vk_response(response_data)

    return response_data['hash'], response_data['photo'], response_data['server']


def save_wall_photo(
        server_image_hash, server_image_photo,
        server_image_server, access_token, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'hash': server_image_hash,
        'photo': server_image_photo,
        'server': server_image_server,
        'access_token': access_token,
        'group_id': group_id,
        'v': 5.154,
    }

    response = requests.post(url, params)
    response.raise_for_status()
    response_data = response.json()
    handle_vk_response(response_data)

    return response_data['response']


def post_on_wall(owner_id, media_id, access_token, alt):
    url = 'https://api.vk.com/method/wall.post'

    params = {
        'v': 5.154,
        'access_token': access_token,
        'from_group': 1,
        'owner_id': owner_id,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': alt
    }

    response = requests.post(url, params)
    response.raise_for_status()

    response_data = response.json()
    handle_vk_response(response_data)


if __name__ == '__main__':
    load_dotenv()
    Path('images').mkdir(exist_ok=True)

    access_token = os.environ['VK_IMPLICIT_FLOW_TOKEN']
    group_id = os.environ['VK_GROUP_ID']

    filepath = Path('images') / 'img.png'

    last_comics_num = get_last_comics_num()

    try:
        comics_text = get_comic(random.randint(0, last_comics_num))
        download_url = get_download_url(group_id, access_token)

        server_image_hash, server_image_photo, server_image_server = \
            push_image_to_server(filepath, download_url)

        response = save_wall_photo(
            server_image_hash, server_image_photo,
            server_image_server, access_token,
            group_id
        )

        post_on_wall(
            response[0]['owner_id'],
            response[0]['id'],
            access_token,
            comics_text
        )

    finally:
        filepath.unlink(missing_ok=True)
