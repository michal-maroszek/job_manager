import os

from website import create_app

# Use environment variables for configuring the app (see https://direnv.net/).
# The configuration should default to production-ready values.
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "FALSE").upper() == "TRUE"


app = create_app()

if __name__ == "__main__":
    app.run(port=8000, debug=FLASK_DEBUG)
