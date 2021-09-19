import json

from django.http import JsonResponse

from AAPyppeteer.models import Action, Block, BaseAction, Question, Answer





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


