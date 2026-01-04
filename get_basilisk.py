import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://o.rthost.win/basilisk/"
INDEX_URL = f"{BASE_URL}index.php?sort=date&order=desc"

def get_latest():
    response = requests.get(INDEX_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find('div', class_='list').find('table').find('tbody').find_all('tr')

    latest = {}
    target = "basilisk52-"

    for row in rows:
        name_cell = row.find('td', class_='n')

        if not name_cell:
            continue

        link = name_cell.find('a')
        filename = link.text.strip()

        if filename.startswith(target) and filename.endswith("-xpmod.7z") and target not in latest:
            filename_attr = filename.split('-')
            wintarget = filename_attr[1].split('.')[-1]
            prefix = target + wintarget
            version = filename_attr[3]

            latest[wintarget] = {
                "prefix": prefix
                "filename": filename,
                "url": BASE_URL + filename,
                "version": version
            }

        if len(latest) == len(targets):
            break

    return latest

if __name__ == "__main__":
    meta = get_latest()
    if len(meta) < 2:
        print("Builds not found.")
        exit(1)

    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"version={meta["win32"]["version"]}\n")
            f.write(f"win32_prefix={meta["win32"]["prefix"]}\n")
            f.write(f"win32_file={meta["win32"]["filename"]}\n")
            f.write(f"win32_url={meta["win32"]["url"]}\n")
            f.write(f"win64_prefix={meta["win64"]["prefix"]}\n")
            f.write(f"win64_file={meta["win64"]["filename"]}\n")
            f.write(f"win64_url={meta["win64"]["url"]}\n")