from rest_framework import serializers
from .models import Metrics

class MetricsSerializer(serializers.Serializer):
    metric = serializers.CharField(max_length=120)
    reference = serializers.CharField(max_length=120)
    alert = serializers.BooleanField()
    date_metric = serializers.DateTimeField()

    def create(self, validated_data):
        return Metrics.objects.create(**validated_data)