import argparse
import os
from time import sleep

from lib import rekognition


def index_faces(collection_id: str, path: str) -> dict:
    with open(path, mode='rb') as f:
        return rekognition.index_faces(collection_id, f.read(), os.path.basename(path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection-id', required=True)
    parser.add_argument('images', nargs='+')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    collection_id = args.collection_id

    rekognition.create_collection(collection_id)

    for image in args.images:
        index_faces(collection_id, image)
        sleep(0.1)


if __name__ == '__main__':
    main()
