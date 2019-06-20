import os
from PIL import Image
from PIL import ImageChops

_CUR_DIR = os.path.dirname(os.path.abspath(__file__))

REF_DATA_FOLDER = os.path.join(_CUR_DIR, "test_data")
TEST_RESULTS_FOLDER = os.path.join(_CUR_DIR, "test_results")


def assert_images_equal(path_one, path_two):
    """Use pill to compare images"""
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
    diff = ImageChops.difference(image_one, image_two)
    # diff.show()
    assert diff.getbbox() is None, "Images differ: %s != %s" % (path_one, path_two)
