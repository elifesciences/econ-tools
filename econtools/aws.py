import boto.sqs
import boto.sqs.connection
import os, sys

def get_queue(queue_name):
    region = os.environ.get('AWS_DEFAULT_REGION')
    if not region:
        print("environment variable 'AWS_DEFAULT_REGION' not set")
        sys.exit(1)
    sqs_conn = boto.sqs.connect_to_region(region)
    if sqs_conn is None:
        print("Cannot connect to SQS for region %s" % region)
        sys.exit(1)
    queue = sqs_conn.get_queue(queue_name)
    if queue is None:
        print("Could not obtain workflow starter queue %s\n" % (queue_name,))
        sys.exit(1)
    return queue
