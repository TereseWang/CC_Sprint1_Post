import requests
import json


def t1():

    health_url = "http://127.0.0.1:5011/api/health"

    try:
        h_message = requests.get(health_url)
        if h_message.status_code == 200:
            print("\n\n Congratulations. Your end-to-end test worked. \n\n")
            print("Application health message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ", h_message.status_code, "\n\n")
            print("\n")
    except Exception as e:
        print("\n\n Epic, Epic, Epic Fail. Exception = ", e, "\n\n")
        print("\n")


if __name__ == "__main__":
    t1()


