
"""
econ_workflow.py - starts arbitrary continuum publishing workflows
"""

from argparse import ArgumentParser
import json
import boto.sqs
import boto.sqs.connection
from econtools.aws import get_queue


def start_workflow(queue_name, workflow_name, workflow_data={}):

    queue = get_queue(queue_name)
    message = {
        'workflow_name': workflow_name,
        'workflow_data': workflow_data,
    }

    msg = boto.sqs.connection.Message()
    msg.set_body(json.dumps(message))
    queue.write(msg)

def get_args():
    usage = "usage: %prog workflow_starter_queue IngestArticleZip"
    parser = ArgumentParser(description="Starts any workflow")
    parser.add_argument('queue_name', type=str, help='The queue to add the starting message to')
    parser.add_argument('workflow_name', type=str, help='The workflow type to start')
    parser.add_argument('workflow_data', type=str, help='The workflow data in JSON format e.g. \`{"a": 42}\`', nargs='?', default='{}')

    return parser.parse_args()


def main():
    args = get_args()
    start_workflow(args.queue_name, args.workflow_name, json.loads(args.workflow_data))


if __name__ == "__main__":
    main()
