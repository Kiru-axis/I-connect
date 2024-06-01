from core import create_app, db

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()  # Create sql tables for our data models
