#from flask import Flask
#app = Flask(__name__)
#if __name__ == '__main__':
#	app.run(host='0.0.0.0', port='5000', debug=True)

from userservice import app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
