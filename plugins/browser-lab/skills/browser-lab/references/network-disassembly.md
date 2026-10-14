# Network Disassembly Playbook (chrome-devtools + mitmproxy)

Goal: understand exactly what a site does over the wire — its endpoints,
payloads, auth scheme, and request dependencies — so it can be reasoned about
or replicated. Read "Responsible use" in SKILL.md first; only do this on sites
the user owns or is authorized to test.

## Two layers, two tools

- **chrome-devtools** sees what *the browser* requests. Fast, zero setup, great
  for a first map of a web app's API. Limited to the browser's own traffic.
- **mitmproxy** sits *below* the browser as a TLS-intercepting proxy. It sees
  everything routed through it (including service workers, native apps, other
  clients), and can modify and replay. Use it when DevTools can't see the
  traffic or when you need interception/replay/token extraction.

Start at the DevTools layer; drop to the proxy layer when you need more.

## Fast map with chrome-devtools

1. `navigate_page`, then exercise the feature you care about (login, search,
   load more, submit).
2. `list_network_requests`; focus on `fetch`/`xhr` entries — those are the API.
3. For each interesting call, `get_network_request` to read method, URL,
   query/body, request headers (auth!), and the response shape.
4. Note the pattern: base URL, auth header (Bearer / cookie / API key), content
   type, pagination params, and which response fields feed later requests.

## Deep capture with mitmproxy

1. `start_proxy` and `set_scope` to the target host(s) so you only capture
   what matters.
2. Point the client (browser or app) at the proxy and ensure the mitmproxy CA
   is trusted for HTTPS (visit `mitm.it` through the proxy, install cert).
   Without a trusted CA you only get plaintext HTTP + TLS metadata.
3. Reproduce the flow. Then:
   - `get_traffic_summary` for the captured flows.
   - `search_traffic` to filter by URL/method/content.
   - `inspect_flow` for full detail — it also returns a **curl equivalent** of
     the request, your bridge to replication.
4. `detect_auth_pattern` to infer the auth scheme, and `get_api_patterns` /
   `export_openapi_spec` to turn scattered calls into a structured API map.

## Mapping request dependencies

The hard part of any private API is that one call produces a value (token,
id, cursor, signature) that a later call needs. Build the dependency graph:

- Identify the "seed" call (usually login or a page bootstrap) that returns
  tokens/ids.
- Use mitmproxy `extract_from_flow` / `extract_session_variable` (regex or
  JSONPath) to pull those values out of responses.
- Trace which subsequent requests carry them (as headers, query params, or
  body fields). Note CSRF tokens and short-lived/signed tokens especially —
  these must be minted live, not copied.

## HAR as a portable capture

Any of these can produce a HAR (DevTools "Export HAR", or a proxy export). A
HAR is the durable artifact you hand to the replication step. When reading a
HAR programmatically, remember some HAR tools auto-redact `Authorization` /
`Cookie` headers — read those from the raw HAR or the live proxy flow if you
need them to replicate.

## Output of this phase

A concise API map: base URL, list of endpoints with method + purpose, the auth
scheme, required headers/params, and the dependency chain (what must be fetched
before what). Hand that to `request-replication.md`. Never include live token
values in the written map — reference them by name/location.
