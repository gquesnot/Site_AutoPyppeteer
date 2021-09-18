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

    return render(request, "../templates/datas.html", {
        "dataBlocks": dataBlocks,
        "dataTypes":dataTypes
    })


def updateData(request, dataPk):
    return None


def addData(request):
    datas = json.loads(request.POST['datas'])
    typeId = request.POST['type']
    dataType = DataBlockType.objects.get(pk=typeId)
    path= None
    if dataType.requireFile:
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

    newData = DataBlock(name=request.POST['name'], path=path, datas=datas, type=dataType, user=request.user)
    newData.save()

    return JsonResponse(newData.getDict(), safe=False)