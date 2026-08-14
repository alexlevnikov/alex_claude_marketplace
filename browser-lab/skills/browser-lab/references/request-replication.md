# Request Replication Playbook (mitmproxy + curlconverter)

Goal: take a captured request and reproduce it programmatically — as curl, as
code, and as a repeatable, parameterized call — with auth intact. Read
"Responsible use" in SKILL.md first.

## From capture to curl

- Fastest path: mitmproxy `inspect_flow` returns a **curl equivalent** of any
  captured flow. Copy that as the starting point.
- From a HAR or an existing curl, convert to clean code with `curlconverter`:

  ```bash
  # HAR (or a saved curl) -> Python requests
  npx curlconverter --language python request.har
  # -> JavaScript fetch
  npx curlconverter --language javascript request.har
  # also: go, ruby, php, rust, httpie, and more
  ```

  `curlconverter` accepts a curl command or a HAR and emits idiomatic client
  code that preserves headers, cookies (`-b`), and body.

## Replay with modifications

- **mitmproxy `replay_flow`** resends a captured request with a modified
  method, headers, or body — best for iterating against the live server with
  browser-grade impersonation.
- For scripted replay, run the generated curl / `requests` / `fetch` code and
  vary parameters programmatically.
- Change one thing at a time (a query param, a body field) and diff the
  response so you learn what each parameter controls.

## Handling auth when replicating

Most replication failures are auth, not HTTP shape. In order of durability:

1. **Cookies / session** — present in the capture as `Cookie`. curlconverter
   preserves them. They expire; if replay 401s, the session is stale.
2. **Bearer tokens / API keys** — request headers. Use mitmproxy
   `extract_session_variable` to pull a token from a login response, then
   `set_global_header` (or inject in your code) so every subsequent request
   carries it. `detect_auth_pattern` helps identify the scheme.
3. **CSRF / signed / short-lived tokens** — cannot be copied; they must be
   minted live because one response produces the value the next request needs.
   Two robust options:
   - Drive the real login/bootstrap with **playwright** so tokens are minted
     fresh, then extract them from the live session for the replayed call.
   - Model the dependency chain explicitly: fetch the seed request first,
     extract the token, then issue the dependent request in the same script.

## Parameterize and save

Once a request replays reliably:

- Extract the variable parts (ids, tokens, page cursors) into named inputs.
- Wrap the sequence (seed → extract → dependent calls) into a small script or,
  if the user uses one, a Postman/Bruno collection for reuse.
- Add pagination/looping only after a single call is proven correct.

## Verify

- Diff the replayed response against the originally captured response (status,
  key fields, shape). A matching 2xx with the expected payload = success.
- If it diverges, re-check: missing header, wrong content-type, a token that
  needed refreshing, or an ordering/timing dependency you skipped.

## Secrets hygiene

Never print live tokens, cookies, or keys into the response or committed
artifacts. Reference them by location ("the Bearer token from the login
response"), and scrub them from any saved code or HAR you hand back.
