from rate.api.serializers import RateSerializer
from rate.models import Rate

from rest_framework import viewsets


class RateAPIViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all().order_by('-id')
    serializer_class = RateSerializer

# class RateListAPIView(generics.ListCreateAPIView):
#     queryset = Rate.objects.all().order_by('-id')
#     serializer_class = RateSerializer
#
#
# class RateAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rate.objects.all().order_by('-id')
#     serializer_class = RateSerializer
