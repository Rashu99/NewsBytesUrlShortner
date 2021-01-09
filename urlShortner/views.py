from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes)

# Create your views here.
from urlShortner.urlService import UrlService


@api_view(['GET'])
def get_tiny_url(request, *args, **kwargs):
    long_url = request.query_params.get('long_url', None)
    if long_url is None:
        return JsonResponse(
            {'status': 400, 'data': None, 'msg': 'Bad Request Please Provide valid Query Params'},
            status=status.HTTP_400_BAD_REQUEST
        )
    code = UrlService.request_data_validator(long_url)
    if code == 0:
        return JsonResponse(
            {'status': 400, 'data': None, 'msg': 'Bad Request Host should be https://www.newsbytesapp.com/'},
            status=status.HTTP_400_BAD_REQUEST
        )
    tiny_url = UrlService(url=long_url).get_tiny_url()
    return JsonResponse(
        {'status': 200, 'data': tiny_url, 'msg': 'Success'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_long_url(request, *args, **kwargs):
    short_url = request.query_params.get('short_url', None)
    if short_url is None:
        return JsonResponse(
            {'status': 400, 'data': None, 'msg': 'Bad Request Please Provide valid Query Params'},
            status=status.HTTP_400_BAD_REQUEST
        )
    code = UrlService.request_data_validator(short_url)
    if code == 0:
        return JsonResponse(
            {'status': 400, 'data': None, 'msg': 'Bad Request Host should be https://www.newsbytesapp.com/'},
            status=status.HTTP_400_BAD_REQUEST
        )
    long_url = UrlService(input_tiny_url=short_url).get_long_url()
    return JsonResponse(
        {'status': 200, 'data': long_url, 'msg': 'Success'},
        status=status.HTTP_200_OK
    )
