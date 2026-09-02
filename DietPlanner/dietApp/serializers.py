from rest_framework import serializers
from dietApp.models import User,Profile


class UserSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','phone','password1','password2']
        read_only_fields=['password']

    def create(self, validated_data):
        password1=validated_data.pop("password1")
        password2=validated_data.pop("password2")
        if password1!=password2:
            raise serializers.ValidationError("password mismatch")
        return User.objects.create_user(**validated_data,password=password1)   

class ProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Profile
        fields="__all__"
        read_only_fields=['id','user','daily_calorie_goal','bmi','created_at']
