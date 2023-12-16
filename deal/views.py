from datetime import datetime
import pytz

from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from deal.models import Deal
from deal.serializers import DealSerializer


class DealList(APIView):

    def get(self, request, format=None):
        deals = Deal.objects.all()
        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DealSerializer(data=request.data)
        import ipdb
        ipdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_object(pk):
    try:
        return Deal.objects.get(pk=pk)
    except Deal.DoesNotExist:
        raise Http404


class DealDetail(APIView):

    def get(self, request, pk, format=None):
        deal = get_object(pk)
        serializer = DealSerializer(deal)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        deal = get_object(pk)
        serializer = DealSerializer(deal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        deal = get_object(pk)
        deal.delete()
        return Response({'message': 'Deal successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

