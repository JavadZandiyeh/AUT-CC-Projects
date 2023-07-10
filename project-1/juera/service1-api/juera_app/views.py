import pika
from auth0.authentication import Database, GetToken, Users
from django.core.files.storage import default_storage
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers, models

# ----------------------------auth0 settings----------------------------
settings = {
    'AUTH0_DOMAIN': 'dev-pwjp3ar40sb22h0a.us.auth0.com',
    'AUTH0_CLIENT_ID': 'Eg46gThxEwWdW4Tdrh0T7gv8hoe7LtBn',
    'AUTH0_CLIENT_SECRET': 'eZ2nwh9E75Kc4bxv3flpWt3L8gMZYrgf6iRI85qwGnSQiuSFMVcG9tefTXNCmTT_',
}
database = Database(settings['AUTH0_DOMAIN'], settings['AUTH0_CLIENT_ID'])
token = GetToken(settings['AUTH0_DOMAIN'], settings['AUTH0_CLIENT_ID'], settings['AUTH0_CLIENT_SECRET'])
users = Users(settings['AUTH0_DOMAIN'])

# ----------------------------RabbitMQ settings----------------------------
AMQP_URL = 'amqps://qvyijfug:Hie5yrfMNvpB_KNBvAWbqY5has3eNbu7@codfish.rmq.cloudamqp.com/qvyijfug'


# ----------------------------implement views----------------------------
@api_view(['POST'])
def sign_up(request) -> Response:
    serializer = serializers.UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    try:
        database.signup(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            connection='Email-Password-Authentication',
        )
    except Exception as e:
        return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)

    return Response(serializer.validated_data, status.HTTP_200_OK)


@api_view(['GET'])
def login(request) -> Response:
    serializer = serializers.UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    try:
        user_token = token.login(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            realm='Email-Password-Authentication',
            scope='',
            audience='',
        )
    except Exception as e:
        return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)

    return Response(user_token, status.HTTP_200_OK)


@api_view(['POST'])
def file_upload(request) -> Response:
    serializer = serializers.UploadFileSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    try:
        user = users.userinfo(request.headers['access-token'])
        upload = models.Upload.objects.create(
            email=user['email'],
            inputs=serializer.validated_data['inputs'],
            language=serializer.validated_data['language'],
        )

        uploaded_file = serializer.validated_data['file']
        s3_file_upload = default_storage.save(
            get_file_name(user['email'], upload.id, upload.language),
            uploaded_file
        )
    except Exception as e:
        return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            'upload': model_to_dict(upload),
            's3_file_upload': s3_file_upload
        },
        status.HTTP_200_OK
    )


@api_view(['POST'])
def file_run(request) -> Response:
    serializer = serializers.RunFileSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    try:
        user = users.userinfo(request.headers['access-token'])

        file_id = serializer.validated_data['file_id']
        upload = models.Upload.objects.get(pk=file_id)

        if upload.email != user['email']:
            return Response({'message': 'you are not allowed to run this file'}, status.HTTP_400_BAD_REQUEST)

        if upload.enable:
            return Response({'message': 'you can not run this file again'}, status.HTTP_400_BAD_REQUEST)

        file_name = get_file_name(upload.email, upload.id, upload.language)

        connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        channel = connection.channel()
        channel.queue_declare(queue='juera')
        channel.basic_publish(exchange='', routing_key='juera', body=bytes(str(file_name), 'utf-8'))
        connection.close()
    except Exception as e:
        return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'done'}, status.HTTP_200_OK)


@api_view(['GET'])
def get_results(request):
    try:
        user = users.userinfo(request.headers['access-token'])

        user_results = []

        results = models.Result.objects.all()
        for result in results:
            if result.job.upload.email == user['email']:
                upload = result.job.upload
                file_name = get_file_name(upload.email, upload.id, upload.language)

                user_results.append(
                    {
                        'file': default_storage.url(file_name),
                        'output': result.output,
                        'executed_date': result.executed_date,
                        'status': result.status
                    }
                )

        return Response({'message': user_results}, status.HTTP_200_OK)

    except Exception as e:
        return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)


# ----------------------------useful services----------------------------
def get_file_name(email: str, file_id: int, language: str) -> str:
    return f"file_{email}_{file_id}.{language}"
