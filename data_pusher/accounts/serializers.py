from rest_framework import serializers
from .models import Account, Destination

from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id', 'email', 'account_name', 'app_secret_token', 'website']


class DestinationSerializer(serializers.ModelSerializer):
    account_id = serializers.UUIDField()

    class Meta:
        model = Destination
        fields = ['id', 'account_id', 'url', 'http_method', 'headers']

    def validate_http_method(self, value):
        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']
        if value not in allowed_methods:
            raise serializers.ValidationError(f"HTTP method must be one of: {', '.join(allowed_methods)}.")
        return value

    def create(self, validated_data):
        account_id = validated_data.pop('account_id')  # Extract account_id
        try:
            account = Account.objects.get(account_id=account_id)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"account_id": "Account not found."})

        # Create and return the Destination object
        return Destination.objects.create(account=account, **validated_data)
