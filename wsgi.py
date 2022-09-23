from src.bot.bot_app import app
from werkzeug.middleware.proxy_fix import ProxyFix


if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
