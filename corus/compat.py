
import sys


PY2 = sys.version_info.major == 2


def patch_tar_file(file):
    #  30     file = tar.extractfile(member)
    #  31 --> yield TextIOWrapper(file, encoding)
    # AttributeError: 'ExFileObject' object has no attribute 'readable'

    file.readable = lambda: True
    file.writable = lambda: False
    file.seekable = lambda: True
    file.read1 = file.read
