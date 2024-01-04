from datetime import datetime

from django.contrib.auth.models import User
from django.utils.timezone import make_aware, now
from rest_framework import serializers
from deal.models import Deal


class DealSerializer(serializers.Serializer):
    # def __init__(self, *args, **kwargs):
    #     super(DealSerializer, self).__init__(*args, **kwargs)
    #
    #     # Check if it's an update operation
    #     if self.instance is not None:
    #         self.fields['name'].required = False
    #         self.fields['start_time'].required = False

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    item_count = serializers.IntegerField(default=0)
    deal_price = serializers.IntegerField(read_only=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Deal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.item_count = validated_data.get('item_count', instance.item_count)
        instance.deal_price = validated_data.get('deal_price', instance.deal_price)
        instance.end_time = validated_data.get('end_time', instance.end_time)

        instance.save()
        return instance

    def is_valid(self, raise_exception=False):

        self.initial_data = self.validate_and_preprocess_timestamps()
        super_valid = super(DealSerializer, self).is_valid(raise_exception=raise_exception)

        return super_valid

    def validate_and_preprocess_timestamps(self):

        data = self.initial_data

        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Convert timestamps to datetime objects if they exist
        if start_time:
            start_time = make_aware(datetime.fromtimestamp(start_time))
            data['start_time'] = start_time  # Update the data dictionary

        if end_time:
            end_time = make_aware(datetime.fromtimestamp(end_time))
            data['end_time'] = end_time  # Update the data dictionary

        # Validate start time only during creation
        if self.instance is None:  # This means it's a create operation
            # Check if start_time is greater than current time
            if start_time and start_time < now():
                raise serializers.ValidationError({
                    'start_time': "Start time must be greater than the current time."
                })

            # Check if start_time is less than end_time
            if start_time and end_time and start_time >= end_time:
                raise serializers.ValidationError({
                    'start_time': "Start time must be less than end time."
                })

        # Validate end time for both create and update operations
        if end_time and end_time < now():
            raise serializers.ValidationError({
                'end_time': "End time must be greater than the current time."
            })

        return data


class UserSerializer(serializers.ModelSerializer):

    deals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'deals']

    def get_deals(self, obj):

        user = self.context['request'].user
        if user.is_authenticated:
            deals = Deal.objects.filter(owner=user)
            return DealSerializer(deals, many=True).data
        return []
