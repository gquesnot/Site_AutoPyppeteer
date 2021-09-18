import json

from django.http import JsonResponse

from AAPyppeteer.models import Action, Block, BaseAction, Question, Answer


def updateAction(request, actionPk):
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


def addAction(request, blockPk, baseActionPk):

    block = Block.objects.get(pk=blockPk)
    print(request.POST)
    type_ = BaseAction.objects.get(pk=baseActionPk).name
    action = Action(name=request.POST['name'], type=type_, position=len(block.elements.all()))
    action.save()
    answerList = []

    for id_, value in json.loads(request.POST['answers']).items():
        print(id_, value)
        question = Question.objects.get(pk=int(id_))
        newAnswer = Answer(value=value, question=question, name=question.name)
        newAnswer.save()
        action.elements.add(newAnswer)
    action.save()

    block.elements.add(action)
    block.save()
    return JsonResponse(block.getDict(), safe=False)


def deleteAction(request, blockPk, actionPk):
    print("block", blockPk, "| action", actionPk)
    action = Action.objects.get(pk=actionPk)
    block = Block.objects.get(pk=blockPk)
    block.elements.remove(action)
    block.save()
    action.delete()
    return JsonResponse(block.getDict(), safe=False)


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