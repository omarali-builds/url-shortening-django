from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ShortURL
from .serializers import (
    ShortURLCreateSerializer,
    ShortURLSerializer,
    ShortURLUpdateSerializer,
)


@api_view(['POST'])
def create_short_url(request):
    serializer = ShortURLCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    short_url = serializer.save()
    output = ShortURLSerializer(short_url)
    return Response(output.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def handle_short_url(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)

    if request.method == 'GET':
        serializer = ShortURLSerializer(short_url)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShortURLUpdateSerializer(short_url, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        output = ShortURLSerializer(short_url)
        return Response(output.data)

    elif request.method == 'DELETE':
        short_url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_url_stats(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    serializer = ShortURLSerializer(short_url)
    return Response(serializer.data)


@api_view(['GET'])
def redirect_to_original(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    short_url.access_count += 1
    short_url.save(update_fields=['access_count'])
    from django.shortcuts import redirect
    return redirect(short_url.url)
