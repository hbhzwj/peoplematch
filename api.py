from flask import Flask
from flask.ext import restful
from match import Matcher
import json
import psycopg2

app = Flask(__name__)
api = restful.Api(app)

todos = {
    'todo1': 'remember your milk',
}
class TodoSimple(restful.Resource):
    def get(self, user_id, max_return):
        conn = psycopg2.connect("dbname='template1'"
                                " user='wangjing' host='localhost'"
                                " password='123456'")
        mc = Matcher(conn)
        return json.dumps(mc.query(user_id, max_return))

# api.add_resource(HelloWorld, '/')
api.add_resource(TodoSimple, '/<int:user_id>/<int:max_return>')

if __name__ == '__main__':
    app.run(debug=True)
