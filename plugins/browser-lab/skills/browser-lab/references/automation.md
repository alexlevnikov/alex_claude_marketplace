# Automation Playbook (playwright)

Use the **playwright** server to drive pages: navigation, forms, clicks,
uploads, multi-step flows, and screenshots. It targets the accessibility tree,
so it is fast and deterministic — prefer it over coordinate clicking.

## Core loop

1. `browser_navigate` to the start URL.
2. `browser_snapshot` to get the accessibility tree with element refs. Read
   the snapshot to find the element you want — do not guess selectors.
3. Act with `browser_click`, `browser_type`, `browser_select_option`,
   `browser_hover`, `browser_press_key`, using the refs from the snapshot.
4. `browser_wait_for` on text/element/state changes before the next step.
5. Re-snapshot after any navigation or DOM change; refs go stale.

## Forms

- Prefer `browser_fill_form` to set many fields in one call when the server
  supports it; otherwise `browser_type` field by field.
- For dropdowns use `browser_select_option`; for checkboxes/radios click the
  ref. For file inputs use `browser_file_upload`.
- Submit by clicking the submit control, then `browser_wait_for` the result
  (success text, URL change, or a network response).

## Authentication

- Drive the real login form when you need a fresh, valid session — this mints
  live cookies/tokens rather than copying stale ones.
- Reuse the browser session across steps so the login persists. Use a
  persistent profile if the flow spans multiple runs.
- Never print captured credentials or session cookies back to the user.

## When the accessibility tree isn't enough

- Canvas/WebGL/custom widgets may not expose refs. Fall back to
  `browser_take_screenshot` + coordinate tools (`browser_mouse_click_xy`,
  `*_move_xy`, `*_drag_xy`).
- To read or manipulate page state directly, use `browser_evaluate` to run JS
  in the page context (e.g. read a value, scroll a container, trigger an event).

## Reading what the page did

- `browser_console_messages` for console output during the run.
- `browser_network_requests` for a list of requests the page made. For deep
  request/response inspection, switch to the **chrome-devtools** server
  (`get_network_request`) — see `debugging.md`.

## Robustness

- Wait on conditions, never fixed sleeps.
- Assert the end state before declaring success: element visible, expected
  text present, URL correct, or a 2xx response for the key call.
- On flaky steps, re-snapshot and retry once; if it still fails, capture a
  screenshot + console + last network entries and report what blocked you.

## Scale / anti-bot (optional add-ons)

The bundled playwright server runs one local browser. For parallel fleets,
proxies, CAPTCHA handling, or stealth against defended sites, add a cloud
provider MCP (Browserbase or Bright Data — see the plugin README) and route
only the hardened targets there. Keep everyday driving on local playwright.
