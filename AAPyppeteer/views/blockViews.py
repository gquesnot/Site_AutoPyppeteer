import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from AAPyppeteer.models import BlockConfigured, Block, Project, BaseAction, Action


def updateActionOrder(request, blockPk):
    newOrder = json.loads(request.POST['datas'])
    block = Block.objects.get(pk=blockPk)


    for el in newOrder:
        id_ = el['id']
        pos = el['position']

        for action in block.elements.all():
            if id_ == action.id and pos != action.position:
                action.position = pos
                action.save()

    return JsonResponse(block.getDict(), safe=False)

def updateActionBlock(request, actionPk):
    action = Action.objects.get(pk=actionPk)
    answers = action.elements.all()

    for answer in answers:
        for k ,v in request.POST.items():

            if k == "csrfmiddlewaretoken":
                continue
            else:

                if k == str(answer.pk):
                    print(answer.pk, k, v)
                    if answer.name == "name":
                        action.name = v
                    answer.value = v
                    answer.save()
    action.save()
    return JsonResponse(action.getDict(), safe=False)

def addBlock(request):
    block = Block(name=request.POST['name'], user_id=request.user)
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