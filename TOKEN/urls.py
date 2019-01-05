from django.contrib import admin
from django.urls import path,include
from app import views
from rest_framework import routers
from app import views



createUserViewRouter = routers.DefaultRouter() # 新增用户
createUserViewRouter.register('', views.createUser,)

getUserRouter = routers.DefaultRouter() # 查看用户列表
getUserRouter.register('', views.getUser,)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('gettoken/',views.loginView.as_view()), # 获取 token
    path('createuser/',include(createUserViewRouter.urls)), # 新增用户
    path('getuser/',include(getUserRouter.urls)), # 新增用户
]
