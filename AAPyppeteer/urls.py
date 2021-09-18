from django.contrib.auth.decorators import login_required
from django.urls import path, include

from AAPyppeteer.views import views, projectViews, blockViews, actionViews, datasViews

urlpatterns = [
    path('', views.index, name='index'),


    path('accounts/', include('django.contrib.auth.urls')),

    path('signup/', views.SignUpView.as_view(), name='signup'),

    # projects
    path('new_project/', login_required(views.newProject), name='new_project'),
    path('project_del/<int:pk>', login_required(views.delProject), name='project_delete'),
    path('projects', login_required(views.ProjectsView.as_view()), name='projects'),

    #project
    path('project/<int:pk>', login_required(projectViews.ProjectView.as_view()), name='project'),
    path('addblock_project/<int:projectPk>', login_required(projectViews.addBlockToProject), name='addblock_project'),
    path('delblock_project/<int:projectPk>/<int:blockPk>', login_required(projectViews.deleteBlockProject), name='delblock_project'),
    path('getblocksproject/<int:projectPk>', login_required(projectViews.getBlocksProject), name='getblocks_project'),
    path('runproject/<int:projectPk>', login_required(projectViews.runProject), name='runproject'),

    #block
    path('blocks', login_required(blockViews.BlocksView.as_view()), name='blocks'),
    path('updateblock/<int:blockPk>', login_required(blockViews.updateBlock), name='updateblock'),
    path('addblock', login_required(blockViews.addBlock), name='addblock'),
    path('getblocks', login_required(blockViews.getBlocks), name='getblocks'),
    path('getblock/<int:blockPk>', login_required(blockViews.getBlock), name='getblock'),
    path('delblock/<int:blockPk>', login_required(blockViews.delBlock), name='delblock'),

    #action
    path('addaction/<int:blockPk>/<int:baseActionPk>', login_required(actionViews.addAction), name='addaction'),
    path('updateaction/<int:actionPk>', login_required(actionViews.updateAction), name='updateaction'),
    path('deleteaction/<int:blockPk>/<int:actionPk>', login_required(actionViews.deleteAction), name='deleteaction'),
    path('updateactionorder/<int:blockPk>', login_required(actionViews.updateActionOrder), name="updateactionorder"),

    #data
    path('datas', datasViews.datasBlockView, name='datas'),
    path('updatedata/<int:dataPk>', datasViews.updateData, name='updatedata'),
    path('adddata', datasViews.addData, name='adddata'),

# other
    path('documentation', views.documentation, name='documentation'),
    path('exemples', views.exemples, name='exemples'),

]



