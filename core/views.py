from django.shortcuts import render
from core.models import Buyer
from django.views.decorators.csrf import csrf_exempt
from core.decorators import measure_view


@csrf_exempt
@measure_view
def buyers_list(request):
    return {'buyers': [buyer.to_dict for buyer in Buyer.objects.all()]}

