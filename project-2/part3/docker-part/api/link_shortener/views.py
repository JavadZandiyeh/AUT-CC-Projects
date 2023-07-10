import base64
import json
import os

import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers

@api_view(['POST'])
def link_shortener(request) -> Response:
    serializer = serializers.LinkShortenerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    try:
        long_url = serializer.validated_data['longUrl']
        redis_status, short_url = get_from_redis(long_url)
        is_cached = short_url is not None
        hostname = request.get_host()

        if not is_cached:
            short_url = get_short_url_from_rebrandly(serializer.validated_data['longUrl'])
            if redis_status:
                cache.set(long_url, short_url)
                

        data = {'longUrl': long_url, 'shortUrl': short_url, 'isCached': is_cached, 'hostname': hostname,
                'redisIsUp': redis_status}

    except Exception as e:
        return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)

    return Response(data, status.HTTP_200_OK)


def get_from_redis(long_url: str):
    try:
        redis_status = True
        short_url = cache.get(long_url)
    except:
        redis_status = False
        short_url = None

    return redis_status, short_url

def get_short_url_from_rebrandly(long_url: str) -> str or None:
    try:
        link_request = {"destination": long_url, "domain": {"fullName": "rebrand.ly"}}
        request_headers = {"Content-type": "application/json", "apikey": base64.b64decode(os.getenv('REBRANDLY_KEY'))}

        response = requests.post(
            base64.b64decode(os.getenv('REBRANDLY_API')),
            data=json.dumps(link_request),
            headers=request_headers
        ).json()

        return response['shortUrl']
    except:
        return None
