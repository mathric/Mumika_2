from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from img_management.models import Tag, ImageInfo
from img_management.constant import PAGE_IMG_LIMIT


class ImgMainView(View):
    template_name = 'homepage.html'
    def get(self, request):
        action = request.GET.get('action', None)
        if action is None:
            return render(request, self.template_name, {})

        elif action == 'GET_IMAGES':
            img_list = ImageInfo.objects.all().order_by('id')
            paginator = Paginator(img_list, PAGE_IMG_LIMIT)

            # the min page is 1
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            import base64
            image_data_summary = []
            for img_obj in page_obj.object_list:

                with open(img_obj.path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

                    image_data_summary.append({
                        'name':img_obj.name, 
                        'base64_data':image_data
                    })

            return JsonResponse({
                'total_page':paginator.num_pages,
                'page': page_obj.number, 
                'img_objs': image_data_summary
            })

    def post(self, request):
        return JsonResponse({'test': 'test'})


