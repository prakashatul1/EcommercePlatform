from datetime import datetime
import pytz
from django.contrib.auth.models import User

from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from deal.models import Deal
from deal.permissions import IsOwnerOrReadOnly
from deal.serializers import DealSerializer, UserSerializer


class DealList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, format=None):
        deals = Deal.objects.all()
        serializer = DealSerializer(deals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
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


class UserList(generics.ListAPIView):

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
