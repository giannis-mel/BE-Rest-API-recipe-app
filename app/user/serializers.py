"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # Meta class defines the model and fields for serialization.
    # 'password' field is marked as write-only and requires a minimum
    # length of 5 characters.
    class Meta:
        model = get_user_model()
        # Specify fields to be included in the serialized output
        fields = ('email', 'password', 'name')
        # Set additional constraints for the 'password' field
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # Create and return a user with an encrypted password.
    # This method is called after successful validation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
