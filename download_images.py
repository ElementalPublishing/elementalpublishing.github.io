import os
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_images(url, output_folder="downloaded_images"):
    os.makedirs(output_folder, exist_ok=True)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")
    for img in img_tags:
        img_url = img.get("src")
        if not img_url:
            continue
        img_url = str(img_url)
        if img_url.startswith("data:"):
            # Skip data URLs
            continue
        img_url = urljoin(url, img_url)
        # Create a unique filename using a hash of the full image URL
        url_hash = hashlib.md5(img_url.encode('utf-8')).hexdigest()
        ext = os.path.splitext(urlparse(img_url).path)[1] or '.img'
        img_name = f"{url_hash}{ext}"
        img_path = os.path.join(output_folder, img_name)
        if os.path.exists(img_path):
            print(f"Already exists, skipping: {img_name}")
            continue
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                img_data = requests.get(img_url, timeout=10).content
                with open(img_path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded: {img_url} -> {img_name}")
                break
            except Exception as e:
                print(f"Attempt {attempt} failed: {img_url} ({e})")
                if attempt == max_retries:
                    print(f"Giving up on: {img_url}")

if __name__ == "__main__":
    url = input("Enter the website URL: ")
    download_images(url)
