from .storage import S3SessionStorage, make_storages
from importlib.metadata import version, PackageNotFoundError

__all__ = ["S3SessionStorage", "make_storages"]

try:
    __version__ = version("django-s3-session-storage")
except PackageNotFoundError:  # when running from source, before installation
    __version__ = "0.0.0"