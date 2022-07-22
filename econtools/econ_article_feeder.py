"""econ_article_feeder.py
feeds arbitrary article zip files into the continuum publishing workflow"""

from optparse import OptionParser
from datetime import datetime
import time
import re
import json
import sys
from econtools import aws


def feed_econ(bucket_name, queue_name, rate=30, prefix=None, key_filter=None, working=False, workflow_name="InitialArticleZip"):

    message = "\nFeeding any keys in %s " % bucket_name
    if prefix is not None:
        message += "with prefix %s " % prefix
    if key_filter is not None:
        message += "with keys matching %s " % key_filter
    message += "at a rate of 1 every %i seconds to %s.\n" % (rate, queue_name)
    message += "Feeding Workflow: %s" % workflow_name
    print(message)

    keys = get_filtered_keys(bucket_name, prefix, key_filter)
    print(keys)

    count = 0
    for i, key in enumerate(keys):
        initiate_econ_feed(queue_name, bucket_name, key, workflow_name)
        count += 1
        if working:
            sys.stdout.write('.')
        time.sleep(rate)
    print("\n\nFed %s keys\n" % (count,))


def get_filtered_keys(bucketname, prefix, key_filter):
    client = aws.get_client('s3')
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjects
    paginator = client.get_paginator('list_objects')
    bucket_object_list_resp = paginator.paginate(Bucket=bucketname, Prefix=prefix)
    bucket_object_list = bucket_object_list_resp['Contents']

    # the list method is a generator and efficiently handles paging over a large
    # set of results so we will maintain this while filtering using another generator
    for key in bucket_object_list:
        valid = True
        if prefix is not None and not key['Name'].startswith(prefix):
            valid = False
        if key_filter is not None and not re.match(key_filter, key['Name']):
            valid = False
        if valid:
            yield key


def initiate_econ_feed(queue_name, bucket_name, key, workflow_name):
    file_info = {
        'event_name': 'ObjectCreated:Put',
        'event_time': now().isoformat() + "Z",  # ISO_8601 e.g. 1970-01-01T00:00:00.000Z
        'bucket_name': bucket_name,
        'file_name': key['Name'],
        'file_etag': key['ETag'].strip("\""),
        'file_size': key['Size']
    }

    message = {
        'workflow_name': workflow_name,
        'workflow_data': file_info
    }

    aws.send_message(queue_name, message)

def now():
    # lsh@2022-07-22: changed from `.now` to `.utcnow`
    return datetime.utcnow()

usage = "usage: %prog [options] bucket_name workflow_starter_queue InitialArticleZip"

def get_options():
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--prefix", default=None, action="store", type="string", dest="prefix",
                      help="only feed keys with the given prefix")
    parser.add_option("-r", "--rate", default="30", action="store", type="int",
                      dest="rate", help="how many seconds between messages")
    parser.add_option("-f", "--filter", default=None, action="store", type="string", dest="filter",
                      help="filter regex to match against keys")
    parser.add_option("-w", "--working", default=False, action="store_true", dest="working",
                      help="show progress indicator to indicate working")

    opts, ags = parser.parse_args()
    if len(ags) not in [2, 3]:
        parser.error("incorrect number of arguments")

    return opts, ags


if __name__ == "__main__":
    options, args = get_options()

    if len(args) > 2:
        bucket_name, queue_name, workflow_name = args[:3]
        feed_econ(bucket_name, queue_name, options.rate, options.prefix, options.filter, options.working, workflow_name)
    elif len(args) == 2:
        bucket_name, queue_name = args[:2]
        feed_econ(args[0], args[1], options.rate, options.prefix, options.filter, options.working)
    else:
        print(usage)
        sys.exit(1)
