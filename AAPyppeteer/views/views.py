from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from AAPyppeteer import models
from AAPyppeteer.models import BaseAction, Project


def index(request):
    return render(request, "../templates/index.html", {
        "user": request.user
    })


def delProject(request, pk):
    project = Project.objects.get(pk=pk)
    if project.user == request.user:
        project.delete()
    return ProjectsView().get(request)



class ProjectsView(View):

    def get(self, request):
        baseActions = BaseAction.objects.all()
        projects = Project.objects.filter(user_id=request.user.id)

        return render(request, "../templates/projects.html", {
            "projects": projects

        })

    def post(self, request):
        pass

def newProject(request):
    project = models.Project(name=request.POST['projectname'], user_id=request.user.pk)
    project.save()
    return redirect("project", project.pk)

class SignUpView(View):
    def get(self, request):
        return render(request, "../templates/registration/signup.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if username and password and email:
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.save()
            return render(request, "../templates/registration/login.html")
        return render(request, "../templates/registration/signup.html")


def documentation(request):
    return render(request, "../templates/documentation.html")


def exemples(request):
    return render(request, "../templates/exemples.html")


