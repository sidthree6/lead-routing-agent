"""Tests for the mock enrichment API."""

import pytest
from fastapi.testclient import TestClient

from app.companies import COMPANIES
from app.main import Company, app

client = TestClient(app)


def test_health() -> None:
    """Health endpoint answers ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_known_domain_returns_company() -> None:
    """A known domain returns its full record."""
    response = client.get("/company/northgale.example")
    assert response.status_code == 200
    assert response.json() == {
        "domain": "northgale.example",
        "company_name": "Northgale Supply",
        "industry": "Ecommerce - apparel",
        "store_platform": "BigCommerce",
        "monthly_orders": 8500,
        "employees": 60,
    }


@pytest.mark.parametrize("raw", ["NorthGale.EXAMPLE", "www.northgale.example", "northgale.example."])
def test_domain_is_normalized(raw: str) -> None:
    """Case, a leading www. and a trailing dot do not affect the lookup."""
    response = client.get(f"/company/{raw}")
    assert response.status_code == 200
    assert response.json()["domain"] == "northgale.example"


def test_unknown_domain_returns_404() -> None:
    """A well-formed domain not in the dataset is a 404 with a readable detail."""
    response = client.get("/company/unknown-brand.example")
    assert response.status_code == 404
    assert response.json() == {"detail": "company not found: unknown-brand.example"}


@pytest.mark.parametrize("raw", ["not a domain", "localhost", "foo..example", "-bad.example"])
def test_malformed_domain_returns_422(raw: str) -> None:
    """Strings that are not hostnames are rejected before lookup."""
    response = client.get(f"/company/{raw}")
    assert response.status_code == 422


def test_missing_fields_are_null() -> None:
    """Unknown values come back as null, not as zero or a missing key."""
    body = client.get("/company/quietharbor.example").json()
    assert body["monthly_orders"] is None


@pytest.mark.parametrize("domain", sorted(COMPANIES))
def test_every_fixture_matches_schema(domain: str) -> None:
    """Every record in the dataset validates against the response model."""
    Company(domain=domain, **COMPANIES[domain])


def test_fixtures_cover_threshold_values() -> None:
    """The dataset includes the exact routing boundaries the eval relies on."""
    orders = {c["monthly_orders"] for c in COMPANIES.values()}
    assert {1999, 2000, 20000, 20001, None} <= orders
