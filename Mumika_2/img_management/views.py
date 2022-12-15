from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
import base64
from img_management.models import Tag, ImageInfo
from img_management.constant import PAGE_IMG_LIMIT

def get_page_images(target_queryset, page_number=1):
    if page_number < 1:
        raise ValueError('page_number must be greater than 0')
    else:
        paginator = Paginator(target_queryset, PAGE_IMG_LIMIT)
        page_obj = paginator.get_page(page_number)

        image_data_summary = []
        for img_obj in page_obj.object_list:
            with open(img_obj.path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

                image_data_summary.append({
                    'name':img_obj.name, 
                    'base64_data':image_data
                })

        return {
            'total_page':paginator.num_pages,
            'page': page_obj.number, 
            'img_objs': image_data_summary
        }

def render_homepage(request):
    return render(request, 'homepage.html', {})

def get_images(request):
    img_queryset = ImageInfo.objects.all().order_by('id')

    # the min page is 1
    page_number = request.GET.get('page', 1)
    json_response = get_page_images(img_queryset, page_number)

    return JsonResponse(json_response)

def test(request):

    return JsonResponse({'test': 'test'})


