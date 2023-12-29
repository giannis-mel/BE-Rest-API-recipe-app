"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

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

    def update(self, instance, validated_data):
        """Update and return user.

        This method handles the updating of an existing user instance.
        It allows for updating fields specified in the validated_data.
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        # If 'password' is included in the update, encrypt and save it
        if password:
            user.set_password(password)
            user.save()

        return user


# Serializer that is not linked to a specific model
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token.

    This method attempts to authenticate the user with the provided email and password.
    If authentication is successful, the user object is added to the serialized attributes.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
