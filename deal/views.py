from datetime import datetime
import pytz

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from deal.models import Deal
from deal.serializers import DealSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def deal_list(request):
    if request.method == "GET":
        deals = Deal.objects.all()
        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data, )

    if request.method == "POST":

        timezone = pytz.timezone('Asia/Kolkata')

        request.data["end_time"] = datetime.fromtimestamp(request.data.get("end_time"), timezone)
        request.data["start_time"] = datetime.fromtimestamp(request.data.get("start_time"), timezone)

        serializer = DealSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def deal_detail(request, pk):
    try:
        deal = Deal.objects.get(pk=pk)
    except Deal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        serializer = DealSerializer(deal)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = DealSerializer(Deal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        deal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
