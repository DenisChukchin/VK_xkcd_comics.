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


def get_random_comics_number():
    total_comics = get_last_comics_number()
    return random.randint(1, total_comics)


def get_picture_url_and_comment(comics_number):
    url = f"https://xkcd.com/{comics_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    picture_details = response.json()
    picture_url_and_comment = [picture_details['img'], picture_details['alt']]
    return picture_url_and_comment


def get_extension_from_file(url):
    encode_link = unquote(url, encoding="utf-8", errors="replace")
    chopped_link = urlparse(encode_link)
    return os.path.splitext(chopped_link.path)[1]


def fetch_picture(picture_url):
    template_name = ["picture", get_extension_from_file(picture_url)]
    filename = "".join(template_name)
    download_picture_to_computer(picture_url, filename)
    return filename


def download_picture_to_computer(picture_url, filename):
    picture_response = requests.get(picture_url)
    picture_response.raise_for_status()
    with open(f"{filename}", 'wb') as file:
        file.write(picture_response.content)


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
    return response.json()['response']['upload_url']


def upload_picture_to_server(vk_token, filename):
    url = get_url_for_download_picture(vk_token)
    with open(f'{filename}', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    return response.json()


def save_picture_on_server(vk_token, filename):
    picture_details = upload_picture_to_server(vk_token, filename)
    headers = {
        'Authorization': f'Bearer {vk_token}'
    }
    params = {
        'photo': picture_details.get('photo'),
        'server': picture_details.get('server'),
        'hash': picture_details.get('hash'),
        'v': '5.131'
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def publish_picture_on_vk_group_wall(vk_token, vk_group_id, comment, filename):
    picture_details = save_picture_on_server(vk_token, filename)
    owner_id = picture_details['response'][0]['owner_id']
    photo_id = picture_details['response'][0]['id']
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
    return response.json()


def check_vk_tokens():
    load_dotenv()
    try:
        vk_token = os.environ['VK_TOKEN']
        vk_group_id = os.environ['GROUP_ID']
        return vk_token, vk_group_id
    except KeyError as error:
        exit(f'Проблема с токеном: {error}')


def main():
    vk_token, vk_group_id = check_vk_tokens()
    comics_number = get_random_comics_number()
    try:
        picture_url, comment = get_picture_url_and_comment(comics_number)
        filename = fetch_picture(picture_url)
        publish_picture_on_vk_group_wall(vk_token, vk_group_id, comment, filename)
    except requests.exceptions.HTTPError as error:
        print(error)
    finally:
        for file in glob.glob("picture*"):
            os.remove(file)


if __name__ == "__main__":
    main()
