import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from AAPyppeteer.models import BlockConfigured, Block, Project, BaseAction


def updateBlock(request, blockPk):

    blockC = BlockConfigured.objects.get(pk=blockPk)
    blockC.isAdvanced = request.POST['isAdvanced'] == "true"
    blockC.nbThread = int(request.POST['nbThread']) if request.POST['nbThread'] else 0
    blockC.datas = json.loads(request.POST['datas'])
    #blockC.type = json.loads(request.POST['type'])
    blockC.save()
    return JsonResponse(blockC.getDict(), safe=False)


def addBlock(request):
    block = Block(name=request.POST['name'], user_id=request.user, type=request.POST['type'])
    block.save()
    return JsonResponse(block.getDict(), safe=False)


def delBlock(request, blockPk):
    block = Block.objects.get(pk=blockPk)
    block.delete()
    return JsonResponse("", safe=False)


def getBlocks(request):
    blocks = Block.objects.all()
    return JsonResponse([block.getDict() for block in blocks], safe=False)


def getBlock(request, blockPk):
    block = Block.objects.get(pk=blockPk)
    blockDic = block.getDict()
    return render(request, "../templates/tab.html", {
        "type": "block",
        "items":block.elements.all().order_by('position')
    })





class BlocksView(View):

    def get(self, request):
        baseActions = BaseAction.objects.all()
        baseActionsDatas = []
        for elem in baseActions:
            baseActionsDatas.append(elem.getDict())

        blocks = Block.objects.filter(user_id=request.user.id)

        return render(request, "../templates/blocks.html", {
            "baseActions": baseActions,
            "blocks": blocks,
            "baseblock": [],
            "baseActionsData": json.dumps(baseActionsDatas),
        })

    def post(self, request):
        self.get(request)