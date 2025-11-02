# django-s3-session-storage

A lightweight Django storage backend for Amazon S3 that supports **shared `boto3.Session` reuse** and **dependency injection** —  
designed to **eliminate latency spikes from repeated IAM credential fetching** on every file access.

---

## ⚡ Why?

When using [`django-storages`](https://github.com/jschneier/django-storages), each new instance of `S3Storage` internally creates a new `boto3.Session`.  
This triggers fresh IAM credential resolution (via EC2/ECS metadata or STS), which can add **tens to hundreds of milliseconds** of latency per request —  
especially when accessing S3-backed `FileField` or `ImageField` objects frequently.

**`django-s3-session-storage`** solves this by allowing you to inject or share a single, cached `boto3.Session`,  
so IAM tokens are fetched once and reused across all storage operations.

Result:  
✅ Consistent response times  
✅ Fewer network round trips to AWS metadata endpoints  
✅ Simpler dependency injection for testing and configuration

---

## 🚀 Features

- 🔁 Reuses a shared `boto3.Session` across all S3 operations
- ⚙️ Supports dependency injection for clean app design
- 🧠 Drop-in replacement for `storages.backends.s3.S3Storage`
- ⚡ Eliminates repeated IAM token lookups, reducing S3 latency
- 🧪 Fully tested, type-annotated, and dependency-light

---

## 📦 Installation

```bash
pip install django-s3-session-storage
```

or with **uv**:

```bash
uv add django-s3-session-storage
```

---

## ⚙️ Usage

In your **Django settings**:

```python
import boto3
from django_s3_session_storage import make_storages

BOTO3_SESSION = boto3.Session(region_name="eu-central-1")

STORAGES = {
    "default": make_storages(
        bucket_name="my-bucket",
        region_name="eu-central-1",
        session=BOTO3_SESSION,  # optional
    ),
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
```

`S3SessionStorage` will reuse your provided session,  
or lazily create one if none is given.

---

## 🧠 Example: Direct instantiation

```python
from django_s3_session_storage import S3SessionStorage
import boto3

session = boto3.Session(region_name="us-east-1")
storage = S3SessionStorage(bucket_name="example-bucket", region_name="us-east-1", session=session)
```

---

## 🧪 Running Tests

```bash
uv sync --dev
pytest
```

Minimal Django settings are auto-configured in `tests/conftest.py`.

---

## 🧰 API Reference

### `S3SessionStorage`

Subclass of `storages.backends.s3.S3Storage` that reuses an injected or cached `boto3.Session`.

#### Constructor:
```python
S3SessionStorage(
    *,
    session: Optional[boto3.Session] = None,
    **kwargs
)
```

- `session`: Optional preconfigured `boto3.Session`.  
  If not provided, one is created lazily from the `region_name`.

---

### `make_storages(bucket_name, region_name, session=None)`

Helper for building a single Django `STORAGES` entry.

Returns:
```python
{
    "BACKEND": "django_s3_session_storage.S3SessionStorage",
    "OPTIONS": { ... }
}
```

---

## 🧾 License
MIT License © 2025 Credibur GmbH  
Developed and maintained by the engineering team at [Credibur GmbH](https://github.com/Credibur-GmbH).

---


## 🔗 Links

[//]: # (TODO: Update links)
[//]: # (- 📘 [Documentation]&#40;https://github.com/yourname/django-s3-session-storage#readme&#41;)
[//]: # (- 💻 [Source Code]&#40;https://github.com/yourname/django-s3-session-storage&#41;)

- 🧪 [django-storages](https://github.com/jschneier/django-storages)