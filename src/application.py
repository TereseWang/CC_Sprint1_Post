from flask import Flask
from datetime import datetime
import json
from flask_cors import CORS
from middleware.sns_notification import Notification
from flask import Response, request
import flask_sqlalchemy

sns_middleware = Notification()
db = flask_sqlalchemy.SQLAlchemy()
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:WHQ21cd1c689742@postdb.cyww6g5eerrg.us-east-1.rds.amazonaws.com:3306/post_database?charset=utf8"
db.init_app(app)

class Post(db.Model):
    __tablename__ = "post_info"
    pid = db.Column('pid', db.Integer, primary_key=True)
    uid = db.Column('uid', db.Integer)
    title = db.Column('post_title', db.Text)
    content = db.Column('post_content', db.Text)
    image = db.Column('image', db.String(200))
    date = db.Column('date', db.String(200))

    def __init__(self, uid, title, content, image):
        self.uid = uid
        self.title = title
        self.content = content
        self.date = str(datetime.now())
        self.image = image

    def toJson(self):
        return {
            'pid': self.pid,
            'uid': self.uid,
            'post_title': self.title,
            'post_content': self.content,
            'image':self.image,
            'date': self.date
        }
@app.route("/hello")
def helloworld():
    print('received')
    return "hello, client!"

@app.after_request
def after_request_func(response):
    print("after_request executing! Response = \n", json.dumps(response, indent=2, default=str))
    sns_middleware.check_publish(request, response)
    return response

@app.route("/api/post/create", methods=["POST"])
def create_post():
    try:
        uid, title, content, image = request.json['uid'], request.json['title'],request.json['content'], \
                                request.json['image']
        post = Post(uid, title, content, image)
        db.session.add(post)
        db.session.commit()
        ret = dict(success=True)
        return ret
    except Exception as e:
        print(e)
        ret = dict(success=False)
        return ret

@app.route("/api/post", methods=["GET"])
def get_post_by_pid():
    try:
        posts = Post.query.all()
        print(posts)
        resp = []
        for post in posts:
            resp.append(post.toJson())
            print(resp)
            print(post.toJson())
        result = Response(json.dumps(resp), status=200, content_type="application.json")
        return result
    except Exception as e:
        print(e)
        result = Response("get post failed", status=500, content_type="application.json")
        return result


@app.route("/api/post/update", methods=["POST"])
def updateByIdWithContent():
    print("try to update")
    try:
        pid, title, content, image = request.json['pid'], request.json['title'], request.json['content'], request.json['image']
        post = Post.query.filter(Post.pid == pid).first()
        post.content = content
        post.title = title
        post.image = image
        post.date = str(datetime.now())
        db.session.add(post)
        db.session.commit()
        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False}


@app.route("/api/post/delete", methods=['DELETE'])
def deletepost():
    args = request.args
    try:
        if 'pid' in args:
            pid = args.get('pid', type=int)
            post = Post.query.filter(Post.pid == pid)
            cnt = post.delete()
            db.session.commit()
            ret = dict(success=True, cnt=cnt)
            return ret
    except Exception as e:
        print(e)
        ret = dict(success=False)
        return ret

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
