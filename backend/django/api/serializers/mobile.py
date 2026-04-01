from rest_framework import serializers


class MobileCheckSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        max_length=15,
        required=True
    )

    def validate_mobile_number(self, value):
        """Validate mobile number format with Indian-specific rules"""
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits"
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Mobile number must be 10 digits"
            )

        # Indian mobile numbers start with 6, 7, 8, or 9
        if value[0] not in ['6', '7', '8', '9']:
            raise serializers.ValidationError(
                "Invalid mobile number format"
            )

        # Prevent obvious fake numbers
        if len(set(value)) == 1:
            raise serializers.ValidationError(
                "Invalid mobile number"
            )

        return value
