from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from img_management.models import Tag, ImageInfo
from img_management.constant import PAGE_IMG_LIMIT

class ImgMainView(View):
    template_name = 'homepage.html'
    def get(self, request):
        img_list = ImageInfo.objects.all()
        paginator = Paginator(img_list, PAGE_IMG_LIMIT)

        # the min page is 1
        page_number = request.GET.get('page', 1)
        page_objs = paginator.get_page(page_number)
        return render(request, self.template_name, {'img_list': page_objs})

    def post(self, request):
        return JsonResponse({'test': 'test'})
