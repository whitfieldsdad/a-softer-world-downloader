# Download every comic from ['A Softer World'](http://www.asofterworld.com/)

A Python 3 library for downloading every comic from [A Softer World](http://www.asofterworld.com/).

![didn't even bring lunch that day.](data/images/cassandra.jpg)
![even after we're done](data/images/camping.jpg)





## Features

- Download every comic
- List metadata about every comic in JSONL format (archives in [JSON](data/comics.json), [JSONL](data/comics.jsonl) and [CSV](data/comics.csv) format have also been included in the [data](data) directory of this repository)

## Usage

This project uses [Poetry](https://python-poetry.org/) for dependency management. 

To install the project's dependencies, run:

```bash
poetry install
```

### Command line interface

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
