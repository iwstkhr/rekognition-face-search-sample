import argparse
import os
import uuid
from time import sleep

from PIL import Image

from lib import image_util, rekognition


def detect_faces(path: str) -> dict:
    with open(path, mode='rb') as f:
        return rekognition.detect_faces(f.read())


def search_faces(collection_id: str, path: str) -> list[Image.Image]:
    faces = detect_faces(path)
    search_image = image_util.load_image(path)
    results = []

    for face in faces['FaceDetails']:
        cropped_face = image_util.crop_by_bounding_box(search_image, face['BoundingBox'])
        matches = rekognition.search_faces_by_image(
            collection_id,
            image_util.convert_image_to_bytes(cropped_face)
        ).get('FaceMatches', [])

        for match in matches:
            face = match['Face']
            result_image = image_util.load_image(os.path.join('./images/portraits', face['ExternalImageId']))
            result_image = image_util.draw_bounding_box(result_image, face['BoundingBox'])
            result_image = image_util.paste_image_on_upper_left(cropped_face, result_image)
            results.append(result_image)

        sleep(0.1)

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection-id', required=True)
    parser.add_argument('images', nargs='+')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    collection_id = args.collection_id
    searched_faces = []

    for image in args.images:
        searched_faces.extend(search_faces(collection_id, image))

    if searched_faces:
        os.makedirs('./images/results', exist_ok=True)
        for searched_face in searched_faces:
            searched_face.save(f'./images/results/{uuid.uuid4()}.png', format='PNG')
    else:
        print('No faces are found in the specified Rekognition face collection.')


if __name__ == '__main__':
    main()
