import json
import os
import string

import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleSheetApi():
    sheetName = ""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    spreadsheetNew = {
        'properties': {
            'title': "new spreadsheet"
        }
    }

    def __init__(self, spreadsheetId= None):

        self.type = "out" if spreadsheetId is None else "in"
        creds = None
        self.spreadsheetId = spreadsheetId
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        tokenPath =f'{os.getcwd()}\\AAPyppeteer\\util\\token.json'
        credentialsPath=  f'{os.getcwd()}\\AAPyppeteer\\util\\credentials.json'
        if os.path.exists(tokenPath):
            creds = Credentials.from_authorized_user_file(tokenPath, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentialsPath, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(tokenPath, 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheetApi = self.service.spreadsheets()
        if self.type == "out":
            newSheet = self.sheetApi.create(body=self.spreadsheetNew,
                                          fields='spreadsheetId').execute()
            self.spreadsheetId = newSheet.get('spreadsheetId')

    def getValues(self, start, end, sheetName=None):
        sheet = sheetName if sheetName is not None else self.sheetName
        range = f"{sheet}!{start.replace(':', '')}:{end.replace(':', '')}"
        datas = self.sheetApi.values().get(spreadsheetId=self.spreadsheetId,
                                    range=range).execute()['values']
        resData = []
        alphabet = list(string.ascii_uppercase)
        for x, row in enumerate(datas):
            tmp= dict()
            for y, col in enumerate(row):

                yy= alphabet[y]
                tmp[yy] = col
            resData.append(tmp)
        return resData
    def insertValues(self, datas):

        alphabet = list(string.ascii_uppercase)
        len_ = len(datas.keys())
        keyLen = len(datas["0"].keys())
        range_ = f"Feuille 1!A1:{alphabet[keyLen - 1]}{len(datas) + 1}"
        res = []
        lastAdded = False
        for i in range(len_):
            for idxStr, data in datas.items():
                tmp = []
                if int(idxStr) == i:
                    for j in range(keyLen):
                        for k, v in data.items():
                            if k == alphabet[j]:
                                tmp.append(v)
                    res.append(tmp)

        body = {
            "values": res
        }
        result = self.sheetApi.values().update(
            spreadsheetId=self.spreadsheetId, range=range_,
            valueInputOption='RAW', body=body).execute()
        #requests.get('https://script.google.com/macros/s/AKfycbzpJxtmzx_B-q7dfuRwvhslzq7MsefOroXjy0VNcD07wz90D2gc9d6WImDuTx5mGB0PAA/exec?id='+ self.spreadsheetId)
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheetId}/edit?usp=sharing"

    def setSheet(self, sheetName):
        self.sheetName = sheetName

if __name__ == '__main__':
    gsa = GoogleSheetApi("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
    gsa.setSheet('Class Data')

    print(json.dumps(gsa.getValues("A:1", "E:5"),indent=4))