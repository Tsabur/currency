from rate.models import Rate

from rest_framework import serializers


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = (
            'id',
            'created',
            'source',
            'get_source_display',
            'currency',
            'get_currency_display',
            'buy',
            'sale',
        )
