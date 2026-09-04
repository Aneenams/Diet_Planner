from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListCreateAPIView,ListAPIView,DestroyAPIView
from dietApp.serializers import UserSerializer,ProfileSerializer,FoodLogSerializer
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from dietApp.models import FoodLog
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


class UserRegisterView(CreateAPIView):
    serializer_class=UserSerializer


class ProfileCreateListView(CreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]  
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ProfileSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

# class ProfileDetailView(APIView):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

#     def get(self,request,*args,**kwargs):
#         user_instance=request.user
#         profile_instance=user_instance.user_profile
#         print(user_instance)
#         print(profile_instance)
#         serializer=ProfileSerializer(profile_instance)
#         return Response(serializer.data)

class ProfileDetailView(RetrieveAPIView,UpdateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ProfileSerializer

    def get_object(self):
        return self.request.user.user_profile
        
class FoodLogCreateListView(CreateAPIView,ListAPIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=FoodLogSerializer
    # queryset=FoodLog.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)       




    # def get(self,request,*args,**kwargs):
    #     user_instance=request.user
    #     food_list=user_instance.food_log.all()
        #   FoodLog.objects.filter(user=user_instance)  
    #     serializer=FoodLogSerializer(food_list,many=True)
    #     return Response(data=serializer.data)

    def get_queryset(self):
        cur_date=timezone.now().date()
        print(cur_date)
        yesterday=cur_date-timedelta(days=1)
        print(yesterday)
        
        seven_day=cur_date-timedelta(days=7)  

        params=self.request.query_params
        # return FoodLog.objects.filter(user=self.request.user,created_at=cur_date)
        # return self.request.user.food_log.all()
        if "start_date" and "end_date" in self.request.query_params:
            start_date=self.request.get("start_date")
            end_date=self.request.get("end_date")
            return self.request.user.food_log.filter(created_at__date__gte=start_date,created_at__date__lte=end_date)
        if "filter_type" in params:
            if params['filter_type']=="yesterday":
                return self.request.user.food_log.filter(created_at__date=yesterday)

            elif params['filter_type']=="seven_day":
                return self.request.user.food_log.filter(created_at__date__gte=seven_day,created_at__date__lte=cur_date)    
        return self.request.user.food_log.filter(created_at__date=cur_date)
    


# class FoodLogDetailView(APIView):


#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("id")      
#         food=FoodLog.objects.get(id=id)
#         serializer=FoodLogSerializer(food)
#         return Response(data=serializer.data)


class FoodLogDetailView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    # authentication_classes=[authentication.TokenAuthentication]
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=FoodLogSerializer
    queryset=FoodLog.objects.all()