from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import base64
from img_management.models import Tag, ImageInfo
from img_management.constant import PAGE_IMG_LIMIT, IMAGE_FORMAT
import os
import glob
from pathlib import Path
import json
import logging
from logging import getLogger

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

# This only import the file path related stuff by reading the file system
def import_images(request):
    dir_path = request.GET.get('dir_path', None)

    # get all image file recursive under folder
    if dir_path:
        file_list = []
        glob_search_path = dir_path + '/**/'
        for file_type in IMAGE_FORMAT:
            file_list.extend(glob.glob(f'{glob_search_path}*.{file_type}',recursive=True))

        image_info_bulk_prepare = []
        for file_full_path in file_list:
            path = Path(file_full_path)
            image_info_bulk_prepare.append(ImageInfo(
                                                filepath=file_full_path, 
                                                filename=path.stem,
                                                filetype=path.suffix
                                            ))
        ImageInfo.objects.bulk_create(
            image_info_bulk_prepare,
            ignore_conflicts=True,
            unique_fields=['filepath']
        )
    
    return JsonResponse({'status': 'success'})


# import image related info from json file
@api_view(['POST'])
def import_img_info_api(request):
    json_path = request.data.get('json_path', None)
    json_response = import_img_info(json_path)
    return JsonResponse(json_response)


def import_img_info(json_path=None):
    json_data = {}
    logger = getLogger('app')
    if json_path:
        try:
            with open(json_path) as f:
                json_data = json.load(f)
        except json.JSONDecodeError:
            return {'status': 'fail', 'message': 'json decode error'}
        else:
            for item in json_data.get('itemList', []):
                # if not found filename property, use id property
                file_name = item.get('filename', '')
                if file_name == '':
                    file_name = item.get('id', '')
                    if file_name == '':
                        continue
                try:
                    img_ref = ImageInfo.objects.get(filename=file_name)
                except ImageInfo.DoesNotExist:
                    continue
                except ImageInfo.MultipleObjectsReturned:
                    logger.warning(f'filename {file_name} has multiple objects')
                    continue
                else:
                    img_ref.artwork_name = item.get('name', '')
                    img_ref.save()
                
                #TODO save tag relationship
                tag_list = []
                for tag_name in item.get('tag', []):
                    try:
                        tag_list.append(Tag.objects.get(name=tag_name))
                    except Tag.DoesNotExist:
                        logger.error(f'tag {tag_name} not found')
                        continue
                    #Todo can add cache to improve performance
                img_ref.tags.add(*tag_list)
    return {'status': 'success'}


@api_view(['POST'])
def import_tags_api(request):
    json_path = request.data.get('json_path', None)
    json_response = import_tags(json_path)
    return JsonResponse(json_response)


# import tags to db from json file
def import_tags(json_path):
    json_data = {}
    if json_path:
        with open(json_path) as f:
            json_data = json.load(f)

        bulk_create_prepare = []
        for tag_type, tag_list in json_data.get('tag', {}).items():
            for tag_name in tag_list:
                bulk_create_prepare.append(Tag(name=tag_name, type_name=tag_type))
        
        Tag.objects.bulk_create(bulk_create_prepare, ignore_conflicts=True, unique_fields=['name'])
    return {'status': 'success'}


@csrf_exempt
def test(request):
    # import_images_related_info(request)
    return JsonResponse({'test': 'test'})


