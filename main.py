import requests
import os
import random
import glob
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv


def get_last_comics_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def get_extension_from_file(url):
    encode_link = unquote(url, encoding="utf-8", errors="replace")
    chopped_link = urlparse(encode_link)
    return os.path.splitext(chopped_link.path)[1]


def download_random_comics_picture(total_comics):
    random_comics_number = random.randint(1, total_comics)
    url = f"https://xkcd.com/{random_comics_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    picture_details = response.json()
    filename = f"picture.{get_extension_from_file(picture_details['img'])}"
    picture_response = requests.get(picture_details['img'])
    picture_response.raise_for_status()
    with open(f"{filename}", 'wb') as file:
        file.write(picture_response.content)
    return filename, picture_details['alt']


def get_url_for_download_picture(vk_token):
    headers = {
        'Authorization': f'Bearer {vk_token}'
    }
    params = {
        'v': '5.131'
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    vk_response = response.json()
    check_vk_response(vk_response)
    return vk_response['response']['upload_url']


def upload_picture_to_server(filename, url):
    with open(f'{filename}', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    vk_response = response.json()
    check_vk_response(vk_response)
    photo = vk_response['photo']
    server = vk_response['server']
    photo_hash = vk_response['hash']
    return photo, server, photo_hash


def save_picture_on_server(vk_token, photo, server, photo_hash):
    headers = {
        'Authorization': f'Bearer {vk_token}'
    }
    params = {
        'photo': photo,
        'server': server,
        'hash': photo_hash,
        'v': '5.131'
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()
    vk_response = response.json()
    check_vk_response(vk_response)
    owner_id = vk_response['response'][0]['owner_id']
    photo_id = vk_response['response'][0]['id']
    return owner_id, photo_id


def publish_picture_on_vk_group_wall(vk_token, vk_group_id, comment, owner_id, photo_id):
    headers = {
        'Authorization': f'Bearer {vk_token}'
    }
    params = {
        'owner_id': f'-{vk_group_id}',
        'from_group': 0,
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': comment,
        'v': '5.131'
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()
    vk_response = response.json()
    check_vk_response(vk_response)
    return vk_response


def check_vk_response(vk_response):
    try:
        vk_response
    except requests.exceptions.HTTPError as error:
        raise error


def check_users_credentials():
    try:
        vk_token = os.environ['VK_TOKEN']
        vk_group_id = os.environ['GROUP_ID']
        return vk_token, vk_group_id
    except KeyError as error:
        exit(f'Проблема с токеном: {error}')


def main():
    load_dotenv()
    vk_token, vk_group_id = check_users_credentials()
    try:
        total_comics = get_last_comics_number()
        filename, comment = download_random_comics_picture(total_comics)
        url = get_url_for_download_picture(vk_token)
        photo, server, photo_hash = upload_picture_to_server(filename, url)
        owner_id, photo_id = save_picture_on_server(vk_token, photo, server, photo_hash)
        publish_picture_on_vk_group_wall(vk_token, vk_group_id, comment, owner_id, photo_id)
    except requests.exceptions.HTTPError as error:
        print(error)
    finally:
        for file in glob.glob("picture*"):
            os.remove(file)


if __name__ == "__main__":
    main()
