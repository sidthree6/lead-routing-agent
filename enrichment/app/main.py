"""Mock enrichment API: look up dummy company data by domain."""

import re
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

from app.companies import COMPANIES

# Hostname labels separated by dots, ending in an alphabetic TLD. Checked after
# normalising, so "WWW.Example.COM" is accepted.
DOMAIN_RE = re.compile(r"(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}")

app = FastAPI(title="Mock enrichment API", version="0.1.0")


class Company(BaseModel):
    """Firmographic data for one company. None means the field is unknown."""

    domain: str
    company_name: str
    industry: str
    store_platform: str | None
    monthly_orders: int | None
    employees: int | None


def normalize_domain(raw: str) -> str:
    """Lowercase, trim, and drop a leading "www." and trailing dot."""
    return raw.strip().lower().rstrip(".").removeprefix("www.")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check for Docker and n8n."""
    return {"status": "ok"}


@app.get("/company/{domain}", responses={404: {"description": "Unknown domain"}})
def get_company(domain: Annotated[str, Path(max_length=253)]) -> Company:
    """Return dummy company data, 404 for an unknown domain, 422 for a malformed one."""
    normalized = normalize_domain(domain)
    if not DOMAIN_RE.fullmatch(normalized):
        raise HTTPException(status_code=422, detail=f"invalid domain: {domain!r}")
    record = COMPANIES.get(normalized)
    if record is None:
        raise HTTPException(status_code=404, detail=f"company not found: {normalized}")
    return Company(domain=normalized, **record)
