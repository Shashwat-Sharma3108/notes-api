from django.urls.conf import path
from users.views import UserCreateAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("signup/", UserCreateAPIView.as_view(), name='create-user'),
]

#ENDPOINTS FOR Accessing Tokens
urlpatterns += [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]