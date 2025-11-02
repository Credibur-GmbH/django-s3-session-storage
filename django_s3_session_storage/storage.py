import boto3
import warnings
from typing import Optional
from storages.backends.s3 import S3Storage


class S3SessionStorage(S3Storage):
    def __init__(self, *, session: Optional[boto3.Session] = None, **kwargs):
        self.region_name: Optional[str] = None
        self._external_session: Optional[boto3.Session] = session
        super().__init__(**kwargs)

    def _create_session(self) -> boto3.Session:
        """Create or return an existing boto3.Session, reusing an injected one if provided."""
        if self._external_session:
            self._validate_session_region(self._external_session)
            return self._external_session

        if not hasattr(self, "_cached_session"):
            self._cached_session = boto3.Session(region_name=self.region_name)
        return self._cached_session

    def _validate_session_region(self, session: boto3.Session) -> None:
        if not self.region_name:
            return
        if session.region_name and session.region_name != self.region_name:
            warnings.warn(
                f"{self.__class__.__name__}: Provided session region "
                f"({session.region_name}) does not match storage region ({self.region_name}).",
                stacklevel=2,
            )


def make_storages(bucket_name: str, region_name: str, session: Optional[boto3.Session] = None) -> dict:
    """Convenience helper to build a Django STORAGES entry for S3 storage."""
    return {
        "BACKEND": f"django_s3_session_storage.{S3SessionStorage.__name__}",
        "OPTIONS": {
            "bucket_name": bucket_name,
            "region_name": region_name,
            "session": session,
        },
    }