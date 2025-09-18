import requests
import os

def download_image(url, filename):
    folder = os.path.join("assets", "portraits")
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, filename)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
        else:
            print(f"Не вдалося завантажити {url}")
    except Exception as e:
        print(f"Помилка при завантаженні {url}: {e}")
    return path
