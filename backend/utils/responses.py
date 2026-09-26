"""Consistent JSON error helpers — never leak stack traces to clients."""

from flask import jsonify


def error_response(message, status_code=400, errors=None):
    """Build a standard error payload."""
    payload = {"success": False, "message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status_code


def success_response(data=None, message=None, status_code=200):
    """Build a standard success payload."""
    payload = {"success": True}
    if message:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code
