from rest_framework import serializers
from .models import User as CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'is_superuser', 'first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_superuser = validated_data.pop('is_superuser', False)
        
        if is_superuser:
            user = CustomUser.objects.create_superuser(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password']
            )
        else:
            user = CustomUser.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password']
            )
        return user