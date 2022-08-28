import boto3
from botocore.exceptions import ClientError

client = boto3.client('rekognition')


def create_collection(collection_id: str) -> dict or None:
    """ Create an Amazon Rekognition face collection.

    Args:
        collection_id (str): A face collection name

    Returns:
        dict or None: A response of create_collection API
                      If the specified collection name already exists, None will be returned.
    """

    try:
        return client.create_collection(CollectionId=collection_id)

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            # Return None when the specified face collection already exists.
            return None
        else:
            raise e


def index_faces(collection_id: str, image_bytes: bytes, external_image_id: str, max_faces: int = 100) -> dict:
    """ Index faces in an image.

    Args:
        collection_id (str): A face collection name
        image_bytes (bytes): Image bytes
        external_image_id (str): An external image id of an Amazon Rekognition face collection
        max_faces (int): A face count to be detected

    Returns:
        dict: A response of index_faces API
    """

    return client.index_faces(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes},
        ExternalImageId=external_image_id,
        MaxFaces=max_faces,
        QualityFilter='AUTO',
        DetectionAttributes=['DEFAULT']
    )


def search_faces_by_image(collection_id: str, image_bytes: bytes, threshold: int = 80, max_faces: int = 1) -> dict:
    """ Search for faces by an image.

    Args:
        collection_id (str): A face collection name
        image_bytes (bytes): Image bytes
        threshold (int): A threshold to be matched
        max_faces (int): A face count to be searched for

    Returns:
        dict: A response of search_faces_by_image API
    """

    try:
        return client.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes},
            FaceMatchThreshold=threshold,
            MaxFaces=max_faces
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidParameterException':
            # Return an empty dict when no faces were detected in an image.
            return {}
        else:
            raise e


def detect_faces(image_bytes: bytes) -> dict:
    """ Detect faces in image bytes.

    Args:
        image_bytes (bytes): Image bytes

    Returns:
        dict: A response of detect_faces API
    """

    return client.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['DEFAULT']
    )
