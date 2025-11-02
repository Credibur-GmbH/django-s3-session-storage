import boto3
from django_s3_session_storage import S3SessionStorage


def test_external_session_is_used():
    session = boto3.Session(region_name="us-west-2")
    s = S3SessionStorage(bucket_name="test-bucket", region_name="us-west-2", session=session)
    assert s._create_session() is session


def test_default_session_created_when_none_provided():
    s = S3SessionStorage(bucket_name="test-bucket", region_name="us-east-1")
    session = s._create_session()
    assert isinstance(session, boto3.Session)
    assert session.region_name == "us-east-1"


def test_session_region_validation_warns(monkeypatch):
    session = boto3.Session(region_name="us-west-1")
    s = S3SessionStorage(bucket_name="test-bucket", region_name="us-east-1", session=session)

    with monkeypatch.context() as m:
        warn_called = False

        def mock_warn(message, stacklevel=2):
            nonlocal warn_called
            warn_called = True
            assert "does not match storage region" in message

        m.setattr("warnings.warn", mock_warn)
        s._validate_session_region(session)
        assert warn_called
