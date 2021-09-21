import json
import os
import string
import requests

class GoogleSheetApi():
    sheetName = "Feuille 1"
    spreadsheetNew = {
        'properties': {
            'title': "new spreadsheet"
        }
    }
    sheetApi = None
    driveApi = None
    fakeToken = ""
    url = "IN TOKEN.JSON"
    secret = "IN TOKEN.JSON"
    alphabet = list(string.ascii_uppercase)

    def __init__(self, spreadsheetId=None):

        self.type = "out" if spreadsheetId is None else "in"
        self.spreadsheetId = spreadsheetId
        tokenPath = os.path.join(os.getcwd(),  "AAPyppeteer", "util","token.json")
        with open(tokenPath, "r") as f:
            jsonData = json.load(f)
            for k,v in jsonData.items():
                setattr(self, k, v)

    def getValues(self, start, end, sheetName=None):
        sheet = sheetName if sheetName is not None else self.sheetName
        startR = self.alphabet.index(start.split(':')[0]) + 1
        endR = int(end.split(':')[1])
        startC = self.alphabet.index(start.split(':')[0]) + 1
        endC = int(start.split(':')[1])
        print(startR, endR, startC, endC)
        r = requests.get(self.url, params={
            "type": "insert_sheet",
            "startR": startR,
            "startC": startC,
            "endR": endR,
            "endC": endC,
            "id": self.spreadsheetId,
            "sheetName": sheet,
            "secret": self.secret
        })
        datas = r.json()
        resData = []

        for x, row in enumerate(datas):
            tmp = dict()
            for y, col in enumerate(row):
                yy = self.alphabet[y]
                tmp[yy] = col
            resData.append(tmp)
        return resData

    def insertValues(self, datas):
        print("INSERT")

        len_ = len(datas.keys())
        keyLen = len(datas["0"].keys())
        endC = keyLen
        endR = len(datas)
        print(endC, endR)
        res = []
        lastAdded = False
        for i in range(len_):
            for idxStr, data in datas.items():
                tmp = []
                if int(idxStr) == i:
                    for j in range(keyLen):
                        for k, v in data.items():
                            if k == self.alphabet[j]:
                                tmp.append(v)
                    res.append(tmp)
        body = json.dumps(res)
        r = requests.get(self.url, params={
            "type": "get_sheet",
            "startR": 1,
            "startC": 1,
            "endR": endR,
            "endC": endC,
            "datas": body,
            "secret": self.secret
        })
        return r.text

    def setSheet(self, sheetName):
        self.sheetName = sheetName


if __name__ == '__main__':
    gsa = GoogleSheetApi("1g33fDq_IqBbtFEs8vLpacZ3D3fOzp4Q_fpvGjbjbQWw")
    # url = gsa.insertValues({'3': {'A': 'A4B4'}, '4': {'A': 'A5B5'}, '1': {'A': 'A2B2'}, '0': {'A': 'A1B1'}, '5': {'A': 'A6B6'}, '9': {'A': 'A10B10'}, '6': {'A': 'A7B7'}, '2': {'A': 'A3B3'}, '10': {'A': 'A11B11'}, '7': {'A': 'A8B8'}, '8': {'A': 'A9B9'}, '11': {'A': 'A12B12'}, '17': {'A': 'A18B18'}, '12': {'A': 'A13B13'}, '13': {'A': 'A14B14'}, '15': {'A': 'A16B16'}, '19': {'A': 'A20B20'}, '14': {'A': 'A15B15'}, '18': {'A': 'A19B19'}, '20': {'A': 'A21B21'}, '16': {'A': 'A17B17'}})
    print(gsa.getValues("A:1", "A:21"))

    # print(json.dumps(gsa.getValues("A:1", "E:5"), indent=4))
