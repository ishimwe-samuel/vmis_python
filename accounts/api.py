from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer, RequestPasswordResetSerializer
# Register API


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
# Login API


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class RequestPasswordResetAPI(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        data={'request':request,'data':request.data}
        # serializer = self.get_serializer(data=request.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "email": UserSerializer(user, context=self.get_serializer_context()).data,
        })
