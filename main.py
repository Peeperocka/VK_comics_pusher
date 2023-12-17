import os
import random
import requests

from dotenv import load_dotenv
from supporting_scripts import download_img


def get_comics(comics_num):
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

    return response.json()['response']['upload_url']


def push_image_to_server(filepath, upload_url):
    with open(filepath, 'rb') as f:

        files = {
            'photo': f
        }

        response = requests.post(upload_url, files=files)
        response.raise_for_status()

    return response.json()


def save_wall_photo(response_data, access_token, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'hash': response_data['hash'],
        'access_token': access_token,
        'group_id': group_id,
        'v': 5.154,
        'photo': response_data['photo'],
        'server': response_data['server'],
    }

    response = requests.post(url, params)
    response.raise_for_status()

    return response.json()['response']


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
    print(response.text)


if __name__ == '__main__':
    load_dotenv()
    os.makedirs('images/', exist_ok=True)

    access_token = os.environ['ACCESS_TOKEN']
    app_id = os.environ['APP_ID']
    group_id = os.environ['GROUP_ID']

    filepath = 'images/img.png'

    last_comics_num = get_last_comics_num()
    comics_text = get_comics(random.randint(0, last_comics_num))
    download_url = get_download_url(group_id, access_token)
    response_data = push_image_to_server(filepath, download_url)
    response = save_wall_photo(response_data, access_token, group_id)
    post_on_wall(
        response[0]['owner_id'],
        response[0]['id'],
        access_token,
        comics_text
    )

    os.remove('images/img.png')
