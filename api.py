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
    def get(self, user_id):
        # return {todo_id: todos[todo_id]}
        # return 'good'
        mc = Matcher()
        try:
            user_id = int(user_id)
        except:
            return "you have entered an invalid url"
        return json.dumps({'matched_ids':mc.get_matched_persons(user_id, 2)})

# api.add_resource(HelloWorld, '/')
api.add_resource(TodoSimple, '/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
