import pytest
import django
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def configure_django():
    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=["django.contrib.contenttypes"],
            DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
        )
        django.setup()
