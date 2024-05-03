from app import app
# register routes
from app.routes import *

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')