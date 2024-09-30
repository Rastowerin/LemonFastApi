import asyncio
from time import sleep

import httpx
import requests
from bs4 import BeautifulSoup, Tag
from fake_useragent import UserAgent

from parsing_script_config import URL_BASE, HEADERS, API_URL, LIMIT

ua = UserAgent()


def headers() -> dict[str, str]:
    return {
        **HEADERS,
        'user-agent': ua.random
    }


def wait_for_api():
    while True:
        try:
            requests.get(API_URL, '/items')
        except requests.exceptions.ConnectionError:
            sleep(1)
            print('ждем апи...')
        else:
            break


def get_token() -> str:
    user_data = {
        "username": "admin",
        "password": "12345",
    }
    requests.post(f"{API_URL}/users", json=user_data)

    r = requests.post(f"{API_URL}/login", json=user_data)
    token = r.json()['token']
    return token


async def get_id_and_author(url) -> tuple[str, str]:
    async with httpx.AsyncClient() as client:
        r = await client.get(URL_BASE + url, headers=headers(), follow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")

    id = ''.join(char if char.isdigit() else '' for char in soup.find(class_="viewbull-bulletin-id__num").get_text())
    author = soup.find(class_="userNick auto-shy").get_text().replace('\n', '')
    return id, author


async def get_item(item: Tag, position: int, token: str) -> None:
    title = item.find(class_="bulletinLink bull-item__self-link auto-shy").get_text()
    views = item.find(class_="views nano-eye-text").get_text()
    sub_url = item.find(class_="bulletinLink bull-item__self-link auto-shy").get("href")
    id, author = await get_id_and_author(sub_url)

    data = {
        "id": id,
        "position": position,
        "author": author,
        "title": title,
        "views": views,
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_URL}/items", json=data, headers={"Authorization": f"Bearer {token}"})
        if r.status_code not in (201, 409):
            raise Exception(r.text)


def main():

    wait_for_api()

    url = URL_BASE + 'vladivostok/service/construction/guard/+/Системы+видеонаблюдения/'
    r = requests.get(url, headers=headers())
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.find_all(class_="bull-list-item-js -exact", limit=LIMIT)
    token = get_token()

    try:

        for i in range(LIMIT):
            item = items[i]
            asyncio.run(get_item(item, i + 1, token))

    except (AttributeError, IndexError):
        print("Что-то пошло не так!"
             f"\nПройите капчу по ссылке {url}"
              "\nЛибо включите/выклчите впн")
    else:
        print("Готово!")


if __name__ == '__main__':
    main()
