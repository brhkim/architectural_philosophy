#!/usr/bin/env python3
"""Serve one elicitation canvas, accept one submission, write it to a file, and exit.

Python 3 standard library only. Usage:

    python3 canvas_server.py SPEC.json --out RESULT.json [--port N] [--host H]
                             [--url-port N] [--timeout SECONDS] [--overwrite]

It inlines SPEC.json into assets/canvas.html, serves the page, and prints one line

    CANVAS URL: http://localhost:PORT/?t=TOKEN

for the person to open. When the person presses "Send to interviewer", the page POSTs
its answers; the server checks the token and the request's Host and Origin, writes the
answers to --out, prints

    RESULT: /absolute/path/to/RESULT.json

and exits 0. With no submission before --timeout seconds (default 1800) it prints a
TIMEOUT line and exits 3, so an agent running it in the background is never left
waiting forever. The person can always fall back to the page's Copy or Download buttons.

Routes: GET / (the page), GET /ping (lets the page confirm it is served by this helper and
show its "Send to interviewer" button), POST /result (one submission). All need the token.

Security model (the page is a local, single-use form):
  * a random token is required on every request (query parameter t);
  * Host must be localhost or 127.0.0.1 on an allowed port (blocks DNS rebinding);
  * a POST must carry Origin equal to http://<its own Host> (blocks other web pages);
  * exactly one accepted submission, a size cap, and JSON that parses.

Containers: the browser runs on the host, so bind inside the container with
--host 0.0.0.0 and pick a port the container publishes (for example --port 3000). If the
published host port differs from the container port, pass it as --url-port so the printed
URL and the Host check use it.

Exit codes: 0 result written, 2 usage or startup error, 3 timed out.
"""
# §§ IMPORTS
import argparse
import json
import os
import re
import secrets
import socket
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "canvas.html"
MAX_BODY = 2 * 1024 * 1024
LOOPBACK_NAMES = ("localhost", "127.0.0.1")


# §§ PAGE_BUILD
def script_json(obj):
    text = json.dumps(obj, ensure_ascii=False, indent=1)
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def build_page(spec, template=TEMPLATE):
    html = Path(template).read_text(encoding="utf-8")
    pat = re.compile(r'^(<script type="application/json" id="canvas-spec">)(.*?)(</script>)', re.S | re.M)
    if not pat.search(html):
        raise ValueError(f"{template} has no canvas-spec block")
    return pat.sub(lambda m: m.group(1) + script_json(spec) + m.group(3), html, count=1)


def check_spec(spec):
    if not isinstance(spec, dict) or not isinstance(spec.get("widgets"), list) or not spec["widgets"]:
        return "spec must be a JSON object with a non-empty 'widgets' list"
    for i, w in enumerate(spec["widgets"]):
        if not isinstance(w, dict) or not w.get("kind"):
            return f"widgets[{i}] needs a 'kind'"
    return None


# §§ REQUEST_CHECKS
def host_ok(host, ports):
    """Host header must be a loopback name on one of our ports."""
    if not host:
        return False
    m = re.fullmatch(r"(localhost|127\.0\.0\.1)(?::(\d{1,5}))?", host.strip().lower())
    if not m:
        return False
    port = int(m.group(2)) if m.group(2) else 80
    return port in ports


# §§ SERVER
class CanvasServer(HTTPServer):
    allow_reuse_address = True

    def __init__(self, addr, page, token, out_path, ports, overwrite):
        super().__init__(addr, Handler)
        self.page = page.encode("utf-8")
        self.token = token
        self.out_path = out_path
        self.ports = ports
        self.overwrite = overwrite
        self.done = False


class Handler(BaseHTTPRequestHandler):
    server_version = "CanvasServer/0.1"

    def log_message(self, fmt, *args):  # keep stdout clean for the agent; log refusals only
        pass

    def send_json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def refuse(self, code, why):
        print(f"REFUSED: {self.command} {urlsplit(self.path).path} ({why})", file=sys.stderr, flush=True)
        self.send_json(code, {"ok": False, "error": why})

    def common_checks(self):
        host = self.headers.get("Host", "")
        if not host_ok(host, self.server.ports):
            self.refuse(403, "host not allowed")
            return None
        query = parse_qs(urlsplit(self.path).query)
        tok = (query.get("t") or [""])[0]
        if not secrets.compare_digest(tok.encode(), self.server.token.encode()):
            self.refuse(403, "bad or missing token")
            return None
        return host

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if self.common_checks() is None:
            return
        if path == "/ping":
            self.send_json(200, {"ok": True, "canvas_server": True})
            return
        if path not in ("/", "/index.html"):
            self.refuse(404, "not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.server.page)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(self.server.page)

    def do_POST(self):
        host = self.common_checks()
        if host is None:
            return
        if urlsplit(self.path).path != "/result":
            self.refuse(404, "not found")
            return
        origin = self.headers.get("Origin")
        if origin != "http://" + host.strip().lower():
            self.refuse(403, "origin not allowed")
            return
        if self.server.done:
            self.refuse(409, "a result was already submitted")
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if length <= 0 or length > MAX_BODY:
            self.refuse(413 if length > MAX_BODY else 400, "missing or oversized body")
            return
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.refuse(400, "body is not JSON")
            return
        if not isinstance(data, dict) or not isinstance(data.get("results"), list):
            self.refuse(400, "body must be a canvas result with a 'results' list")
            return
        out = self.server.out_path
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            tmp = out.with_name(out.name + ".part")
            tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            os.replace(tmp, out)
        except OSError as e:
            self.refuse(500, f"could not write result: {e}")
            return
        self.server.done = True
        self.send_json(200, {"ok": True})


# §§ PORTS
def free_port(host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return s.getsockname()[1]


# §§ MAIN
def main(argv=None):
    ap = argparse.ArgumentParser(description="Serve one philosophy canvas and collect one submission.")
    ap.add_argument("spec", help="canvas spec JSON")
    ap.add_argument("--out", required=True, help="where to write the submitted answers (JSON)")
    ap.add_argument("--host", default="127.0.0.1", help="bind address (default 127.0.0.1; use 0.0.0.0 inside a container)")
    ap.add_argument("--port", type=int, default=0, help="port to listen on (default: a free one)")
    ap.add_argument("--url-port", type=int, default=0, help="port the browser uses, if a container maps it differently")
    ap.add_argument("--timeout", type=float, default=1800, help="seconds to wait for a submission (default 1800)")
    ap.add_argument("--template", default=str(TEMPLATE), help="canvas template (default: assets/canvas.html)")
    ap.add_argument("--overwrite", action="store_true", help="allow replacing an existing --out file")
    args = ap.parse_args(argv)

    try:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: cannot read spec {args.spec}: {e}", file=sys.stderr)
        return 2
    problem = check_spec(spec)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2
    out = Path(args.out).resolve()
    if out.exists() and not args.overwrite:
        print(f"error: {out} already exists; choose a new --out or pass --overwrite", file=sys.stderr)
        return 2
    try:
        page = build_page(spec, args.template)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    port = args.port or free_port(args.host)
    url_port = args.url_port or port
    token = secrets.token_urlsafe(18)
    try:
        server = CanvasServer((args.host, port), page, token, out, {port, url_port}, args.overwrite)
    except OSError as e:
        print(f"error: cannot listen on {args.host}:{port}: {e}", file=sys.stderr)
        return 2
    server.timeout = 0.5
    print(f"CANVAS URL: http://localhost:{url_port}/?t={token}", flush=True)
    deadline = time.monotonic() + args.timeout
    try:
        while not server.done and time.monotonic() < deadline:
            server.handle_request()
    except KeyboardInterrupt:
        print("STOPPED: interrupted before a submission arrived", flush=True)
        return 3
    finally:
        server.server_close()
    if server.done:
        print(f"RESULT: {out}", flush=True)
        return 0
    print(f"TIMEOUT: no submission within {args.timeout:g} seconds; ask the person to use Copy answers instead", flush=True)
    return 3


if __name__ == "__main__":
    sys.exit(main())
