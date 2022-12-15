from django.shortcuts import render
from django.http import JsonResponse
# import jsonresponse


# Create your views here.
def test_view(request):
    return JsonResponse({'test': 'test'})