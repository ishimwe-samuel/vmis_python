from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'orgunitname', 'parentorgunitname',)


# register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'surname', 'phone_number', 'orgunitid', 'orgunitname',
                  'orgunitlevel', 'parentorgunitid', 'parentorgunitname', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            surname=validated_data['surname'],
            phone_number=validated_data['phone_number'],
            orgunitid=validated_data['orgunitid'],
            orgunitname=validated_data['orgunitname'],
            orgunitlevel=validated_data['orgunitlevel'],
            parentorgunitid=validated_data['parentorgunitid'],
            parentorgunitname=validated_data['parentorgunitname'],
        )
        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print(data)
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorect credentials")


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, validated_data):
        print(validated_data)
        data = validated_data['data'].get('email', '')
        try:
            user = User.objects.get(email=data)
            if user and user.is_active:
                # uidb64=urlsafe_base64_encode(user.id)
                token=PasswordResetTokenGenerator().make_token(user)
                absurl=f'http://127.0.0.1?token={token}'
                # relativeLink=reverse('email-verify')
                email_body=f"Hi {user.username} here is you password reset link {absurl}"
                return user
            else:
                raise serializers.ValidationError("Account is not activated")

        except ObjectDoesNotExist:
            print("Does not exists")
            raise serializers.ValidationError("No such email found")
