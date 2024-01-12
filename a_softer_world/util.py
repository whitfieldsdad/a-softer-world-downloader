from typing import Dict
import logging
import os
import shutil
import concurrent.futures
import requests

logger = logging.getLogger(__name__)


def download_files(downloads: Dict[str, str]) -> None:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url, path in downloads.items():
            if not os.path.exists(path):
                future = executor.submit(download_file, url, path)
                futures.append(future)
        
        if futures:
            for future in concurrent.futures.as_completed(futures):
                future.result()


def download_file(url: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
