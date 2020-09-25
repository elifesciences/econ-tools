
"""
econ_dashprop.py - Sets string properties against versions of articles within the eLife Continuum Dashboard
"""

from optparse import OptionParser
from econtools.aws import get_queue
import uuid
import boto.sqs
import boto.sqs.connection
import json


def feed_econ(queue_name, article, version, property, value):

    queue = get_queue(queue_name)

    message = {
        'message_type': 'property',
        'item_identifier': article,
        'version': version,
        'name': property,
        'value': value,
        'property_type': "text",
        'message_id': str(uuid.uuid4())
    }

    msg = boto.sqs.connection.Message()
    msg.set_body(json.dumps(message))
    queue.write(msg)

    print("Property message sent\n")


def get_options():
    usage = "usage: %prog dashboard_queue_name article_id version property_name property_value"
    parser = OptionParser(usage=usage)

    opts, ags = parser.parse_args()
    if len(ags) != 5:
        parser.error("incorrect number of arguments")

    return opts, ags


if __name__ == "__main__":
    options, args = get_options()

    # args[0] = bucket_name, args[1] = queue_name
    feed_econ(args[0], args[1], args[2], args[3], args[4])
