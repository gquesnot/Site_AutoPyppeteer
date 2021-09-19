import asyncio
import json
import os

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.views import View

from AAPyppeteer import models
from AAPyppeteer.models import Project, Block, DataBlockType, DataBlock, ImageProject, BlockConfigured
from AAPyppeteer.util.aacontroller import AAController
from AAPyppeteer.views.views import ProjectsView


def getBlocksProject(request, projectPk):
    project = Project.objects.get(pk=projectPk)
    datasOut = DataBlockType.objects.all()
    datasIn = DataBlock.objects.filter(user_id=request.user.id)
    return render(request, "../templates/tab.html", {
        "type": "project",
        "items": project.blocks.all(),
        "datasOut": datasOut,
        "datasIn": datasIn
    })


class ProjectView(View):

    def get(self, request, pk):
        blocks = Block.objects.filter(user_id=request.user.id)
        project = Project.objects.get(pk=pk)
        datasOut = DataBlockType.objects.all()
        datasIn = DataBlock.objects.filter(user_id=request.user.id)
        return render(request, "../templates/project.html", {
            "blocks": blocks,
            "project": project,
            "datasOut": datasOut,
            "datasIn": datasIn
        })

    def post(self, request, pk):
        self.get(request, pk)


def runProject(request, projectPk):
    project = Project.objects.get(pk=projectPk)
    projectDict = project.getDict()
    res = []
    allActions = []
    newBlocks = []
    for block in projectDict['blocks']:
        newblock = {
            "name": block['name'],
            "isAdvanced": block['isAdvanced'],
            "isLinkedToNext": block['isLinkedToNext'],
            "nbThread": block['nbThread'],
            "datas": block['datas'],
            "datasIn": block['datasIn'],
            "datasOut": block['datasOut'],
            "type": block['block']['type'],
            "actions": [],
            "id": block['id']
        }
        for action in block['block']['elements']:
            tmp = {
                "action": action['type'],
                "name": action['name'],
            }
            for answer in action['answers']:
                if answer['name'] not in {'name'}:
                    tmp[answer['name']] = answer['value']
            newblock['actions'].append(tmp)
        newBlocks.append(newblock)
    # print(json.dumps(res, indent=4))

    projectDict['blocks'] = newBlocks
    # print(json.dumps(projectDict, indent=4))
    aa = AAController(projectDict)
    datas, datasOut, imgs = asyncio.run(aa.runAll())
    print("DATAS:\n", datas, "\nIMG:\n", imgs, "\nDATASOUT: \n", datasOut)
    urlList = {}

    project.datasOutUrl = datasOut
    project.save()
    for k, path in imgs.items():
        path = path.split('/')
        path = os.path.join(path[-3], path[-2], path[-1])
        url = static(path)
        urlList[k] = url
        image = project.images.filter(name_pk=f"{k}_{project.pk}")
        if not len(image):
            image = ImageProject(name_pk=f"{k}_{project.pk}", path=url, name=k)
            image.save()
            project.images.add(image)
            project.save()

    imageRender = render(request, "../templates/carousel.html", {
        "items": project.images.all().reverse(),
    })
    urlRender = render(request, "../templates/projecturl.html", {
        "data": project.datasOutUrl
    })

    return JsonResponse({"images": imageRender.content.decode('utf-8'), "url": urlRender.content.decode('utf-8')},
                        safe=False)


def updateBlockProject(request, blockPk):
    blockC = BlockConfigured.objects.get(pk=blockPk)
    blockC.name = request.POST['name']
    blockC.isAdvanced = request.POST['isAdvanced'] == "true"
    blockC.isLinkedToNext = request.POST['isLinkedToNext'] == "true"
    blockC.nbThread = int(request.POST['nbThread']) if request.POST['nbThread'] else 0
    blockC.datasIn = DataBlock.objects.get(pk=int(request.POST['datasIn'])) if request.POST['datasIn'] != "0" else None
    blockC.datasOut = DataBlockType.objects.get(pk=int(request.POST['datasOut'])) if request.POST['datasOut'] != "0" else None
    blockC.datas = json.loads(request.POST['datas'])
    # blockC.type = json.loads(request.POST['type'])
    blockC.save()
    return JsonResponse(blockC.getDict(), safe=False)


def updateProject(request, projectPk):
    project = Project.objects.get(pk=projectPk)
    for k, v in request.POST.items():

        if k not in ("csrfmiddlewaretoken", "datas", "name"):
            v = int(v)
        if k == "csrfmiddlewaretoken":
            continue
        else:
            if k in ("datasIn", "datasOut"):
                pass
            elif k == "datas":
                setattr(project, k, json.loads(v))
            else:
                print(k, v)
                setattr(project, k, v)
    print(project.name)
    project.save()
    return JsonResponse(project.getDict(), safe=False)


def addBlockToProject(request, projectPk):
    project = Project.objects.get(pk=projectPk)
    block = Block.objects.get(pk=request.POST['id'])
    isAdvanced = False if request.POST['isAdvanced'] == "false" else True
    isLinkedToNext = False if request.POST['isLinkedToNext'] == "false" else True
    nbThread = int(request.POST['nbThread']) if request.POST['nbThread'] else 0
    datas = json.loads(request.POST['datas'])
    print(request.POST['datasIn'], request.POST['datasOut'], type(request.POST['datasOut']))
    datasInId = int(request.POST['datasIn'])
    datasOutId = int(request.POST['datasOut'])
    if datasInId == 0:
        datasIn = None
    else:
        datasIn = DataBlock.objects.get(pk=datasInId)
    if datasOutId == 0:
        datasOut = None
    else:
        datasOut = DataBlockType.objects.get(pk=datasOutId)

    newBlockC = BlockConfigured(name=request.POST['name'], block=block, nbThread=nbThread, datas=datas,
                                isAdvanced=isAdvanced, datasIn=datasIn, datasOut=datasOut,
                                isLinkedToNext=isLinkedToNext)
    newBlockC.save()
    project.blocks.add(newBlockC)
    project.save()
    return render(request, "../templates/tab.html", {
        "type": "project",
        "items": project.blocks.all()
    })


def deleteBlockProject(request, projectPk, blockPk):
    project = Project.objects.get(pk=projectPk)
    block = BlockConfigured.objects.get(pk=blockPk)
    project.blocks.remove(block)
    project.save()
    block.delete()
    return JsonResponse(project.getDict(), safe=False)
