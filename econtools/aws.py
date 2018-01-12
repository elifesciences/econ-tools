import boto.sqs
import boto.sqs.connection
import os

def get_queue(queue_name):
    sqs_conn = boto.sqs.connect_to_region(os.environ['AWS_DEFAULT_REGION'])
    queue = sqs_conn.get_queue(queue_name)
    if queue is None:
        print("Could not obtain workflow starter queue %s\n" % queue_name)
        exit()
    return queue
