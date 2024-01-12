import os
import tempfile

# Where to cache comic metadata to avoid repeated lookups
CACHE_DIR = os.path.join(tempfile.gettempdir(), "468948a3-b1ec-4c54-bb2d-3ca61ab8057e")

# A Softer World has ended, and therefore the range of available comics is static
MIN_COMIC_ID, MAX_COMIC_ID = 1, 1248

URL_TEMPLATE = "http://www.asofterworld.com/index.php?id={comic_id}"

# How to name downloaded comics
FILENAME = 'filename'
ID = 'id'

FILENAME_POLICIES = [
    FILENAME,
    ID,
]
DEFAULT_FILENAME_POLICY = FILENAME
