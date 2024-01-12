import json
import os
import shutil
from typing import Iterator, Optional
from a_softer_world.json_serializer import JSONEncoder
from a_softer_world import util
import bs4
import logging
import requests
import concurrent.futures
from dataclasses import dataclass
from a_softer_world.constants import DEFAULT_FILENAME_POLICY, FILENAME, ID, MIN_COMIC_ID, MAX_COMIC_ID, URL_TEMPLATE, CACHE_DIR

logger = logging.getLogger(__name__)


@dataclass()
class Comic:
    id: str
    url: str
    filename: str
    img: str
    alt: str

    @property
    def src(self) -> str:
        return self.img


@dataclass()
class Client:
    cache_dir: str = CACHE_DIR
    filename_policy: str = DEFAULT_FILENAME_POLICY

    def __post_init__(self):
        self.cache_dir = self.cache_dir or CACHE_DIR
        self.filename_policy = self.filename_policy or DEFAULT_FILENAME_POLICY

    def iter_comics(self, min_comic_id: int = MIN_COMIC_ID, max_comic_id: int = MAX_COMIC_ID) -> Iterator[Comic]:
        comic_ids = range(min_comic_id, max_comic_id + 1)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            comics = executor.map(self.get_comic_metadata, comic_ids)
            yield from sorted(comics, key=lambda c: c.id)
 
    def clean_comic_metadata_cache(self) -> None:
        shutil.rmtree(self.cache_dir)

    def get_comic_metadata(self, comic_id: int) -> Comic:
        m = self._read_comic_metadata(comic_id)
        if m is None:
            m = self._resolve_comic_metadata(comic_id)
            self._save_comic_metadata(m)
        return m

    def _read_comic_metadata(self, comic_id: int) -> Optional[Comic]:
        path = self._get_comic_metadata_path(comic_id)
        if os.path.exists(path):
            with open(path) as file:
                data = json.load(file)
                return Comic(**data)

    def _save_comic_metadata(self, metadata: Comic):
        path = self._get_comic_metadata_path(metadata.id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            json.dump(metadata, file, cls=JSONEncoder)

    def _get_comic_metadata_path(self, comic_id: int) -> str:
        path = os.path.join(self.cache_dir, f"{comic_id}.json")
        return path

    def _resolve_comic_metadata(self, comic_id: int) -> Comic:
        url = self.get_comic_url(comic_id)

        response = requests.get(url)
        response.raise_for_status()

        html = response.text
        soup = bs4.BeautifulSoup(html, features="html.parser")

        comic_div = soup.find("div", id="comicimg")
        img_tag = comic_div.find("img")

        img = img_tag["src"]
        filename = os.path.basename(img)
        alt = img_tag["title"]

        return Comic(
            id=comic_id,
            url=url,
            filename=filename,
            img=img,
            alt=alt,
        )

    def iter_comic_download_urls(self) -> Iterator[str]:
        for comic_id in range(MIN_COMIC_ID, MAX_COMIC_ID + 1):
            yield self.get_comic_download_url(comic_id)

    def get_comic_download_url(self, comic_id: int) -> str:
        meta = self.get_comic_metadata(comic_id)
        return meta.img

    def iter_comic_urls(self, min_comic_id: int = MIN_COMIC_ID, max_comic_id: int = MAX_COMIC_ID) -> Iterator[str]:
        for comic_id in range(min_comic_id, max_comic_id):
            yield self.get_comic_url(comic_id)

    def get_comic_url(self, comic_id: int) -> str:
        return URL_TEMPLATE.format(comic_id=comic_id)

    def download_comics(self, output_dir: str, min_comic_id: int = MIN_COMIC_ID, max_comic_id: int = MAX_COMIC_ID) -> None:
        downloads = {}
        for comic in self.iter_comics(min_comic_id=min_comic_id, max_comic_id=max_comic_id):
            url = comic.src
            if self.filename_policy == FILENAME:
                filename = comic.filename
            elif self.filename_policy == ID:
                filename = f'{comic.id}.jpg'
            else:
                raise ValueError(f"Unknown filename policy: {self.filename_policy}")
            
            path = os.path.join(output_dir, filename)
            downloads[url] = path
        
        if downloads:
            util.download_files(downloads=downloads)
