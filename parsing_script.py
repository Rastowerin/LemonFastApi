import asyncio

import httpx
import requests
from bs4 import BeautifulSoup

from parsing_script_config import URL_BASE, HEADERS, API_URL


def get_token():
    user_data = {
        "username": "admin",
        "password": "12345",
    }
    requests.post(f"{API_URL}/users", json=user_data)

    r = requests.post(f"{API_URL}/login", json=user_data)
    token = r.json()['token']
    return token


async def get_id_and_author(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(URL_BASE + url, headers=HEADERS, follow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")

    with open('file.html', 'w', encoding='utf-8') as file:
        file.write(r.text)

    id = ''.join(char if char.isdigit() else '' for char in soup.find(class_="viewbull-bulletin-id__num").get_text())
    author = soup.find(class_="userNick auto-shy").get_text().replace('\n', '')
    return id, author


async def get_item(item, position, token):
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

    url = URL_BASE + 'vladivostok/repository/construction/guard/+/Системы+видеонаблюдения'
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.find_all(class_="bull-list-item-js -exact", limit=10)
    token = get_token()

    try:
        for i in range(len(items)):
            item = items[i]
            asyncio.run(get_item(item, i + 1, token))
    except AttributeError:
        print("Что то пошло не так!"
             f"\nпройите капчу по ссылке {url}"
              "\nлибо включите/выклчите впн")
    else:
        print("Готово!")


if __name__ == '__main__':
    main()
