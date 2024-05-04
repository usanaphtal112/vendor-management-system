from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from .serializers import UserLoginSerializers


@extend_schema(
    description="JWT Authentication token",
    tags=["Users"],
)
class TokenObtainView(APIView):
    serializer_class = UserLoginSerializers  # Specify the serializer class

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            User = get_user_model()
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                access_token = AccessToken.for_user(user)
                return Response(
                    {"access": str(access_token)}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
