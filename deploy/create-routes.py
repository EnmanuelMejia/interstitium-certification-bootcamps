#!/usr/bin/env python3
"""Create the /bootcamps/* worker routes on all three domains.

Run AFTER deploying the worker (deploy-worker-assets deploy/worker-config.json).
Needs the `custom.cloudflare` credential (same pattern as the cloudflare skill).

Usage: python3 deploy/create-routes.py
"""
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response  # noqa: E402

BASE = "https://api.cloudflare.com/client/v4"
WORKER = "cert-bootcamps"
ZONES = {
    "enmanueldmejia.com": "c17e24dfb06602421aefb6d8e88e60c2",
    "interstitiumlabs.dev": "3f705489afbb4d6ed20b777e2d027047",
}


def api(method, path, body=None):
    req = urllib.request.Request(
        BASE + path, data=body, method=method,
        headers={"Content-Type": "application/json"})
    add_surrogate_to_request(req, credential_name="custom.cloudflare",
                             allowed_hosts=["api.cloudflare.com"])
    try:
        resp = urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as e:
        print(json.dumps({"http_error": e.code,
                          "body": e.read().decode()[:2000]}, indent=2))
        sys.exit(1)
    return read_json_response(resp)


def main():
    for host, zone_id in ZONES.items():
        targets = [host] if host != "interstitiumlabs.dev" else [host, "learn." + host]
        for h in targets:
            pattern = "%s/bootcamps/*" % h
            r = api("POST", "/zones/%s/workers/routes" % zone_id,
                    body=json.dumps({"pattern": pattern, "script": WORKER}).encode())
            ok = r.get("success")
            print("route %s: %s" % (pattern, "OK" if ok else json.dumps(r)[:400]))


if __name__ == "__main__":
    main()
