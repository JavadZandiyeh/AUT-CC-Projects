import json
import os
import sys
from urllib.parse import urlencode

import boto3
import pika

import db_connector

AMQP_URL = 'amqps://qvyijfug:Hie5yrfMNvpB_KNBvAWbqY5has3eNbu7@codfish.rmq.cloudamqp.com/qvyijfug'


def main():
    try:
        db = get_database()
        s3 = get_file_storage()
        bucket = s3.Bucket('juera')
    except Exception as e:
        print(str(e))
        sys.exit(0)

    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()
    channel.queue_declare(queue='juera')

    def callback(ch, method, properties, body):
        file_name = str(body.decode('utf-8'))
        file_data = get_file_data(file_name)
        try:
            upload = db.get_upload(file_data['file_id'])

            bucket.download_file(f"static/{file_name}", file_name)
            job = get_job_as_string(file_name, upload)
            os.remove(file_name)

            if db.create_job(file_data['file_id'], job):
                print(f"log: job created for upload {json.dumps(file_data, default=str)}")
        except Exception as e:
            print(str(e))

    channel.basic_consume(queue='juera', on_message_callback=callback, auto_ack=True)

    print('log*: waiting for messages. to exit press ctrl+c')
    channel.start_consuming()


def get_file_data(file_name: str) -> dict:
    return {
        'email': file_name[(file_name.index('_') + 1):file_name.rfind('_')],
        'file_id': file_name[(file_name.rfind('_') + 1):file_name.rfind('.')],
        'language': file_name[(file_name.rfind('.') + 1):]
    }


def get_database():
    db = db_connector.PostgresDatabase()
    db.connect()
    return db


def get_file_storage():
    return boto3.resource(
        's3',
        endpoint_url='https://storage.iran.liara.space',
        aws_access_key_id='ltomimvkcb9mrkoa',
        aws_secret_access_key='3e1135cd-6d03-4664-bbd6-f7c56521c166'
    )


def get_job_as_string(file_name, upload):
    with open(file_name, 'r') as file:
        file_contents = file.read()

    params = {'code': file_contents, 'language': upload[0][3], 'input': upload[0][2]}

    return urlencode(params)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('job creator interrupted')
        sys.exit(0)
