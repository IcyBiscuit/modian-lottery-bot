import sys
import pathlib


def setup():
    BASE_PATH = pathlib.Path(__file__).parent.parent
    base_path = BASE_PATH.absolute().as_posix()
    sys.path.append(base_path)
