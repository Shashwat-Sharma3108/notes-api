from users.models import User
from users.serializers import CustomUserSerializer
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        existing_user = User.objects.filter(Q(username=request.data.get("username"))| Q(email=request.data.get("email"))).exists()
        if existing_user:
            return Response({"error":"Email or Username Already in use"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return super(UserCreateAPIView, self).create(request, *args, **kwargs)