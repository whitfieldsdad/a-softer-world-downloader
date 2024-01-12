import json
import logging
import click
from a_softer_world.client import Client
from a_softer_world.constants import CACHE_DIR, DEFAULT_FILENAME_POLICY, MIN_COMIC_ID, MAX_COMIC_ID, FILENAME_POLICIES
from a_softer_world.json_serializer import JSONEncoder


@click.command()
@click.option("--output-dir", "-o", help="If provided, download comics to this directory, otherwise list comic metadata")
@click.option('--cache-dir', '-c', default=CACHE_DIR, show_default=True, help='Directory to cache comic metadata')
@click.option('--name-by', '-n', 'filename_policy', type=click.Choice(FILENAME_POLICIES), default=DEFAULT_FILENAME_POLICY, show_default=True, help='Naming policy for downloaded comics',)
@click.option('--min-comic-id', type=int, default=MIN_COMIC_ID, show_default=True, help='Minimum comic ID to download (e.g. 1)')
@click.option('--max-comic-id', type=int, default=MAX_COMIC_ID, show_default=True, help='Maximum comic ID to download (e.g. 1)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--clean-cache', is_flag=True, help='Clean the metadata cache')
def main(
    output_dir: str,
    cache_dir: str, 
    filename_policy: str,
    min_comic_id: int,
    max_comic_id: int,
    verbose: bool,
    clean_cache: bool) -> None:

    configure_logging(verbose)

    client = Client(
        cache_dir=cache_dir, 
        filename_policy=filename_policy,
    )
    if clean_cache:
        client.clean_comic_metadata_cache()

    if output_dir:
        client.download_comics(output_dir, min_comic_id=min_comic_id, max_comic_id=max_comic_id)
    else:
        for comic in client.iter_comics(min_comic_id=min_comic_id, max_comic_id=max_comic_id):
            print(json.dumps(comic, cls=JSONEncoder))


def configure_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(message)s')


if __name__ == "__main__":
    main()
