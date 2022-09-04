from src import app
from src.api_routes.get import get_routes
from src.api_routes.post import post_routes


if __name__ == "__main__":
    get_routes(app)
    post_routes(app)
    app.run(host="0.0.0.0", debug=True)
