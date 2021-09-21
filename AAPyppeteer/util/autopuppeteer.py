import asyncio
import copy
import os
import re
from math import floor, ceil
from multiprocessing.pool import ThreadPool
from time import sleep, time

from pyppeteer import launch

from Site_Auto import settings
import django.conf as conf


class AutoPuppeteer:
    nbThread = 0
    id = 0
    isAdvanced = False
    name = ""
    globalDatas = []
    imgs = None
    block = None
    actions = []
    type = ""

    def __init__(self, block, controller, globalsDatas, datasIn):

        self.controller = controller
        self.mainBlock = block
        self.projectPk = controller.id
        self.lock = asyncio.Lock()
        self.globalDatas = globalsDatas

        for k, v in self.mainBlock.items():
            setattr(self, k, v)
        self.datasIn = datasIn
        print(self.datasIn)
        self.datasOut = dict()
        if self.isAdvanced:
            self.p = ThreadPool(self.nbThread if self.nbThread != 0 else 1)

        self.allStep = len(self.actions)
        self.maxLenConfig = 0
        self.lenStr = []

        for idx, action in enumerate(self.actions):
            if action['action'] == "screenshot":
                action = self.makeScreenShotConfig(action)
                self.actions[idx] = action

            tmpLen = len(repr(action))
            self.lenStr.append(tmpLen)
        if self.isAdvanced:
            self.actions = [copy.deepcopy(self.actions) for i in range(len(self.datasIn))]
        else:
            self.actions = (self.actions,)
        self.maxLenConfig = max(self.lenStr)
        self.step = 0
        self.page = lambda x: self.pages[(x % len(self.pages))]
        self.pages = []

    async def run(self):

        if not self.isAdvanced:
            outpout = await self.runAll()
            return self.datasOut, self.globalDatas, outpout
        else:
            limit = self.nbThread
            prev = 0
            outpout = []
            for i in range(prev, len(self.datasIn), limit):
                tmpMax = i + limit if i + limit < len(self.datasIn) else len(self.datasIn)
                outpout.append(await asyncio.gather(*[self.runAll(i) for i in range(prev, tmpMax)]))
                prev = i + limit
            datas = dict() | self.globalDatas
            imgs = dict()
            for row in outpout[0]:
                imgs.update(row)

            return self.datasOut, datas, imgs

    async def runAll(self, idx=0):
        result = {}
        page = await self.controller.createNewPage()
        # page = self.page(idx)
        # print(page)
        step = 0
        while step < self.allStep:
            action = await self.nextStep(step, page, idx)

            step += 1
        await page.close()
        return self.imgs

    def makeScreenShotConfig(self, action):
        return {
            "name": action['name'],
            "action": "screenshot",
            "path": self.configToPath(action),
            "fullPage": action['fullPage'] == "1",
            "clip": {
                "x": int(action['x']) if action['x'] != "" else 0,
                "y": int(action['y']) if action['y'] != "" else 0,
                "width": int(action['width']) if action['width'] != "" else 0,
                "height": int(action['height']) if action['height'] != "" else 0
            }
        }

    async def nextStep(self, step, page=None, idx=0):
        action = self.actions[idx][step]
        nextConfig = None
        if step + 1 < self.allStep:
            nextConfig = self.actions[idx][step + 1]

        t = time()
        self.applyReformatData(action, idx)
        print(self.name, "    step", step, "   idx", idx, "    ", action, end="")
        maxFail = 5
        # while maxFail > 0:
        #     try:
        action = await self.configToMethod(action, nextConfig, page)
            #     break
            # except:
            #     sleep(0.5)
            #     maxFail -= 1
            #     if maxFail == 0:
            #         raise ValueError

        if action['action'] in ("get js value", "get jquery value"):
            self.applySaveData(action, idx)

        elif action['action'] == "screenshot":
            if self.imgs is None:
                self.imgs = {action['name']: action['path']}
            else:
                self.imgs[action['name']] = action['path']

        print(f"{' ' * (self.maxLenConfig - self.lenStr[step] + 4)} OK",
              f"{round(time() - t, 3) if time() - t > 0 else 0}s")
        if "result" in action.keys():
            print('FOUND', action['value'], " = ", action['result'])

        return action

    def applyReformatData(self, action, idx):
        for actionKey in action.keys():

            if type(action[actionKey]) == str:
                regex = "\{{2}[A-Za-z0-9.]+\}{2}"

                founds = re.findall(regex, action[actionKey])

                for found in founds:
                    action = self.applyFound(action, actionKey, found, idx)


    def applySaveData(self, action, idx):
        try:
            hint = action['value'].split('.')
            if hint[0] == 'g':
                self.globalDatas = {action['value']: action['result']}
            elif hint[0] == "out":
                idxStr = str(idx)
                if idxStr not in self.datasOut.keys():
                    self.datasOut[idxStr] = dict()

                self.datasOut[idxStr][hint[1]] = action['result']
        except:
            pass

    def applyFound(self, action, actionKey, found, idx=0):

        valToFound = found[2:-2]
        actioncpy = copy.deepcopy(action)
        hint = valToFound.split('.')
        datas = ""
        if hint[0] == "g":
            if valToFound in self.globalDatas.keys():
                datas = self.globalDatas[hint[1]]
        elif hint[0] == "in" and idx is not None:
            try:
                datas  = self.datasIn[idx][hint[1]]
            except:
                pass
        print(f"REPLACE ON {action['name']} {action['action']} : {actionKey} : {action[actionKey]}=>", end="")
        action[actionKey] = action[actionKey].replace(found, datas)
        print(f"{action[actionKey]}")
        return action

    async def configToMethod(self, action, nextConfig, page):
        toDo = action['action']
        if 'cssSelector' in action:
            await page.waitForSelector(action['cssSelector'])
        if toDo == "go_to":
            await self.goToLink(action, page)
        elif toDo == "input":
            await self.applyInput(action, page)
        elif toDo == "click":
            await self.click(action, page)
        elif toDo == "screenshot":
            await self.takeScreenshot(action, page)
        elif toDo == "select":
            await self.applySelect(action, page)
        elif toDo == "wait_presence":
            await self.waitPresence(action, page)
        elif toDo == "eval_str":
            await self.eval(action, page)
        elif toDo == "real_click":
            await self.realClick(action, page)
        elif toDo == "wait_time":
            sleep(int(action['value']) / 1000)
        elif toDo in ("get js value", "exec js"):
            action = await self.getJsContent(action, page)
        elif toDo in ("get jquery value", "exec jquery"):
            action = await self.getJqueryContent(action, page)
        #await page.waitForNavigation()
        return action
        # await self.applyWait(action, nextConfig)

    async def applyWait(self, action, nextConfig, page):
        if "wait" in action:
            if action["wait"] is True:
                await page.waitForNavigation()
        if "waitNext" in action:
            if action["waitNext"] is True:
                await page.waitForSelector(nextConfig['cssSelector'])

        if "waitTime" in action:
            sleep(action['waitTime'] / 1000)

    async def eval(self, action, page):
        await page.evaluate(action['value'], force_expr=True)

    async def waitPresence(self, action, page):
        while await page.waitForSelector(action['cssSelector']) is None:
            sleep(0.25)

    async def applySelect(self, action, page):
        await page.querySelectorEval(action['cssSelector'], "(elem, val) => elem.selectedIndex = val",
                                     action['optionValue'])
        # print(await self.page.querySelectorEval(action['cssSelector'], "(elem, val) => elem.value", action['value']))
        # print(await self.page.querySelectorEval(action['cssSelector'], "(elem, val) => elem", action['value']))

    def configToPath(self, action):
        path = f"{os.getcwd()}/static/img/"
        if not os.path.isdir(path):
            os.mkdir(path)
            conf.settings.STATICFILES_DIRS.append(path)

        return path + f"/{self.projectPk}_{action['name']}.png"

    async def takeScreenshot(self, action, page):

        await page.screenshot(action)
        await self.lock.acquire()
        try:
            pass
        finally:
            self.lock.release()

    async def click(self, action, page):
        await page.querySelectorEval(action['cssSelector'], "elem => elem.click()")

    async def realClick(self, action, page):
        x = int(action['x'])
        y = int(action['y'])
        await page.mouse.click(x=x, y=y)

    async def applyInput(self, action, page):
        await page.querySelectorEval(action['cssSelector'], "(elem, val) => elem.value = val", action['value'])
        await page.querySelectorEval(action['cssSelector'], "(e) => e.blur()")

    async def goToLink(self, action, page):
        await page.goto(action['url'])

    async def getJsContent(self, action, page):
        try:
            result = await page.querySelectorEval(action['cssSelector'], f"elem => elem{action['js attr']}")
            print("result", result)
            if action['action'] == "get js value":
                action['result'] = result
        except:
            pass

        return action

    async def getJqueryContent(self, action, page):

        tmp = await page.addScriptTag({"url": "https://code.jquery.com/jquery-3.2.1.min.js"})
        string = f"elem => $('elem'){action['jquery attr']}"
        try:
            result = await page.querySelectorEval(action['cssSelector'], f"elem => $(elem){action['jquery attr']}")
            if action['action'] == "get jquery value":
                action['result'] = result
        except:
            pass


        return action
