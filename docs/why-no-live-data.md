# Why v0.1.0 has no live-data adapter

Live fish prices, freight, foreign exchange, tariffs and tax rules change on different schedules and often carry licensing, contract or jurisdictional constraints. Automatically fetching them would create four new risks:

1. stale data presented as current;
2. mismatched route, quantity, service or product scope;
3. redistribution or credential exposure;
4. an API response being mistaken for legal or commercial confirmation.

v0.1.0 therefore keeps data acquisition outside the calculation core. Future adapters must provide provenance, retrieval time, validity, licensing status, cache policy and a human approval boundary before their values enter a quote.
