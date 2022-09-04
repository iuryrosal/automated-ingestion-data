

def test_api_is_created(app):
    assert app.name == "src.utils.api_factory"


def test_request_returns_404(app):
    assert app.test_client().get("/url_not_exists").status_code == 404
