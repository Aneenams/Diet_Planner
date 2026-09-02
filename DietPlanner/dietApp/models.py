from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal

# Create your models here.
class User(AbstractUser):
    phone=models.CharField(max_length=15,unique=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    GENDER_OPTIONS=(
        ('male','male'),
        ('female','female'),
        ('others','others')
    )
    ACTIVITY_LEVEL_CHOICES=(
        ('sedentary','sedentary'),
        ('light','light'),
        ('moderate','moderate'),
        ('active','active'),
        ('very_active','very_active')
    )
    GOAL_CHOICES=(
        ('weight_loss','weight_loss'),
        ( 'weight_gain','weight_gain'),
        ('maintenance','maintenance')
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_profile")
    age=models.PositiveIntegerField()
    gender=models.CharField(max_length=20,choices=GENDER_OPTIONS)
    weight=models.DecimalField(max_digits=5,decimal_places=2,help_text="weight in kg")
    height=models.DecimalField(max_digits=5,decimal_places=2,help_text="height in meter")
    target_weight=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    duration= models.PositiveIntegerField(validators=[MinValueValidator(1)],null=True,blank=True)
    activity_level=models.CharField(max_length=50,choices=ACTIVITY_LEVEL_CHOICES)
    goal=models.CharField(max_length=50,choices=GOAL_CHOICES)
    daily_calories_goal=models.PositiveIntegerField(null=True,blank=True)
    profile_pic=models.ImageField(upload_to="media",null=True,blank=True)   #pip install pillow
    bmi=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-created_at"]

    def save(self,*args,**kwargs):
    #-----------------------------------
    #           BMI
    #-----------------------------------
        if self.weight and self.height:
            self.bmi=self.weight/(self.height**2)
    #-----------------------------------
    #           BMR
    #-----------------------------------
        weight=self.weight
        height_in_cm=self.height*100
        age=self.age

        if self.gender=="male":
            bmr=((10*weight)+(Decimal(6.25)*height_in_cm)-(5*age)+5)

        elif self.gender=="female":
            bmr=((10*weight)+(Decimal(6.25)*height_in_cm)-(5*age)-161)    

    #--------------------------
    #      activity factors
    #----------------------------

        activity_factors = {
                "sedentary": 1.2,
                "light": 1.375,
                "moderate": 1.55,
                "active": 1.725,
                "very_active": 1.9
            }
         #tdee=bmr*activity_factors
        activity=self.activity_level
        tdee=Decimal(bmr)*Decimal(activity_factors.get(activity))
        #---------------------------------
        #           daily calorie goal
        #----------------------------------

        if self.goal=="weight_loss":
            self.daily_calories_goal=tdee-500
        elif self.goal=="weight_gain":
            self.daily_calories_goal=tdee+500
        elif self.goal=="maintenance":
            self.daily_calories_goal=tdee 
        super().save(*args,**kwargs)

        
    def __str__(self):
        return f"{self.user.username} profile"    


class FoodLog(models.Model):
    MEAL_TYPE_CHOICES=(
        ('break fast','break fast'),
        ('lunch','lunch'),
        ('dinner','dinner'),
        ('snack','snack')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="food_log")
    title=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to="food",null=True,blank=True)
    meal_type=models.CharField(max_length=30,choices=MEAL_TYPE_CHOICES)
    quantity=models.CharField(max_length=100,null=True,blank=True)
    calories=models.PositiveIntegerField(null=True,blank=True)
    protien=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    consumed_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return f"{self.user.username}--{self.meal_type}"




class Subscription(models.Model):
    STATUS_CHOICES=(
        ('active','active'),
        ('expired','expired')
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="membership")
    amount=models.DecimalField(max_digits=8,decimal_places=2,default=300)
    payment_date=models.DateField(default=timezone.now)
    end_date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES,default='active')

    def save(self,*args,**kwargs):
        self.end_date=self.payment_date+timedelta(days=28)
        super().save(*args,**kwargs)

    def __atr__(self):
        return self.user.username    






