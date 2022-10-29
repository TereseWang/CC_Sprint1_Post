from flask import Flask, Response, request
from datetime import datetime
import json
from post_resource import PostResource
from post import Post
from flask_cors import CORS

# Create the Flask application object.
application = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(application)


@application.get("/api/post")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "CC-POST_SERVICE",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@application.route("/api/post/<pid>", methods=["GET"])
def get_post_by_pid(pid):
    result = PostResource.get_by_key(pid)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@application.route("/api/post/create", methods=["POST"])
def create_post_by_pid():
    uid = request.args.get('uid', None)
    post_content = request.args.get('content', None)
    print("Uid and post content is ", uid, post_content)

    result = PostResource.create_by_user(uid, post_content)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT SUCCESSFULLY CREATE", status=404, content_type="text/plain")

    return rsp


@application.route("/api/post/update", methods=["PUT"])
def update_post_by_pid():
    pid = request.args.get('pid', None)
    content = request.args.get('content', None)
    print("Post to be updated is ", pid)

    result = PostResource.update_by_key(pid, content)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT SUCCESSFULLY UPDATE", status=404, content_type="text/plain")

    return rsp


@application.route("/api/post/delete", methods=["DELETE"])
def delete_post_by_pid():
    pid = request.args.get('pid', None)
    print("Post to be deleted is ", pid)

    result = PostResource.delete_by_key(pid)

    if result:
        rsp = Response("NOT SUCCESSFULLY DELETE", status=404, content_type="text/plain")
    else:
        rsp = Response("SUCCESSFULLY DELETE", status=200, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
