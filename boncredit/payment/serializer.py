from rest_framework import serializers
from .models import PaymentModel

class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    credit_id = serializers.UUIDField(source='credit.id', read_only=True)

    class Meta:
        model = PaymentModel
        fields = [
            'id',
            'user',
            'user_email',
            'credit',
            'credit_id',
            'amount',
            'payment_date',
            'status',
        ]
        read_only_fields = ['id', 'payment_date', 'status', 'user_email', 'credit_id']

    def create(self, validated_data):
        return super().create(validated_data)
