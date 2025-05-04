import os
from datetime import datetime
from typing import Literal, Tuple
from urllib.parse import urlparse

import httpx
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()
api_base = os.getenv("OPENAI_API_BASE_URL")
api_key = os.getenv("OPENAI_API_KEY")

__IMAGES_BASE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/images')
os.makedirs(__IMAGES_BASE_FOLDER, exist_ok=True)

client = OpenAI(
    base_url=api_base,
    api_key=api_key,
)

def get_all_images() -> pd.DataFrame:
    image_files = [f for f in os.listdir(__IMAGES_BASE_FOLDER) if f.endswith('.png')]
    records = []
    for image_file in image_files:
        image_path = os.path.join(__IMAGES_BASE_FOLDER, image_file)
        txt_file = image_file.replace('.png', '.txt')
        txt_path = os.path.join(__IMAGES_BASE_FOLDER, txt_file)
        description = ""
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                description = f.read()
        created_time = datetime.fromtimestamp(os.path.getctime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
        records.append({"Image": image_path, "Description": description, "Date Created": created_time})
    return pd.DataFrame(records)

def delete_image(image_path: str):
    if os.path.exists(image_path):
        os.remove(image_path)
    txt_path = image_path.replace('.png', '.txt')
    if os.path.exists(txt_path):
        os.remove(txt_path)

def generate_image(
    prompt: str,
    model: str = "dall-e-3",
    style: Literal["vivid", "natural"] = "vivid",
    quality: Literal["standard", "hd"] = "hd",
    timeout: int = 100,
    size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024"
) -> Tuple[str, str]:

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        style=style,
        n=1
    )

    image_url = response.data[0].url
    filename = _extract_filename_from_url(image_url)
    image_path = os.path.join(__IMAGES_BASE_FOLDER, filename)

    with httpx.Client(timeout=timeout) as http_client:
        img_response = http_client.get(image_url)
        with open(image_path, 'wb') as f:
            f.write(img_response.content)

    prompt_txt_path = image_path.replace('.png', '.txt')
    with open(prompt_txt_path, 'w') as f:
        f.write(prompt)

    return prompt, image_path

def _extract_filename_from_url(url: str) -> str:
    path = urlparse(url).path
    return os.path.basename(path)
