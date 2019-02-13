from app import create_app

app = create_app()

# gunicorn -b 127.0.0.1:8000 -k gevent -w 2 --threads 4 --max-requests 2000 wsgi:app -D


if __name__ == "__main__":
    app.run()
