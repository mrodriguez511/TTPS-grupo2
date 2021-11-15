from app import create_app
import os

if "DYNO" in os.environ:
    app = create_app()
    app.run()
else:
    if __name__ == "__main__":
        app = create_app()
        app.run()
