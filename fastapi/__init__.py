from urllib.parse import parse_qs, urlparse


class Response:
    def __init__(self, content=b"", media_type="application/json", status_code=200):
        self.content = content if isinstance(content, bytes) else str(content).encode("utf-8")
        self.media_type = media_type
        self.status_code = status_code


class FastAPI:
    def __init__(self, docs_url=None, redoc_url=None):
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[("GET", path)] = func
            return func

        return decorator

    def _handle_get(self, raw_path: str):
        parsed = urlparse(raw_path)
        handler = self.routes.get(("GET", parsed.path))
        if handler is None:
            return Response(content=b'{"msg":"not found"}', status_code=404)

        query_params = {k: v[-1] for k, v in parse_qs(parsed.query).items()}
        try:
            result = handler(**query_params)
        except TypeError:
            # Missing/invalid params
            return Response(content=b'{"msg":"bad request"}', status_code=400)

        if isinstance(result, Response):
            return result

        return Response(content=result)
