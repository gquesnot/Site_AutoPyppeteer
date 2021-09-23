import json
import os
from sys import platform
from time import time

import requests
from django.templatetags.static import static
from pyppeteer import launch

from AAPyppeteer.util.autopuppeteer import AutoPuppeteer
from AAPyppeteer.util.excel import Excel
from AAPyppeteer.util.googlesheetapi import GoogleSheetApi
from AAPyppeteer.util.googleslideapi import GoogleSlideApi


class AAController:
    browser = None
    pages = []
    blocks = []
    name = []
    id = 0
    cookies = []
    allDataOut = []
    linkedToNextDatas = []
    googleApi = None

    def __init__(self, project, config=None):
        self.project = project
        if config is None:
            config = {
                "viewport": {"width": 1920, "height": 1080}
            }
        for k, v in project.items():
            setattr(self, k, v)
        self.allDataOut = []
        self.config = config
        self.globalDatas = dict()
        self.imgs = dict()

    async def runAll(self):
        await self.startBrowser()

        try:
            for block in self.blocks:
                datasIn = self.processDatasIn(block)

                tmpAP = AutoPuppeteer(block, self, self.globalDatas, self.linkedToNextDatas or datasIn)
                datasOut, resData, imgs = await tmpAP.run()
                self.linkedToNextDatas = []
                if imgs is not None:
                    self.imgs |= imgs
                self.globalDatas = resData
                print(self.globalDatas, datasOut)
                self.linkedToNextDatas = self.processDatasOut(block, datasOut)

        except:
            await self.closeBrowser()
        await self.closeBrowser()
        print(self.allDataOut)
        return self.globalDatas, self.allDataOut, self.imgs

    def processDatasIn(self, block):
        if block['datasIn'] is not None:
            datasInC = block['datasIn']

            if datasInC['type']['name'] == "Excel IN":
                ex = Excel(datasInC['path'])
                return ex.getValues(datasInC['datas']['start'], datasInC['datas']['end'],
                                    datasInC['datas']['sheetName'])
            elif datasInC['type']['name'] == "Google Spreadsheet IN":
                gs = GoogleSheetApi(datasInC["datas"]['sheetId'])
                return gs.getValues(datasInC['datas']['start'], datasInC['datas']['end'],
                                    datasInC['datas']['sheetName'])
            elif datasInC['type']['name'] == "API IN":
                print(datasInC['datas'])
                f = requests.get if datasInC['datas']['method'] == "GET" else requests.post
                params = datasInC['datas']['params']
                res = f(datasInC['datas']["url"], params=params)
                print(res)
                return res.json()
            elif datasInC['type']['name'] == "JSON IN":
                return json.loads(datasInC['datas']['datas'])
        return None

    def processDatasOut(self, block, datasOut):


        if datasOut is not None and block['datasOut'] is not None:
            datasOutC = block['datasOut']
            tmp = {
                "name": block['name'],
                "blockType": datasOutC["type"]['name'],
            }
            if datasOutC['type']['name'] == "Excel OUT":
                ex = Excel()
                path = ex.insertValues(datasOut)
                tmp['type'] = "static"
                tmp['url'] = path
            elif datasOutC['type']['name'] == "Google Spreadsheet OUT":
                print("pass here")
                gs = GoogleSheetApi()

                path = gs.insertValues(datasOut)

                tmp['type'] = "normal"
                tmp['url'] = path

            elif datasOutC['type']['name'] == "Google Slide OUT":
                gs = GoogleSlideApi()
                url = gs.createSlide(datasOutC['datas']['templateId'], self.globalDatas)

                tmp['type'] = "normal"
                tmp['url'] = url.replace("\"", "")

            elif datasOutC['type']['name'] == "API OUT":
                print(datasOutC['datas'])
                f = requests.get if datasOutC['datas']['method'] == "GET" else requests.post
                params = datasOutC['datas']['params']
                params['datas'] = json.dumps(datasOut)
                res = f(datasOutC['datas']["url"], params=params)
                tmp['type'] = "normal"
                tmp['url'] = datasOutC['datas']['url']

            elif datasOutC['type']['name'] == "JSON OUT":
                rPath = f"{os.getcwd()}/static/filesOut/{str(int(time()))}.json"
                with open(rPath, 'w') as f:
                    json.dump(datasOutC, f)
                path = rPath.split('/')
                path = os.path.join(path[-2], path[-1])
                url = static(path)
                tmp['type'] = "static"
                tmp['url'] = url
            self.allDataOut.append(tmp)
        return datasOut if block['isLinkedToNext'] else []

    async def createNewPage(self):
        page = await self.browser.newPage()
        await page.setViewport(self.config['viewport'])
        self.pages.append(page)
        return page

    async def startBrowser(self):
        try:
            if platform == "linux":
                self.browser = await launch(handleSIGINT=False,
                                            handleSIGTERM=False,
                                            handleSIGHUP=False,
                                            handleSIGPIPE=True,
                                            headless=True,
                                            executablePath='/usr/bin/google-chrome-stable',
                                            args=[
                                                '--no-sandbox',
                                            ]
                                            )
            else:
                self.browser = await launch(handleSIGINT=False,
                                            handleSIGTERM=False,
                                            handleSIGHUP=False,
                                            handleSIGPIPE=True,
                                            headless=True,
                                            args=[
                                                '--no-sandbox',
                                            ]
                                            )
        except:
            print("ERROR OS")

    async def closeBrowser(self):
        for page in self.pages:
            try:
                await page.close()
            except:
                pass
        if self.browser is not None:
            await self.browser.close()
            self.browser = None
