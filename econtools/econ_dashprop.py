
"""
econ_dashprop.py - Sets string properties against versions of articles within the eLife Continuum Dashboard
"""

from optparse import OptionParser
from econtools import aws
import uuid
import json


def feed_econ(queue_name, article_id, version, property_name, property_value):
    message = {
        'message_type': 'property',
        'item_identifier': article_id,
        'version': version,
        'name': property_name,
        'value': property_value,
        'property_type': "text",
        'message_id': str(uuid.uuid4())
    }
    aws.send_message(queue_name, message)
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
    queue_name, article_id, version, property_name, property_value = args
    feed_econ(queue_name, article_id, version, property_name, property_value)
