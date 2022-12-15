from django.shortcuts import render
from django.http import JsonResponse
# import jsonresponse


# Create your views here.
def test_view(request):
    return render(request, 'homepage.html', {})
    # return JsonResponse({'test': 'test'})