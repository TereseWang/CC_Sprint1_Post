import boto3
import json


class Notification():

    def __init__(self):
        self.s_topic = "arn:aws:sns:us-east-1:950047596654:Post_Topic"
        self.sns_client = boto3.client('sns', region_name='us-east-1',
                                       aws_access_key_id='AKIA52MZ74BXAJVWB6N2',
                                       aws_secret_access_key= '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')

    def publish_notification(self, sns_topic, json_message):
        res = self.sns_client.publish(
            TopicArn=sns_topic,
            Message=json.dumps(json_message, indent=2, default=str),
            Subject='SoEme change in Post'
        )

        print("publish_notification response = ", json.dumps(res, indent=2, default=str))

    def check_publish(self, request, response):
        if self.s_topic:
            if request.method in ['PUT', 'POST', 'DELETE']:
                event = {
                    "URL": request.url,
                    "Method": request.method
                }
                print("request method is ", request.method)
                if request.url:
                    parameters = request.url.split('/')
                    data = {}
                    if request.method == 'POST':
                        data = {
                            "Operation": parameters[5],
                            "UserId": request.form['uid'],
                            "Title": request.form['title'],
                            "Content": request.form['content']
                        }
                    else:
                        data = {
                            "Operation": parameters[5],
                            "PostId": request.form['pid']
                        }
                    print(data)
                    event["new_data"] = data
                self.publish_notification(self.s_topic, event)
