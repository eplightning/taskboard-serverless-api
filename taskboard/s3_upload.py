import boto3
from taskboard.models import Task
from urllib.parse import unquote_plus

s3 = boto3.client('s3', 'eu-west-1')

def process_upload(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])

    head = s3.head_object(Bucket=bucket, Key=key)
    meta = head['Metadata']
    task = Task.get(meta['project'], meta['task'])

    task.update(actions=[
        Task.attachments.add({key})
    ])
