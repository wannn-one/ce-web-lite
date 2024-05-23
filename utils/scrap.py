import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

os.makedirs('images', exist_ok=True)

def download_image(url, folder):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {url}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url} - {e}")

base_url = "https://www.its.ac.id/komputer/id/dosen-staf/dosen/" # tinggal ganti urlnya

response = requests.get(base_url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            full_img_url = urljoin(base_url, img_url)
            download_image(full_img_url, 'images')
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
