from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NGO, Restaurant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NGO, Restaurant

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('restaurant', 'Restaurant'), ('ngo', 'NGO')], write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract role before popping it out
        role = validated_data.pop('role')

        # Create the User instance
        user = User.objects.create_user(**validated_data)

        # Assign the user to the correct table based on the role
        if role == 'ngo':
            NGO.objects.create(user=user, name=user.username, email=user.email)
        elif role == 'restaurant':
            Restaurant.objects.create(user=user, name=user.username, email=user.email)

        return user

