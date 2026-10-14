# Debugging Playbook (chrome-devtools)

Use the **chrome-devtools** server for deep frontend debugging via the Chrome
DevTools Protocol: console, network waterfall, performance traces, memory,
storage, and Lighthouse audits. This is the only bundled server with real
performance and protocol-level inspection.

## Console errors

1. `navigate_page` to the URL (or reproduce the failing interaction).
2. `list_console_messages` to see errors/warnings; `get_console_message` for
   full detail including source-mapped stack traces.
3. Correlate the error to a network failure or a script. Use
   `evaluate_script` to probe page state (feature flags, globals, element
   presence).

## Network inspection

- `list_network_requests` for the full waterfall (URL, method, status, type,
  timing). Filter mentally to XHR/fetch to find API calls.
- `get_network_request` for one request's full headers, request payload,
  response body, and timing. This is how you see the exact API contract.
- Look for: failing status codes, slow calls, blocking waterfalls, oversized
  responses, missing caching headers, and auth headers on the API calls.

## Performance ("why is it slow")

1. `performance_start_trace`, reproduce the slow interaction, then
   `performance_stop_trace`.
2. `performance_analyze_insight` to surface bottlenecks (long tasks, layout
   shifts, render-blocking resources, LCP/CLS contributors).
3. Use `emulate` to throttle CPU/network or emulate a device and re-measure —
   many "slow" bugs only appear on mid-tier mobile / slow networks.
4. `lighthouse_audit` for a structured performance / a11y / SEO / best-practice
   report with concrete recommendations.

## Storage, cookies, and app state

- Read/write `localStorage`, `sessionStorage`, and non-HttpOnly cookies via
  `evaluate_script` (`localStorage`, `document.cookie`).
- **HttpOnly cookies are invisible to JavaScript by design** — you cannot read
  them from the page. To see them, inspect the request headers via
  `get_network_request`, or capture at the proxy layer with **mitmproxy**
  (see `network-disassembly.md`).
- For memory leaks, use the heap-snapshot tools: take a snapshot, exercise the
  app, take another, and compare.

## Verifying a fix

Reproduce the original failing path and confirm: the console error is gone,
the failing request now returns 2xx, and the perf metric improved. Capture the
before/after numbers rather than asserting from feel.

## Debugging the user's real, logged-in browser (optional add-on)

The bundled server drives its own Chrome. To debug against the user's actual
logged-in session (real cookies, real extensions), add a real-browser
debugging MCP such as `browser-tools-mcp` (Chrome extension + Lighthouse) — see
the plugin README. Use it when the bug only reproduces with the user's live
session and cannot be recreated in a clean browser.
