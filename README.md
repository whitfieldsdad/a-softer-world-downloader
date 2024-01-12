# Download every comic from ['A Softer World'](http://www.asofterworld.com/)

A Python 3 library for downloading every comic from [A Softer World](http://www.asofterworld.com/).

![didn't even bring lunch that day.](data/images/cassandra.jpg)
![even after we're done](data/images/camping.jpg)

## Table of contents

- [Features](#features)
- [Usage](#usage)
    - [Command line interface](#command-line-interface)
        - [Downloading all comics](#downloading-all-comics)
        - [Listing comics](#listing-comics)
        - [Listing metadata about specific comics](#listing-metadata-about-specific-comics)
        - [Listing the alt text of every comic](#listing-the-alt-text-of-every-comic)
        - [Listing the download URLs for every comic](#listing-the-download-urls-for-every-comic)
    - [Python](#python)
        - [Retrieving comic metadata with Python](#retrieving-comic-metadata-with-python)
        - [Downloading one comic with Python](#downloading-one-comic-with-python)
        - [Downloading multiple comics with Python](#downloading-multiple-comics-with-python)
        - [Downloading all comics with Python](#downloading-all-comics-with-python)
        - [Get the alt text of every comic with Python](#get-the-alt-text-of-every-comic-with-python)

## Features

- Download every comic
- List metadata about every comic in JSONL format (archives in [JSON](data/comics.json), [JSONL](data/comics.jsonl) and [CSV](data/comics.csv) format have also been included in the [data](data) directory of this repository)
- Automatically caches comic metadata to a customizable directory to avoid unnecessary network calls and improve performance

## Usage

This project uses [Poetry](https://python-poetry.org/) for dependency management. 

To install the project's dependencies, run:

```bash
poetry install
```

### Command line interface

```bash
poetry run client --help
```

```text
Usage: client [OPTIONS]

Options:
  -o, --output-dir TEXT        If provided, download comics to this directory,
                               otherwise list comic metadata
  -c, --cache-dir TEXT         Directory to cache comic metadata  [default: /v
                               ar/folders/px/d9nhhv0144g2n9yjs36k6wgw0000gn/T/
                               468948a3-b1ec-4c54-bb2d-3ca61ab8057e]
  -n, --name-by [filename|id]  Naming policy for downloaded comics  [default:
                               filename]
  --min-comic-id INTEGER       Minimum comic ID to download (e.g. 1)
                               [default: 1]
  --max-comic-id INTEGER       Maximum comic ID to download (e.g. 1)
                               [default: 1248]
  -v, --verbose                Enable verbose logging
  --clean-cache                Clean the metadata cache
  --help                       Show this message and exit.
```

#### Downloading all comics

To download all comics, run:

```bash
poetry run client -o data/
```

By default, comics will be named according to their filename.

To name comics according to their ID, run:

```bash
poetry run client -o data/ --name-by=id
```

#### Listing comics

To list metadata about every comic, run:

```bash
poetry run client
```

```json
"id": 1, "url": "http://www.asofterworld.com/index.php?id=1", "filename": "myparents.jpg", "img": "https://www.asofterworld.com/clean/myparents.jpg", "alt": "Are my parents ever coming home?"}
{"id": 2, "url": "http://www.asofterworld.com/index.php?id=2", "filename": "babydoom.jpg", "img": "https://www.asofterworld.com/clean/babydoom.jpg", "alt": "There had to be an answer"}
{"id": 3, "url": "http://www.asofterworld.com/index.php?id=3", "filename": "softerworld.jpg", "img": "https://www.asofterworld.com/clean/softerworld.jpg", "alt": "what I did for love"}
...
```

If you'd like the output to be indented, pipe the output to [`jq`](https://github.com/jqlang/jq):

```bash
poetry run client | jq
```

Or, if you'd prefer JSONL, but just want syntax highlighting:

```bash
poetry run client | jq -c
```

#### Listing metadata about specific comics

Since the output is in JSONL format, you can use the `grep` + `jq` [wombo combo](https://www.ssbwiki.com/Wombo_Combo) to filter the output:

```bash
poetry run client | grep camping.jpg | jq
```

```json
{
  "id": 194,
  "url": "http://www.asofterworld.com/index.php?id=194",
  "filename": "camping.jpg",
  "img": "https://www.asofterworld.com/clean/camping.jpg",
  "alt": "even after we're done"
}
```

It's hard to beat `grep` over JSONL files.

#### Listing the alt text of every comic

To list [the alt text of every comic](data/alt.txt), run:

```bash
poetry run client | jq -r '.alt' | sort
```

```text
...
Let's be the quiet realization that our time has passed.
Let's break the curse.
Let's do something wrong.
Let's join a street gang! Is NASA recruiting?
Let's use that against them.
Let's void some warranties, my love.
Little things are important too.
Live every day like the ice cream store is closing.
Live free or die soft
...
```

#### Listing the download URLs for every comic

To list [the download URLs for every comic](data/urls.txt), run:

```bash
poetry run client | jq -r '.img' | sort
```

### Python

This library is also designed to be used as a library!

#### Retrieving comic metadata with Python

```python
from a_softer_world.client import Client

import dataclasses

client = Client()
meta = client.get_comic_metadata(194)

print(dataclasses.asdict(meta))
```

```text
{'id': 194, 'url': 'http://www.asofterworld.com/index.php?id=194', 'filename': 'camping.jpg', 'img': 'https://www.asofterworld.com/clean/camping.jpg', 'alt': "even after we're done"}
```

#### Downloading one comic with Python

To download [comic #194](https://www.asofterworld.com/index.php?id=194) to the current working directory:

```python
from a_softer_world.client import Client

import os

client = Client()
client.download_comic(194, os.getcwd())
```

#### Downloading multiple comics with Python

To download comics [#1](https://www.asofterworld.com/index.php?id=1) through [#10](https://www.asofterworld.com/index.php?id=10) to the current working directory:

```python
from a_softer_world.client import Client

import os

client = Client()
client.download_comics(min_comic_id=1, max_comic_id=10, output_dir=os.getcwd())
```

#### Downloading all comics with Python

To download every comic to the current working directory:

```python
from a_softer_world.client import Client

import os

client = Client()
client.download_comics(output_dir=os.getcwd())
```

#### Get the alt text of every comic with Python

A Softer World features some pretty interesting [alt text](data/alt.txt).

You can create a list containing all alt text as follows:

```python
from a_softer_world.client import Client

client = Client()
alt_text = sorted([meta.alt for meta in client.iter_comics()])
for alt in alt_text:
    print(alt)
```

```text
...
we should have taken flying lessons instead of flamenco.
we will have a spare room again, and mankind is safe!
we'll need to find you a new pet name i guess
we're hiring, sure. but this job won't save you.
we're just getting started.
we've been good, but we can't last
...
```

To create a map between alt text and filenames:

```python
from a_softer_world.client import Client

import json

client = Client()
comics = client.iter_comics()

alt_to_filename = {meta.alt: meta.filename for meta in comics}
print(json.dumps(alt_to_filename, indent=2))
```

```json
{
  ...
  "be the goblin you want to see in the world": "dress.jpg",
  "we don't need words": "empty.jpg",
  "The Earth is better off without humans, too, but here we are.": "drastic.jpg",
  "the heroes we deserve.": "chickens.jpg",
  "How do you say goodbye to someone who was never there?": "ruby.jpg"
}
```
