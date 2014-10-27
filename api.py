from flask import Flask
from flask.ext import restful
from match import Matcher
import json
import psycopg2
import os

app = Flask(__name__)
api = restful.Api(app)

todos = {
    'todo1': 'remember your milk',
}
class TodoSimple(restful.Resource):
    def get(self, user_id, max_return):
        try:
            oe = os.environ
            conn = psycopg2.connect(database=oe['DB_NAME'],
                                    user=oe['DB_USER'],
                                    password=oe['DB_PASSWORD'],
                                    host=oe['DB_HOST'])
        except Exception as e:
            return str(e)
        mc = Matcher(conn)
        return json.dumps(mc.query(user_id, max_return))

# api.add_resource(HelloWorld, '/')
# api.add_resource(TodoSimple, '/<int:user_id>/<int:max_return>/<string:needs>/')
api.add_resource(TodoSimple, '/<int:user_id>/<int:max_return>')

if __name__ == '__main__':
    app.run(debug=True)
