from django.db.models import Prefetch, F, Sum
from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only(
                     'company_name',
                     'user__email'))
    ).annotate(price=F('service__full_price') -
                     F('service__full_price') * F('plan__discount_percent') / 100)
    serializer_class = SubscriptionSerializer

