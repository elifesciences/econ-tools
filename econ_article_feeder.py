
"""
econ-article-feeder.py - feeds arbitrary article zip files into the continuum publishing workflow
"""

from optparse import OptionParser
from boto.s3.connection import S3Connection
from datetime import datetime
import boto.sqs
import boto.sqs.connection
import time
import re
import json
import os
import sys


def feed_econ(bucket_name, queue_name, rate, prefix, key_filter, working, workflow_name="PublishPerfectArticle"):

    message = "\nFeeding any keys in %s " % bucket_name
    if prefix is not None:
        message += "with prefix %s " % prefix
    if key_filter is not None:
        message += "with keys matching %s " % key_filter
    message += "at a rate of 1 every %i seconds to %s.\n" % (rate, queue_name)
    message += "Feeding Workflow: %s" % workflow_name
    print message

    queue = get_queue(queue_name)
    keys = get_filtered_keys(bucket_name, prefix, key_filter)

    count = 0
    for key in keys:
        initiate_econ_feed(queue, key, workflow_name)
        count += 1
        if working:
            sys.stdout.write('.')
        time.sleep(rate)
    print "\n\nFed %s keys\n" % count


def get_queue(queue_name):
    sqs_conn = boto.sqs.connect_to_region(os.environ['AWS_DEFAULT_REGION'])
    queue = sqs_conn.get_queue(queue_name)
    if queue is None:
        print "Could not obtain workflow starter queue %s\n" % queue_name
        exit()
    return queue


def get_filtered_keys(bucketname, prefix, key_filter):
    conn = S3Connection()
    bucket = conn.get_bucket(bucketname)
    keys = bucket.list(prefix=prefix)

    # the list method is a generator and efficiently handles paging over a large
    # set of results so we will maintain this while filtering using another generator
    for key in keys:
        valid = True
        if prefix is not None and not key.name.startswith(prefix):
            valid = False
        if key_filter is not None and not re.match(key_filter, key.name):
            valid = False
        if valid:
            yield key


def initiate_econ_feed(queue, key, workflow_name):
    file_info = {
        'event_name': 'ObjectCreated:Put',
        'event_time': datetime.now().isoformat() + "Z",  # ISO_8601 e.g. 1970-01-01T00:00:00.000Z
        'bucket_name': key.bucket.name,
        'file_name': key.name,
        'file_etag': key.etag.strip("\""),
        'file_size': key.size
    }

    message = {
        'workflow_name': workflow_name,
        'workflow_data': file_info
    }

    msg = boto.sqs.connection.Message()
    msg.set_body(json.dumps(message))
    queue.write(msg)


def get_options():
    usage = "usage: %prog [options] bucket_name workflow_starter_queue IngestArticleZip"
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
    if (len(ags) < 2) and (len(ags) > 3):
        parser.error("incorrect number of arguments")

    return opts, ags


if __name__ == "__main__":
    options, args = get_options()

    if len(args) > 2:
        # args[0] = bucket_name, args[1] = queue_name args[2] = WorkflowName
        feed_econ(args[0], args[1], options.rate, options.prefix, options.filter, options.working, args[2])
    else:
        # args[0] = bucket_name, args[1] = queue_name
        feed_econ(args[0], args[1], options.rate, options.prefix, options.filter, options.working)
