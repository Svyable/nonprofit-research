# Jurisdiction taxonomy

Use ISO 3166-1 alpha-2 country codes as the sovereign-country base and add subnational identifiers only where the legal distinction materially changes formation, charity, tax, fundraising, or recurring obligations.

Examples of intended identifiers:

- `US` — United States federal layer
- `US-IL` — Illinois, United States
- `GB-ENG-WLS` — England and Wales as a legally meaningful combined scope
- `CA-ON` — Ontario, Canada
- `FR` — France

The identifier system is a project taxonomy, not a claim that every ID is an ISO code. Non-ISO combined or special legal scopes must be documented in `data/jurisdictions/index.yaml`.

Do not create separate packets merely for geographic convenience. Create them when a user would receive materially different legal-operational guidance.
