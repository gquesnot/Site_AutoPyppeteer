import json

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Question(models.Model):
    name = models.CharField(max_length=200)
    ask = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def getDict(self):
        return {
            "name": self.name,
            "ask": self.ask,
            "type": self.type
        }

    def __str__(self):
        return f"name: {self.name}, ask: {self.ask}, type: {self.type}"


class Answer(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def getDict(self):
        return {"id": self.pk, "value": self.value, "name": self.name, "question": self.question.getDict()}

    def __str__(self):
        return f"name: {self.name}, value: {self.value}, question : {str(self.question)}"


class BaseAction(models.Model):
    name = models.CharField(max_length=200)
    elements = models.ManyToManyField(Question)

    def getDict(self):
        res = {"id": self.id, "name": self.name, "questions": []}
        for question in self.elements.all().values():
            tmp = {}
            for k, v in question.items():
                tmp[k] = v
            res['questions'].append(tmp)
        return res

    def __str__(self):
        questions = '\n'.join([str(question) for question in self.elements.all()])
        return f"name: {self.name} | question: {questions}"


class Action(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    elements = models.ManyToManyField(Answer)

    def __str__(self):
        answers = '\n'.join([str(answer) for answer in self.elements.all()])

        return f"name: {self.name} | type: {self.type} | answer: {answers}"

    def getDict(self):
        res = {"id": self.pk, "type": self.type, "name": self.name, "position": self.position, "answers": []}
        for answer in self.elements.all():
            res['answers'].append(answer.getDict())

        return res


class Block(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    elements = models.ManyToManyField(Action)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def getDict(self):
        res = {
            "id": self.pk,
            "name": self.name,
            "description": self.description,
            "elements": [action.getDict() for action in self.elements.all().order_by('position')],
            "user_id": self.user_id.pk
        }
        return res

    def all(self):
        self.actions = self.elements.all().order_by('position')
        return self

    @property
    def __str__(self):
        blockConfig = '\n'.join([str(action) for action in self.elements.all()])
        return f"name: {self.name}, description: {self.description}, blockConfig: {blockConfig}"


class DataBlockType(models.Model):
    name = models.CharField(max_length=200)
    datas = models.JSONField(default=dict)
    requireFile = models.BooleanField(default=False)
    io = models.CharField(max_length=200, default="in")
    value = models.CharField(max_length=200, default="")


    def all(self):
        self.datasDecoded = json.loads(self.datas)
        return self

    def getDict(self):
        return {"name": self.name, "datas": self.datas, "requireFile": str(self.requireFile), "io": self.io, "value": self.value}


class DataBlock(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(DataBlockType, on_delete=models.CASCADE, blank=True, null=True)
    #datasType = models.CharField(max_length=200, default="")
    datas = models.JSONField(default=dict)
    path= models.CharField(max_length=200,default="")

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def all(self):
        self.answersDecoded = json.loads(self.datas)
        return self

    def getDict(self):
        tmp = {
            "name": self.name,
            "type": self.type.getDict(),
            "datas": self.datas,
            "path": self.path
        }
        return tmp


class BlockConfigured(models.Model):
    name = models.CharField(max_length=200)
    isAdvanced = models.BooleanField(default=False)
    datasIn = models.ForeignKey(DataBlock, on_delete=models.CASCADE, blank=True, null=True, related_name="datasIn")
    datasOut = models.ForeignKey(DataBlock, on_delete=models.CASCADE, blank=True, null=True, related_name="datasOut")
    block = models.ForeignKey(Block, on_delete=models.CASCADE, blank=True, null=True)
    nbThread = models.IntegerField(default=0)
    datas = models.JSONField(default=dict)

    isLinkedToNext = models.BooleanField(default=False)

    def getDict(self):
        res = {
            "id": self.pk,
            "name": self.name,
            "datasIn": self.datasIn.getDict() if self.datasIn is not None else None,
            "datasOut": self.datasOut.getDict() if self.datasOut is not None else None,
            "datas": self.datas,
            "nbThread": self.nbThread,
            "isAdvanced": self.isAdvanced,
            "block": self.block.getDict(),
            "isLinkedToNext": self.isLinkedToNext,
        }

        return res


class ImageProject(models.Model):
    name = models.CharField(max_length=200)
    name_pk = models.CharField(max_length=200)
    path = models.CharField(max_length=200)

    def getDict(self):
        return {
            "name_pk": self.name_pk,
            "name": self.name_pk.split("_")[0],
            "path": self.path
        }


class Project(models.Model):
    name = models.CharField(max_length=200)
    blocks = models.ManyToManyField(BlockConfigured, related_name='blocks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datasOutUrl = models.JSONField(default=list)
    images = models.ManyToManyField(ImageProject, related_name='imagesProject')

    def getDict(self):
        res = {"id": self.id, "name": self.name, "datasOutUrl": self.datasOutUrl}

        if self.blocks is not None:
            res['blocks'] = [block.getDict() for block in self.blocks.all()]
        else:
            res['blocks'] = []

        if self.images is not None:
            res['images'] = [image.getDict() for image in self.images.all()]
        else:
            res['images'] = []

        return res

    def __str__(self):
        return f"name : {self.name}"
