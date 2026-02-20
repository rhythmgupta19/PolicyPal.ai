class TestClient:
    __test__ = False

    def __init__(self, app):
        self.app = app

    def get(self, path: str):
        return self.app._handle_get(path)
