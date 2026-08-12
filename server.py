#!/usr/bin/env python3
"""Unified TDS GA7 policy server ΓÇö all five endpoints."""

from flask import Flask, request, jsonify
import re
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)


# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
#  Health
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
#  Task 1 ΓÇö CI/CD Container Release Gate
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
@app.route("/release-gate", methods=["POST"])
@app.route("/release-gate/release-gate", methods=["POST"])
@app.route("/", methods=["POST"])
def release_gate():
    payload = request.get_json(force=True, silent=True)
    if not isinstance(payload, dict):
        payload = {}

    violations = set()

    wf = payload.get("workflow") if isinstance(payload.get("workflow"), dict) else {}
    img = payload.get("image") if isinstance(payload.get("image"), dict) else {}

    # ΓöÇΓöÇ Rule 1: permissions must be exactly least-privilege ΓöÇΓöÇ
    if wf.get("permissions") != {
        "contents": "read",
        "packages": "write",
        "id-token": "none",
    }:
        violations.add("EXCESS_PERMISSION")

    # ΓöÇΓöÇ Rule 2a: pull_request_target is always unsafe ΓöÇΓöÇ
    if wf.get("trigger") == "pull_request_target":
        violations.add("UNSAFE_PR_TRIGGER")

    # ΓöÇΓöÇ Rule 2b: tests must pass, matrix complete, failFast false ΓöÇΓöÇ
    if (
        not wf.get("testsPassed", False)
        or not wf.get("matrixComplete", False)
        or wf.get("failFast", False)
    ):
        violations.add("TESTS_INCOMPLETE")

    # ΓöÇΓöÇ Rule 3: action pinning ΓöÇΓöÇ
    for act in wf.get("actions", []) if isinstance(wf.get("actions"), list) else []:
        if not isinstance(act, dict):
            continue
        owner = act.get("owner", "")
        ref = act.get("ref", "")
        if owner == "actions":
            pass  # first-party, version tag OK
        else:
            if not (
                isinstance(ref, str)
                and len(ref) == 40
                and all(c in "0123456789abcdef" for c in ref)
            ):
                violations.add("MUTABLE_ACTION")

    # ΓöÇΓöÇ Rule 4: image properties ΓöÇΓöÇ
    if not img.get("multiStage", False):
        violations.add("SINGLE_STAGE_IMAGE")
    if img.get("runsAsRoot", False):
        violations.add("ROOT_RUNTIME")
    if img.get("secretMode", "") not in ("none", "buildkit"):
        violations.add("SECRET_IN_LAYER")
    try:
        if img.get("criticalVulnerabilities", 0) > 0:
            violations.add("CRITICAL_CVE")
    except TypeError:
        violations.add("CRITICAL_CVE")
    if not img.get("digestPinned", False):
        violations.add("UNPINNED_IMAGE")

    # ΓöÇΓöÇ Rule 5: production-only extras ΓöÇΓöÇ
    if payload.get("target") == "production":
        if payload.get("event") != "push" or payload.get("ref") != "refs/heads/main":
            violations.add("INVALID_PRODUCTION_REF")
        if not wf.get("environmentApproval", False):
            violations.add("APPROVAL_REQUIRED")

    v = sorted(violations)
    return jsonify({"decision": "promote" if not v else "block", "violations": v})


# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
#  Task 2 ΓÇö LLM Action Firewall
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
_FW_TENANT = "tenant-nfopnki"
_FW_DOMAIN = "notify-uq0e5nk.example"


@app.route("/action-firewall", methods=["POST"])
def action_firewall():
    payload = request.get_json(force=True, silent=True)

    def _block(r):
        return jsonify({"decision": "block", "reason": r})

    # 1. top-level schema
    if not isinstance(payload, dict):
        return _block("INVALID_SCHEMA")
    action = payload.get("action")
    if not isinstance(action, dict):
        return _block("INVALID_SCHEMA")
    tool = action.get("tool")
    args = action.get("args")
    if not isinstance(tool, str):
        return _block("INVALID_SCHEMA")
    if not isinstance(args, dict):
        return _block("INVALID_SCHEMA")

    # 2. tool allowlist
    if tool not in ("search", "lookup_record", "send_email", "render_html"):
        return _block("TOOL_NOT_ALLOWED")

    # 3. per-tool argument schema (exactly the right keys + value types)
    if tool == "search":
        if set(args.keys()) != {"query"}:
            return _block("INVALID_SCHEMA")
        q = args["query"]
        if not isinstance(q, str) or len(q) < 1 or len(q) > 200:
            return _block("INVALID_SCHEMA")

    elif tool == "lookup_record":
        if set(args.keys()) != {"tenantId", "recordId"}:
            return _block("INVALID_SCHEMA")
        if not isinstance(args["tenantId"], str) or not isinstance(
            args["recordId"], str
        ):
            return _block("INVALID_SCHEMA")
        if not args["recordId"]:
            return _block("INVALID_SCHEMA")

    elif tool == "send_email":
        if set(args.keys()) != {"to", "subject", "body"}:
            return _block("INVALID_SCHEMA")
        if not all(isinstance(args[k], str) for k in ("to", "subject", "body")):
            return _block("INVALID_SCHEMA")

    elif tool == "render_html":
        if set(args.keys()) != {"html"}:
            return _block("INVALID_SCHEMA")
        if not isinstance(args["html"], str):
            return _block("INVALID_SCHEMA")

    # 4. tenant scope
    if tool == "lookup_record" and args["tenantId"] != _FW_TENANT:
        return _block("TENANT_SCOPE")

    # 5. email domain
    if tool == "send_email":
        to = args["to"]
        if "@" not in to:
            return _block("EGRESS_DENIED")
        domain = to.rsplit("@", 1)[1]
        if domain != _FW_DOMAIN:
            return _block("EGRESS_DENIED")

    # 6. human approval
    if tool == "send_email" and not payload.get("humanApproved", False):
        return _block("APPROVAL_REQUIRED")

    # 7. HTML safety
    if tool == "render_html":
        html = args["html"]
        if re.search(r"<\s*(script|iframe)\b", html, re.I):
            return _block("UNSAFE_OUTPUT")
        if re.search(r"\bon\w+\s*=", html, re.I):
            return _block("UNSAFE_OUTPUT")
        if re.search(r"javascript\s*:", html, re.I):
            return _block("UNSAFE_OUTPUT")

    return jsonify({"decision": "allow", "reason": "ALLOW"})


# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
#  Task 3 ΓÇö Terraform Plan Policy Gate
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
_TF_WS = "prod-hgb092"
_TF_LABELS = {
    "owner": "student-jmwnh",
    "environment": "production",
    "cost_center": "cc-bms5",
}
_TF_STATEFUL = {"storage_bucket", "sql_database", "persistent_disk"}


def _tf_reject(reason):
    return jsonify({"decision": "reject", "reason": reason})


@app.route("/terraform/plan", methods=["POST"])
def terraform_plan():
    p = request.get_json(force=True, silent=True)

    # ΓöÇΓöÇ Rule 1: value-type validation (INVALID_PLAN) ΓöÇΓöÇ
    if not isinstance(p, dict):
        return _tf_reject("INVALID_PLAN")

    required_top = {"environment", "state", "providerVersion", "destroyApproved", "resource"}
    if not required_top.issubset(p.keys()):
        return _tf_reject("INVALID_PLAN")

    env = p.get("environment")
    state = p.get("state")
    pv = p.get("providerVersion")
    da = p.get("destroyApproved")
    res = p.get("resource")

    if not isinstance(env, str):
        return _tf_reject("INVALID_PLAN")
    if not isinstance(state, dict):
        return _tf_reject("INVALID_PLAN")
    if not isinstance(pv, str):
        return _tf_reject("INVALID_PLAN")
    if type(da) is not bool:
        return _tf_reject("INVALID_PLAN")
    if not isinstance(res, dict):
        return _tf_reject("INVALID_PLAN")

    if "backend" not in state or "locked" not in state:
        return _tf_reject("INVALID_PLAN")
    backend = state.get("backend")
    locked = state.get("locked")
    if not isinstance(backend, str) or type(locked) is not bool:
        return _tf_reject("INVALID_PLAN")

    required_res = {"address", "type", "action", "labels", "secret", "forceDestroy"}
    if not required_res.issubset(res.keys()):
        return _tf_reject("INVALID_PLAN")

    r_addr = res.get("address")
    r_type = res.get("type")
    r_action = res.get("action")
    r_labels = res.get("labels")
    r_secret = res.get("secret")
    r_force = res.get("forceDestroy")

    if not isinstance(r_addr, str):
        return _tf_reject("INVALID_PLAN")
    if not isinstance(r_type, str):
        return _tf_reject("INVALID_PLAN")
    if not isinstance(r_action, str) or r_action not in ("create", "update", "delete"):
        return _tf_reject("INVALID_PLAN")
    if not isinstance(r_labels, dict):
        return _tf_reject("INVALID_PLAN")
    if r_secret is not None and not isinstance(r_secret, str):
        return _tf_reject("INVALID_PLAN")
    if type(r_force) is not bool:
        return _tf_reject("INVALID_PLAN")

    # ΓöÇΓöÇ Rule 2: environment ΓöÇΓöÇ
    if env != _TF_WS:
        return _tf_reject("ENVIRONMENT_MISMATCH")

    # ΓöÇΓöÇ Rule 3: state backend + lock ΓöÇΓöÇ
    if backend not in ("gcs", "s3", "azurerm", "remote") or not locked:
        return _tf_reject("STATE_UNSAFE")

    # ΓöÇΓöÇ Rule 4: provider pinning ΓöÇΓöÇ
    pvs = pv.strip()
    pinned = False
    if pvs.startswith("~>") or pvs.startswith("="):
        pinned = True
    elif re.match(r"^\d+\.\d+(\.\d+)?$", pvs):
        pinned = True
    if not pinned:
        return _tf_reject("UNPINNED_PROVIDER")

    # ΓöÇΓöÇ Rule 5: labels ΓöÇΓöÇ
    for k, v in _TF_LABELS.items():
        if r_labels.get(k) != v:
            return _tf_reject("MISSING_LABELS")

    # ΓöÇΓöÇ Rule 6: secret ΓöÇΓöÇ
    if r_secret is not None:
        if not r_secret.startswith("secret://") or len(r_secret) <= len("secret://"):
            return _tf_reject("PLAINTEXT_SECRET")

    # ΓöÇΓöÇ Rule 7: stateful delete approval ΓöÇΓöÇ
    is_stateful = any(x in r_type for x in ("storage_bucket", "sql_database", "persistent_disk"))
    if r_action == "delete" and is_stateful and not da:
        return _tf_reject("DELETE_NOT_APPROVED")

    # ΓöÇΓöÇ Rule 8: force-destroy on production storage_bucket ΓöÇΓöÇ
    is_bucket = "storage_bucket" in r_type
    if is_bucket and r_force:
        return _tf_reject("FORCE_DESTROY")

    return jsonify({"decision": "approve", "reason": "APPROVE"})


# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
#  Task 4 ΓÇö LLM Output Handling Gate  (sanitize-output)
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
_SO_HOSTS = {"cdn-9enr3tt.example", "app-yoashjf.example"}
_SO_CHANNELS = {"html", "markdown", "url", "sql", "shell"}

# ΓöÇΓöÇ Decoding helpers ΓöÇΓöÇ

def _decode_once(s):
    """percent ΓåÆ HTML entities ΓåÆ \\uXXXX, one pass each."""
    # 1. percent
    def _pct(m):
        try:
            return chr(int(m.group(1), 16))
        except Exception:
            return m.group(0)

    r = re.sub(r"%([0-9a-fA-F]{2})", _pct, s)

    # 2. HTML entities (only the five named + numeric)
    _named = {"lt": "<", "gt": ">", "quot": '"', "apos": "'", "amp": "&"}

    def _ent(m):
        e = m.group(1)
        if e in _named:
            return _named[e]
        if e.lower().startswith("#x"):
            try:
                return chr(int(e[2:], 16))
            except Exception:
                return m.group(0)
        if e.startswith("#"):
            try:
                return chr(int(e[1:]))
            except Exception:
                return m.group(0)
        return m.group(0)

    r = re.sub(r"&(#[xX][0-9a-fA-F]+|#\d+|lt|gt|quot|apos|amp);", _ent, r)

    # 3. \uXXXX
    def _uni(m):
        try:
            return chr(int(m.group(1), 16))
        except Exception:
            return m.group(0)

    r = re.sub(r"\\u([0-9a-fA-F]{4})", _uni, r)
    return r


# ΓöÇΓöÇ URL extraction ΓöÇΓöÇ

def _extract_urls(channel, text):
    if channel == "html":
        return re.findall(r"(?:src|href)\s*=\s*[\"']([^\"']*)[\"']", text, re.I)
    if channel == "markdown":
        return re.findall(r"\]\(([^)]*)\)", text)
    if channel == "url":
        return [text.strip()]
    return []


# ΓöÇΓöÇ Dangerous scheme ΓöÇΓöÇ

def _dangerous_scheme_text(text):
    return bool(re.search(r"(?:javascript|data|vbscript)\s*:", text, re.I))


def _dangerous_scheme_urls(urls):
    for u in urls:
        u = u.strip()
        if u.startswith("//"):
            continue  # protocol-relative ΓåÆ https, scheme is fine
        parsed = urlparse(u)
        if parsed.scheme and parsed.scheme.lower() not in ("http", "https"):
            return True
    return False


def _has_dangerous_scheme(text, urls):
    return _dangerous_scheme_text(text) or _dangerous_scheme_urls(urls)


# ΓöÇΓöÇ External exfil ΓöÇΓöÇ

def _external_exfil(urls):
    for u in urls:
        u = u.strip()
        if not u:
            continue
        if u.startswith("//"):
            u = "https:" + u
        parsed = urlparse(u)
        if not parsed.scheme and not parsed.netloc:
            continue  # relative
        hostname = parsed.hostname
        if hostname and hostname not in _SO_HOSTS:
            return True
    return False


# ΓöÇΓöÇ Per-tag / metachar checks ΓöÇΓöÇ

def _script_tag(t):
    return bool(re.search(r"<\s*(script|iframe|object|embed)\b", t, re.I))


def _event_handler(t):
    return bool(re.search(r"\bon\w+\s*=", t, re.I))


def _sql_meta(t):
    if re.search(r"['\";]", t):
        return True
    if "--" in t:
        return True
    if "/*" in t:
        return True
    if re.search(r"\bunion\b", t, re.I):
        return True
    if re.search(r"\bor\s+1\s*=\s*1", t, re.I):
        return True
    return False


def _shell_meta(t):
    if re.search(r"[;&|`<>]", t):
        return True
    if re.search(r"\$[({]", t):
        return True
    return False


# ΓöÇΓöÇ Channel-rule dispatcher ΓöÇΓöÇ

def _channel_violation(channel, text):
    """Return first violation code or None."""
    if channel == "html":
        if _script_tag(text):
            return "SCRIPT_TAG"
        if _event_handler(text):
            return "EVENT_HANDLER"
        urls = _extract_urls(channel, text)
        if _has_dangerous_scheme(text, urls):
            return "DANGEROUS_SCHEME"
        if _external_exfil(urls):
            return "EXTERNAL_EXFIL"
    elif channel in ("markdown", "url"):
        urls = _extract_urls(channel, text)
        if _has_dangerous_scheme(text, urls):
            return "DANGEROUS_SCHEME"
        if _external_exfil(urls):
            return "EXTERNAL_EXFIL"
    elif channel == "sql":
        if _sql_meta(text):
            return "SQL_METACHAR"
    elif channel == "shell":
        if _shell_meta(text):
            return "SHELL_METACHAR"
    return None


@app.route("/sanitize-output", methods=["POST"])
def sanitize_output():
    payload = request.get_json(force=True, silent=True)

    def _unsafe(r):
        return jsonify({"safe": False, "reason": r})

    # INVALID_SCHEMA
    if not isinstance(payload, dict):
        return _unsafe("INVALID_SCHEMA")
    channel = payload.get("channel")
    output = payload.get("output")
    if channel not in _SO_CHANNELS:
        return _unsafe("INVALID_SCHEMA")
    if not isinstance(output, str):
        return _unsafe("INVALID_SCHEMA")
    if len(output) > 20000:
        return _unsafe("INVALID_SCHEMA")

    # ENCODED_PAYLOAD
    decoded = _decode_once(output)
    if decoded != output:
        if _channel_violation(channel, decoded) is not None:
            return _unsafe("ENCODED_PAYLOAD")

    # channel rules on original
    v = _channel_violation(channel, output)
    if v:
        return _unsafe(v)

    return jsonify({"safe": True, "reason": "SAFE"})


# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
#  Task 5 ΓÇö OSINT Corroboration Engine
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
_CORR_TYPES = {"dns", "ct_log", "registry", "archive", "scan"}


def _iso(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


@app.route("/corroborate", methods=["POST"])
def corroborate():
    payload = request.get_json(force=True, silent=True)
    INV = {"verdict": "invalid", "confidence": "low", "corroboratingSources": []}
    UNV = {"verdict": "unverified", "confidence": "low", "corroboratingSources": []}

    if not isinstance(payload, dict):
        return jsonify(INV)

    claim = payload.get("claim")
    as_of = payload.get("asOf")
    stale = payload.get("stalenessDays")
    sources = payload.get("sources")

    if not isinstance(claim, dict):
        return jsonify(INV)
    cv = claim.get("value")
    if not isinstance(cv, str):
        return jsonify(INV)
    if as_of is None or not isinstance(as_of, str):
        return jsonify(INV)
    as_of_dt = _iso(as_of)
    if as_of_dt is None:
        return jsonify(INV)
    if stale is None or not isinstance(stale, (int, float)):
        return jsonify(INV)
    if sources is None or not isinstance(sources, list):
        return jsonify(INV)

    # collect valid-and-fresh sources
    fresh = []
    for src in sources:
        if not isinstance(src, dict):
            continue
        sid = src.get("id")
        origin = src.get("origin")
        val = src.get("value")
        obs = src.get("observedAt")
        stype = src.get("type")
        if not all(isinstance(x, str) for x in [sid, origin, val, obs]):
            continue
        if not isinstance(stype, str) or stype not in _CORR_TYPES:
            continue

        obs_dt = _iso(obs)
        if obs_dt is None:
            continue
        diff_days = (as_of_dt - obs_dt).total_seconds() / 86400.0
        if diff_days > stale:
            continue

        auth = src.get("authoritative", False)
        if not isinstance(auth, bool):
            auth = False

        fresh.append(
            {
                "id": sid,
                "origin": origin,
                "value": val,
                "type": stype,
                "authoritative": auth,
            }
        )

    # contradicted?
    contra = sorted(
        s["id"] for s in fresh if s["authoritative"] and s["value"] != cv
    )
    if contra:
        return jsonify(
            {
                "verdict": "contradicted",
                "confidence": "low",
                "corroboratingSources": contra,
            }
        )

    # supported?
    matching = [s for s in fresh if s["value"] == cv]
    reps = {}
    for s in matching:
        o = s["origin"]
        if o not in reps or s["id"] < reps[o]["id"]:
            reps[o] = s

    if len(reps) >= 2:
        rep_types = {v["type"] for v in reps.values()}
        conf = "high" if len(rep_types) >= 2 else "medium"
        ids = sorted(v["id"] for v in reps.values())
        return jsonify(
            {"verdict": "supported", "confidence": conf, "corroboratingSources": ids}
        )

    return jsonify(UNV)


# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
