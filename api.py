from flask import Flask
from flask.ext import restful
from match import Matcher
import json

app = Flask(__name__)
api = restful.Api(app)

todos = {
    'todo1': 'remember your milk',
}
class TodoSimple(restful.Resource):
    def get(self, user_id, max_return, needs):
        mc = Matcher()
        # return json.dumps(mc.query(user_id, max_return, needs))
        return json.dumps(mc.query(user_id, max_return, 'all'))

# api.add_resource(HelloWorld, '/')
# api.add_resource(TodoSimple, '/<int:user_id>/<int:max_return>/<string:needs>/')
api.add_resource(TodoSimple, '/<int:user_id>/<int:max_return>')

if __name__ == '__main__':
    app.run(debug=True)
