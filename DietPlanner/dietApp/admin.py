from django.contrib import admin
from dietApp.models import User,Profile,FoodLog,Subscription
# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(FoodLog)
admin.site.register(Subscription)