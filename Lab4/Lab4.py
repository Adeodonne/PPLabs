from flask import Flask, make_response

def create_app():
    app = Flask(__name__)

    @app.route('/api/v1/hello-world-2', methods=['GET'])
    def helloorld():
        return 'Hello World 2!'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

#waitress-serve --host 127.0.0.1 --port 8081 --call "Lab4:create_app"
#http://127.0.0.1:8081/api/v1/hello-world-2