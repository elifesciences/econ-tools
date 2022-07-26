
"""
econ_workflow.py - starts arbitrary continuum publishing workflows
"""

from argparse import ArgumentParser
import json
from econtools import aws


def start_workflow(queue_name, workflow_name, workflow_data={}):
    message = {
        'workflow_name': workflow_name,
        'workflow_data': workflow_data,
    }
    aws.send_message(queue_name, message)


def get_args():
    usage = "example usage: %prog workflow_starter_queue IngestArticleZip"
    parser = ArgumentParser(description="Starts any workflow. " + usage)
    parser.add_argument('queue_name', type=str, help='The queue to add the starting message to')
    parser.add_argument('workflow_name', type=str, help='The workflow type to start')
    parser.add_argument('workflow_data', type=str, help='The workflow data in JSON format e.g. {"a": 42}', nargs='?', default='{}')

    return parser.parse_args()


def main():
    args = get_args()
    start_workflow(args.queue_name, args.workflow_name, json.loads(args.workflow_data))


if __name__ == "__main__":
    main()
