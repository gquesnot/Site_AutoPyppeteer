import os
from sys import platform

from pyppeteer import launch

from AAPyppeteer.util.autopuppeteer import AutoPuppeteer
from AAPyppeteer.util.excel import Excel
from AAPyppeteer.util.googlesheetapi import GoogleSheetApi


class AAController:
    browser = None
    pages = []
    blocks = []
    name = []
    id = 0
    cookies = []
    allDataOut = []
    linkedToNextDatas = []

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
                if block['type'] == "Basic":

                    tmpAP = AutoPuppeteer(block, self, self.globalDatas, self.linkedToNextDatas or datasIn)
                    datasOut, resData, imgs = await tmpAP.run()
                    self.linkedToNextDatas = []
                    if imgs is not None:
                        self.imgs |= imgs

                    self.linkedToNextDatas = self.processDatasOut(block, datasOut)
                    self.globalDatas = resData

                else:
                    print("BLOCK IS DATA")
        except:
            await self.closeBrowser()
        await self.closeBrowser()

        return self.globalDatas, self.allDataOut, self.imgs

    @staticmethod
    def processDatasIn(block):
        if block['datasIn'] is not None:
            datasInC = block['datasIn']

            if datasInC['type']['name'] == "Excel":
                ex = Excel(datasInC['path'])
                return ex.getValues(datasInC['datas']['start'], datasInC['datas']['end'],
                                    datasInC['datas']['sheetName'])
            elif datasInC['type']['name'] == "Google Spreadsheet":
                gs = GoogleSheetApi(datasInC["datas"]['sheetId'])
                return gs.getValues(datasInC['datas']['start'], datasInC['datas']['end'],
                                    datasInC['datas']['sheetName'])
        return None

    def processDatasOut(self, block, datasOut):
        if datasOut is not None and block['datasOut'] is not None:
            datasOutC = block['datasOut']
            if datasOutC['name'] == "Excel":
                ex = Excel()
                path = ex.insertValues(datasOut)
                self.allDataOut.append({"url": path, "type": "other", "name": block['name']})
            elif datasOutC['name'] == "Google Spreadsheet":
                gs = GoogleSheetApi()
                path = gs.insertValues(datasOut)
                self.allDataOut.append({"url": path, "type": "static", "name": block['name']})
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
