import os
import sys
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIRequest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()


def _build_environ(event):
    headers = event.get("headers", {}) or {}
    method = event.get("method", "GET").upper()
    raw_path = event.get("path", "/")
    query = event.get("query", {}) or {}
    body = event.get("body", b"")
    if isinstance(body, str):
        body = body.encode("utf-8")

    query_string = "&".join(
        f"{k}={v}" for k, v in query.items()
    )

    environ = {
        "REQUEST_METHOD": method,
        "SCRIPT_NAME": "",
        "PATH_INFO": raw_path.split("?")[0],
        "QUERY_STRING": query_string,
        "CONTENT_TYPE": headers.get("content-type", ""),
        "CONTENT_LENGTH": str(len(body)) if body else "0",
        "SERVER_NAME": headers.get("host", "vercel.app"),
        "SERVER_PORT": "443",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "https",
        "wsgi.input": BytesIO(body),
        "wsgi.errors": BytesIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
    }
    for k, v in headers.items():
        key = k.upper().replace("-", "_")
        if key not in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            environ[f"HTTP_{key}"] = v
    return environ


def handler(event, context):
    status = "500 Internal Server Error"
    response_headers = []
    body_buffer = BytesIO()

    def start_response(s, headers, exc_info=None):
        nonlocal status, response_headers
        status = s
        response_headers = headers
        return body_buffer.write

    try:
        environ = _build_environ(event)
        result = application(environ, start_response)
        for chunk in result:
            if chunk:
                body_buffer.write(bytes(chunk))
        if hasattr(result, "close"):
            result.close()
    except Exception as e:
        status = "500 Internal Server Error"
        response_headers = [("Content-Type", "text/plain; charset=utf-8")]
        body_buffer.write(f"Server Error: {e}".encode("utf-8"))

    try:
        code_text = status.split(" ", 1)[0]
        status_code = int(code_text)
    except Exception:
        status_code = 500

    headers_out = {}
    is_base64 = False
    for k, v in response_headers:
        headers_out[k] = str(v)
        if k.lower() == "content-type" and "text" not in v.lower() and "json" not in v.lower() and "xml" not in v.lower() and "javascript" not in v.lower() and "css" not in v.lower():
            is_base64 = True

    raw_body = body_buffer.getvalue()
    import base64
    if is_base64:
        encoded_body = base64.b64encode(raw_body).decode("ascii")
    else:
        try:
            encoded_body = raw_body.decode("utf-8")
        except UnicodeDecodeError:
            encoded_body = base64.b64encode(raw_body).decode("ascii")
            is_base64 = True

    return {
        "statusCode": status_code,
        "headers": headers_out,
        "body": encoded_body,
        "encoding": "base64" if is_base64 else "utf-8",
        "isBase64Encoded": is_base64,
    }


app = handler
