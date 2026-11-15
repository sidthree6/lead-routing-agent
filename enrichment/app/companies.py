"""Dummy company records keyed by domain.

All companies are invented. Domains use the reserved .example TLD so none can
belong to a real business. Records are chosen to hit the routing thresholds
(SMB < 2,000 monthly orders, Mid-market 2,000-20,000, Enterprise > 20,000)
and a few awkward cases.
"""

COMPANIES: dict[str, dict] = {
    # SMB, well inside the band.
    "tinyloom.example": {
        "company_name": "Tiny Loom",
        "industry": "Ecommerce - home textiles",
        "store_platform": "Shopify",
        "monthly_orders": 450,
        "employees": 6,
    },
    # SMB, one below the Mid-market threshold.
    "harborandpine.example": {
        "company_name": "Harbor & Pine",
        "industry": "Ecommerce - outdoor gear",
        "store_platform": "WooCommerce",
        "monthly_orders": 1999,
        "employees": 14,
    },
    # Mid-market, exactly on the lower threshold.
    "copperleaf.example": {
        "company_name": "Copperleaf Tea Co.",
        "industry": "Ecommerce - food and drink",
        "store_platform": "Shopify",
        "monthly_orders": 2000,
        "employees": 25,
    },
    # Mid-market, well inside the band.
    "northgale.example": {
        "company_name": "Northgale Supply",
        "industry": "Ecommerce - apparel",
        "store_platform": "BigCommerce",
        "monthly_orders": 8500,
        "employees": 60,
    },
    # Mid-market, exactly on the upper threshold.
    "velvetfern.example": {
        "company_name": "Velvet Fern Beauty",
        "industry": "Ecommerce - cosmetics",
        "store_platform": "Shopify Plus",
        "monthly_orders": 20000,
        "employees": 140,
    },
    # Enterprise, one above the threshold.
    "stonebridgeoutfitters.example": {
        "company_name": "Stonebridge Outfitters",
        "industry": "Ecommerce - footwear",
        "store_platform": "Salesforce Commerce Cloud",
        "monthly_orders": 20001,
        "employees": 310,
    },
    # Enterprise, well inside the band.
    "orbitmart.example": {
        "company_name": "OrbitMart",
        "industry": "Ecommerce - marketplace",
        "store_platform": "Adobe Commerce",
        "monthly_orders": 150000,
        "employees": 1200,
    },
    # Known company with no order volume: exercises the missing-field path.
    "quietharbor.example": {
        "company_name": "Quiet Harbor Candles",
        "industry": "Ecommerce - home fragrance",
        "store_platform": "Squarespace",
        "monthly_orders": None,
        "employees": 4,
    },
    # A helpdesk vendor: a competitor, so not a fit.
    "ticketnest.example": {
        "company_name": "TicketNest",
        "industry": "Software - customer support",
        "store_platform": None,
        "monthly_orders": None,
        "employees": 85,
    },
}
