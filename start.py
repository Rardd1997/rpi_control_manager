from app import create_app, db, cli


if __name__ == "__main__":
    app = create_app()
    cli.register(app)
    app.run(debug=True)