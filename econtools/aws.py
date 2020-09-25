import boto.sqs
import boto.sqs.connection
import os, sys

def get_queue(queue_name):
    sqs_conn = boto.sqs.connect_to_region(os.environ['AWS_DEFAULT_REGION'])
    if sqs_conn is None:
        print("Cannot connect to SQS for region %s" % os.environ['AWS_DEFAULT_REGION'])
        sys.exit(1)
    queue = sqs_conn.get_queue(queue_name)
    if queue is None:
        print("Could not obtain workflow starter queue %s\n" % (queue_name,))
        sys.exit(2)
    return queue
