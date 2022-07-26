import boto3
import os, sys, json

def get_client(service):
    region = os.environ.get('AWS_DEFAULT_REGION')
    if not region:
        print("environment variable 'AWS_DEFAULT_REGION' not set")
        sys.exit(1)
    conn_kwargs = {
        'region_name': region,
    }
    return boto3.client(service, **conn_kwargs)

def get_queue(queue_name):
    try:
        client = get_client('sqs')
        response = client.get_queue_url(QueueName=queue_name)
        queue_url = response.get("QueueUrl")
        return client, queue_url
    except Exception as exc:
        print("Unhandled exception obtaining workflow starter queue %r: %s\n" % (exc, queue_name,))
        sys.exit(1)

def send_message(queue_name, message):
    client, queue_url = get_queue(queue_name)
    return client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
