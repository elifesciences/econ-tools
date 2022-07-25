import boto3
import os, sys, json

def get_client(service):
    region = os.environ.get('AWS_DEFAULT_REGION')
    if not region:
        print("environment variable 'AWS_DEFAULT_REGION' not set")
        sys.exit(1)

    # https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html#botocore-config
    conn_kwargs = {
        'region_name': region,
        'connect_timeout': 5, # seconds, default 60
        'read_timeout': 5, # seconds, default 60
        'retries': {
            'total_max_attempts': 3,
            'mode': 'adaptive'
        }
    }
    return boto3.client(service, **conn_kwargs)

def get_queue(queue_name):
    try:
        client = get_client('sqs')
        queue_url = client.get_queue_url(QueueName=queue_name)
        return client, queue_url
    except Exception as exc:
        print("Unhandled exception obtaining workflow starter queue %r: %s\n" % (exc, queue_name,))
        sys.exit(1)

def send_message(queue_name, message):
    client, queue_url = get_queue(queue_name)
    return client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
