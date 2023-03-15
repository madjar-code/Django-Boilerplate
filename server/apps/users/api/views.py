from rest_framework import status
from rest_framework.generics import\
    GenericAPIView, UpdateAPIView
from rest_framework.permissions import\
    AllowAny, IsAuthenticated
from rest_framework.parsers import\
    MultiPartParser, FormParser, JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import *


class RegisterAPIView(GenericAPIView):
    """Register user"""
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = RegisterSerializer
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    """Login user"""
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = LoginSerializer
    
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, queryset=None) -> User:
        object = self.request.user
        return object

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
