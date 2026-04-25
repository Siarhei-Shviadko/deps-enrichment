from uuid import uuid4

import pytest
from fastapi import FastAPI
from pytest_factoryboy import register
from starlette.testclient import TestClient

from deps_enrichment import api
from deps_enrichment.entrypoint import create_fastapi
from deps_enrichment.infrastructure.access_management.context_vars import user

from .factories import *


@pytest.fixture(scope="session")
def app() -> FastAPI:
    fastapi_app = create_fastapi()
    yield fastapi_app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def session_containers(app):
    return app.containers


@pytest.fixture
def containers(session_containers):
    with session_containers.reset_singletons() as containers:
        yield containers


@pytest.fixture
def repositories(containers):
    return containers.repositories


@pytest.fixture
def test_command_channel():
    return None


@pytest.fixture
def tenant():
    return uuid4().hex


@pytest.fixture
def this_user(tenant):
    return dict(
        subject="Test",
        groups=[tenant],
        token="token",
        roles=[],
        organisation=tenant,
    )


@pytest.fixture(autouse=True)
def set_this_user(this_user):
    user.set(this_user)


@pytest.fixture(autouse=True)
def mocked_middleware(monkeypatch, mocker):
    monkeypatch.setattr(api.auth, "set_user_from_token", mocker.Mock({}))


register(EntityIdFactory)
register(CodeFactory)
register(TenantIdFactory)
register(ExtraDataFactory)
register(SupplementFactory)
register(ExtraFieldFactory)
