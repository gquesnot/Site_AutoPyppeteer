import json
import os

import requests


class GoogleSlideApi:
    url = "IN TOKEN"
    secret = "IN TOKEN"

    def __init__(self):
        tokenPath = os.path.join(os.getcwd(), "AAPyppeteer", "util", "token.json")
        with open(tokenPath, "r") as f:
            jsonData = json.load(f)
            for k, v in jsonData.items():
                setattr(self, k, v)

    def createSlide(self, templateId, datas):
        
        datasIn = {"datas": json.dumps(datas), "templateId":templateId, "secret":self.secret, "type": "create_slide"}
        print(json.dumps(datasIn, indent=4))
        r = requests.get(self.url, params=datasIn)
        return r.text

