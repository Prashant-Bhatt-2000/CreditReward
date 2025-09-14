from rest_framework import serializers
from .models import CreditModel

class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditModel
        fields = ['credit_type', 'amount']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        credit = CreditModel.objects.create(user=user, **validated_data)
        return credit

class CreditViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditModel
        fields = [
            'id', 'user', 'credit_type', 'amount', 'repayment_amount', 
            'status', 'created_at', 'credit_repayment_date'
        ]
        read_only_fields = ['id', 'user', 'repayment_amount', 'status', 'created_at', 'credit_repayment_date']
