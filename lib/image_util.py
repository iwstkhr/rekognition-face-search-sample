import io

from PIL import Image, ImageDraw


def load_image(path: str) -> Image.Image:
    """ Load an image.

    Args:
        path (str): An image path

    Returns:
        PIL.Image.Image: A loaded image
    """

    return Image.open(path)


def crop_by_bounding_box(image: Image.Image, bounding_box: dict) -> Image.Image:
    """ Crop an image by a bounding box returned from Amazon Rekognition.

    Args:
        image (PIL.Image.Image): An image
        bounding_box (dict): A bounding box

    Returns:
        PIL.Image.Image: A cropped image
    """

    image_width, image_height = image.size
    left, top, width, height = convert_bounding_box_to_rect(bounding_box, image_width, image_height)
    return image.crop((left, top, left + width, top + height))


def convert_image_to_bytes(image: Image.Image, format='PNG') -> bytes:
    """ Convert an image to bytes.

    Args:
        image (PIL.Image.Image): An image
        format (str): Image format after converting

    Returns:
        bytes: Converted image bytes
    """

    image_bytes = io.BytesIO()
    image.save(image_bytes, format=format)
    return image_bytes.getvalue()


def convert_bounding_box_to_rect(bounding_box: dict, width: int, height: int) -> (float, float, float, float):
    """ Convert a bounding box returned from Amazon Rekognition to a rect.

    Args:
        bounding_box (dict): A bounding box
        width (int): Image width
        height (int): Image height

    Returns:
        tuple (float, float, float, float): Left, Top, Width, Height
    """

    left = width * bounding_box['Left']
    top = height * bounding_box['Top']
    width = width * bounding_box['Width']
    height = height * bounding_box['Height']
    return left, top, width, height


def draw_bounding_box(image: Image.Image, bounding_box: dict) -> Image.Image:
    """ Draw a bounding box returned from Amazon Rekognition on an image.

    Args:
        image (PIL.Image.Image): An image
        bounding_box (dict): A bounding box

    Returns:
        PIL.Image.Image: A new image
    """

    new_image = image.copy()
    draw = ImageDraw.Draw(new_image)
    image_width, image_height = new_image.size
    left, top, width, height = convert_bounding_box_to_rect(bounding_box, image_width, image_height)
    draw.rectangle((left, top, left + width, top + height), outline=(200, 0, 0), width=4)
    return new_image


def paste_image_on_upper_left(image: Image.Image, canvas: Image.Image) -> Image.Image:
    """ Paste an image on upper left (10, 10) of a canvas.

    Args:
        image (PIL.Image.Image): An image to be pasted
        canvas (PIL.Image.Image): A canvas

    Returns:
        PIL.Image.Image: A new image
    """

    new_image = image.copy()
    new_image.thumbnail(size=(128, 128))
    new_canvas = canvas.copy()
    new_canvas.paste(new_image, (10, 10))
    return new_canvas
