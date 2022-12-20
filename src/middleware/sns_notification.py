import boto3
import json


class Notification():

    def __init__(self):
        self.s_topic = "arn:aws:sns:us-east-1:950047596654:Post_Topic"
        self.sns_client = boto3.client('sns', region_name='us-east-1',
                                       aws_access_key_id='AKIA52MZ74BXBQKP4BO3',
                                       aws_secret_access_key= '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')

    def publish_notification(self, sns_topic, json_message):
        res = self.sns_client.publish(
            TopicArn=sns_topic,
            Message=json.dumps(json_message, indent=2, default=str),
            Subject='Some change in Post'
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
                    print(parameters)
                    data = {}
                    if request.method == 'POST':
                        data = {
                            "Operation": parameters[5],
                            "UserId": parameters[6],
                            "Title": parameters[7],
                            "Content": parameters[8]
                        }
                    else:
                        data = {
                            "Operation": parameters[5],
                            "PostId": parameters[6]
                        }
                    print(data)
                    event["new_data"] = data
                self.publish_notification(self.s_topic, event)
