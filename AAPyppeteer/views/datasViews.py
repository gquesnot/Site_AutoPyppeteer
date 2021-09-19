import json
import os
from time import time

from django.http import JsonResponse
from django.shortcuts import render

from AAPyppeteer.models import DataBlock, DataBlockType
from django.templatetags.static import static


def datasBlockView(request):
    try:
        dataBlocks = DataBlock.objects.filter(user_id=request.user)
    except:
        dataBlocks = []
    dataTypes = DataBlockType.objects.all()
    # try:
    #
    # except:
    #     dataTypes = []
    res = []
    for block in dataBlocks:
        block.elements = []
        tmp = {}

        for k, el in block.type.datas.items():
            try:
                el['value'] = block.datas[k]
            except:
                pass
            tmp[k] = el
        block.datas = tmp
    return render(request, "../templates/datas.html", {
        "dataBlocks": dataBlocks,
        "dataTypes": dataTypes
    })


def updateData(request, dataPk):
    dataBlock = DataBlock.objects.get(pk=dataPk)
    dataBlock.datas = json.loads(request.POST['datas'])
    if dataBlock.type.requireFile:
        if len(request.FILES) > 0:
            dataBlock.path = checkAndDataFile(request)
    dataBlock.save()
    return JsonResponse(dataBlock.getDict(), safe=False)


def addData(request):
    datas = json.loads(request.POST['datas'])
    typeId = request.POST['type']
    dataType = DataBlockType.objects.get(pk=typeId)
    path = None
    if dataType.requireFile:
        path = checkAndDataFile(request)

    newData = DataBlock(name=request.POST['name'], path=path, datas=datas, type=dataType, user=request.user)
    newData.save()

    return JsonResponse(newData.getDict(), safe=False)


def checkAndDataFile(request):
    path = ""
    if len(request.FILES) > 0:
        file = request.FILES['fileData']
        path = f"{os.getcwd()}/static/files/{str(int(time()))}.{file.name.split('.')[-1]}"
        with open(path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        path = path.split('/')
        path = os.path.join(path[-2], path[-1])
        path = static(path)
        print(path)
    return path
