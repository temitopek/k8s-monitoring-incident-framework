"""Tiny demo alert receiver: prints every Alertmanager notification to stdout.
Replace with Slack/PagerDuty/email in alertmanager/alertmanager.yml for real use."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        for a in body.get("alerts", []):
            lbl, ann = a.get("labels", {}), a.get("annotations", {})
            print(f"[{self.path}] {a.get('status','?').upper()} {lbl.get('alertname')} "
                  f"severity={lbl.get('severity')} :: {ann.get('summary','')}", flush=True)
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass


HTTPServer(("0.0.0.0", 5001), H).serve_forever()
