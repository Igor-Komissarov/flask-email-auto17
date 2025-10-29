import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
API_URL = "https://api.github.com"

def get_headers():
    if not TOKEN:
        raise ValueError("❌ GITHUB_TOKEN не найден в .env")
    return {"Authorization": f"token {TOKEN}"}


def create_or_update_file(repo, path, content, message, branch="main"):
    """
    Создаёт или обновляет файл в репозитории на GitHub.
    repo: "username/reponame"
    path: путь к файлу в репо, например "auto/test.txt"
    content: содержимое файла (текст)
    message: сообщение коммита
    """
    url = f"{API_URL}/repos/{repo}/contents/{path}"

    headers = get_headers()
    data = {"message": message, "content": content.encode("utf-8").hex(), "branch": branch}

    # Проверим, существует ли файл
    get_resp = requests.get(url, headers=headers)
    if get_resp.status_code == 200:
        sha = get_resp.json()["sha"]
        data["sha"] = sha  # если есть, добавляем SHA для обновления

    # Отправляем PUT-запрос для создания/обновления файла
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in (200, 201):
        print("✅ Коммит успешно создан!")
    else:
        print(f"⚠️ Ошибка: {response.status_code} {response.text}")
