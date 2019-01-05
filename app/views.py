from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app import models
from django.contrib.auth import login
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.shortcuts import Http404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


"""1. 登陆"""
class loginView(APIView):
    """登陆成功后,获取TOKEN"""
    def post(self,request):
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if not user:
            raise Http404("账号密码不匹配")
        login(request, user)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({ "success": True, "msg": "登录成功","results": token},status=status.HTTP_200_OK)


"""2. 新增玩家"""
class UserSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ["username","password",]
    def create(self, validated_data):
        user= models.UserProfile.objects.create_user(**validated_data) # 这里新增玩家必须用create_user,否则密码不是秘文
        return user

class createUser(mixins.CreateModelMixin,GenericViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = UserSerializer


"""3. 获取用户列表(验证token)"""

class getUser(mixins.ListModelMixin,GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.UserProfile.objects.all()
    serializer_class = UserSerializer

