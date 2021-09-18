from django.contrib import admin

# Register your models here.
from AAPyppeteer.models import Question, BaseAction, DataBlockType, DataBlock

admin.site.register(Question)
admin.site.register(BaseAction)
admin.site.register(DataBlockType)
admin.site.register(DataBlock)