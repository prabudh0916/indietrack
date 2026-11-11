import os
from indietrack import create_app, db

app = create_app(os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    with app.app_context():
        # Ensure database tables exist on startup if using dev SQLite
        db.create_all()
    # Run development server
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true")
    app.run(host="127.0.0.1", port=port, debug=debug_mode, use_reloader=False)
