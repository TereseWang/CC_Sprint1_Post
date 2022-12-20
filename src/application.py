from flask import Flask, Response, request
from datetime import datetime
import json
from post_resource import PostResource
from post import Post
from flask_cors import CORS
from middleware.sns_notification import Notification
from flask import Response, request

sns_middleware = Notification()

# Create the Flask application object.
application = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(application)

@application.after_request
def after_request_func(response):
    print("after_request executing! Response = \n", json.dumps(response, indent=2, default=str))
    sns_middleware.check_publish(request, response)

    return response

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
        rsp = Response("NOT FOUND", status=404, content_type="application.json")

    return rsp


@application.route("/api/post/create/<uid>/<title>/<content>/<date>/<image>", methods=["POST"])
def create_post(uid, title, content, date, image):

    result = PostResource.create_by_user(uid, title, content, date, image)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT SUCCESSFULLY CREATE", status=404, content_type="application.json")

    print("Finish operation and the response is ", rsp)
    return rsp


@application.route("/api/post/update/<postId>/<content>", methods=["PUT"])
def update_post_by_pid(postId, content):

    result = PostResource.update_by_key(postId, content)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT SUCCESSFULLY UPDATE", status=404, content_type="application.json")

    return rsp


@application.route("/api/post/delete/<pid>", methods=["DELETE"])
def delete_post_by_pid(pid):

    result = PostResource.delete_by_key(pid)

    if result:
        rsp = Response("NOT SUCCESSFULLY DELETE", status=404, content_type="application.json")
    else:
        rsp = Response("SUCCESSFULLY DELETE", status=200, content_type="application.json")

    return rsp


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5011, debug=True)
