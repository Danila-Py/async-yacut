import urllib
import os
from http import HTTPStatus

from dotenv import load_dotenv
import aiohttp
from . import app


load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
API_VERSION = 'v1'
UPLOAD_PATH = 'app:/{}'
REQUEST_UPLOAD_URL = (
    f'{app.config["API_HOST"]}'
    f'{API_VERSION}/disk/resources/upload'
)
REQUEST_DOWNLOAD_URL = (
    f'{app.config["API_HOST"]}'
    f'{API_VERSION}/disk/resources/download'
)
GET_LINK_FAILED = 'Не удалось получить ссылку: {}'


async def upload_files_to_yadisk(file_data, filename):
    async with aiohttp.ClientSession() as session:
        params = {
            'path': f'app:/{filename}',
            'overwrite': 'true'
        }
        async with session.get(
            REQUEST_UPLOAD_URL,
            headers=AUTH_HEADERS,
            params=params,
        ) as response:
            upload_url = (await response.json()).get('href')

        async with session.put(upload_url, data=file_data) as upload_response:
            if upload_response.status not in [
                HTTPStatus.CREATED,
                HTTPStatus.ACCEPTED,
            ]:
                raise IOError(
                    REQUEST_UPLOAD_URL.format(upload_response.status)
                )
        return f'app:/{filename}'


async def get_download_link(file_path):
    async with aiohttp.ClientSession() as session:
        params = {'path': file_path}
        async with session.get(
            REQUEST_DOWNLOAD_URL,
            headers=AUTH_HEADERS,
            params=params,
        ) as response:
            if response.status != HTTPStatus.OK:
                raise IOError(
                    GET_LINK_FAILED.format(response.status)
                )
            return (await response.json()).get('href')


async def upload_file_and_get_url(session, file):
    """Функция загрузки файлов и получения URL для скачивания."""
    async with session.get(
            REQUEST_UPLOAD_URL,
            headers=AUTH_HEADERS,
            params={
                'path': UPLOAD_PATH.format(file.filename),
                'overwrite': 'True'
            },
    ) as response:
        upload_url = (await response.json())['href']
    async with session.put(data=file.read(), url=upload_url) as response:
        location = urllib.parse.unquote(response.headers['Location'])
    location = location.replace('/disk', '')
    async with session.get(
            REQUEST_DOWNLOAD_URL,
            headers=AUTH_HEADERS,
            params={'path': location, },
    ) as response:
        download_url = (await response.json())['href']
    return dict(filename=file.filename, url=download_url)