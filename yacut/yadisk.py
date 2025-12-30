import os
import asyncio
import aiohttp
import urllib

from dotenv import load_dotenv


load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
API_VERSION = 'v1'
API_HOST = 'https://cloud-api.yandex.net/'
UPLOAD_PATH = 'app:/{}'
REQUEST_UPLOAD_URL = (
    f'{API_HOST}'
    f'{API_VERSION}/disk/resources/upload'
)
REQUEST_DOWNLOAD_URL = (
    f'{API_HOST}'
    f'{API_VERSION}/disk/resources/download'
)


async def upload_files_to_yadisk(files):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[upload_single_file(session, file) for file in files]
        )


async def upload_single_file(session, file):
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