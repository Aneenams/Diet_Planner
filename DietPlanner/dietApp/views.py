from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from dietApp.serializers import UserSerializer,ProfileSerializer
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class UserRegisterView(CreateAPIView):
    serializer_class=UserSerializer


class ProfileCreateListView(CreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]  
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ProfileSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class ProfileDetailView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        user_instance=request.user
        profile_instance=user_instance.user_profile
        print(user_instance)
        print(profile_instance)
        serializer=ProfileSerializer(profile_instance)
        return Response(serializer.data)

    
        