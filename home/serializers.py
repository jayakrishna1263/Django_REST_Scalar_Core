from .models import *

from django.contrib.auth.models import User


from rest_framework import serializers

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields=['color_name','id']

class PeopleSerializer(serializers.ModelSerializer):
    color=ColorSerializer()
    # color_info= serializers.SerializerMethodField()
    class Meta:
        model=Person
        fields="__all__"
        #exclude=['name']
        #fields=['name','age']
        # depth=1
        
    # def validate(self,data):  # Here data=[id,name,age]
    #     if data['age']<18:
    #         raise serializers.ValidationError("age should be greater than 18")
    #     return data
    # def validate_age(self,data):   #Here data=age
    #     if data<18:
    #         raise serializers.ValidationError("age should be greater than 18")
    #     return data
    def validate(self,data):  # Here data=[id,name,age]
        special_characters="!@#$%^&*()-+=<>?/_"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError("Name should not contain special chars")
        
        if data['age']<18:
            raise serializers.ValidationError("age should be greater than 18")
        return data
    
    #serializer method fields
    # def get_color_info(self,obj):
    #     color_obj=Color.objects.get(id=obj.color.id)
    #     return {'color_name':color_obj.color_name,'hex_code':'#000'}


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    
    
    
    
class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    
    def validate(self,data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username is taken")
    
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email is taken")
        return data
    def create(self, validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data 
        
 
 
 
 
 
 
 
    