
"""
econ_workflow.py - starts arbitrary continuum publishing workflows
"""

from optparse import OptionParser
import json
import boto.sqs
import boto.sqs.connection
from econtools.aws import get_queue


def start_workflow(queue_name, workflow_name):

    queue = get_queue(queue_name)
    message = {
        'workflow_name': workflow_name,
        'workflow_data': {}
    }

    msg = boto.sqs.connection.Message()
    msg.set_body(json.dumps(message))
    queue.write(msg)

def get_args():
    usage = "usage: %prog workflow_starter_queue IngestArticleZip"
    parser = OptionParser(usage=usage)

    _, args = parser.parse_args()
    if (len(args) < 2) or (len(args) > 3):
        parser.error("incorrect number of arguments")

    return args

def main():
    args = get_args()
    start_workflow(args[0], args[1])


if __name__ == "__main__":
    main()
