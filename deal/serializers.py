from rest_framework import serializers
from deal.models import Deal


class DealSerializer(serializers.Serializer):

    def create(self, validated_data):
        return Deal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.item_count = validated_data.get('item_count', instance.item_count)
        instance.deal_price = validated_data.get('deal_price', instance.deal_price)
        instance.end_time = validated_data.get('end_time', instance.name)

        instance.save()
        return instance

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    item_count = serializers.IntegerField(default=0)
    deal_price = serializers.IntegerField(default=0, read_only=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
