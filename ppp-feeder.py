from optparse import OptionParser
from boto.s3.connection import S3Connection
from boto.sqs.connection import SQSConnection
from datetime import datetime
from time import sleep
from re import match
from json import dumps


def feed_ppp(bucket_name, queue_name, rate, prefix, key_filter):

    print "feeding any keys in %s with prefix %s matching %s at a rate of 1 every %i seconds" % (
        bucket_name, prefix, key_filter, rate)

    queue = get_queue(queue_name)
    keys = get_filtered_keys(bucket_name, prefix, key_filter)

    for key in keys:
        initiate_ppp(queue, key)
        sleep(rate)


def get_queue(queue_name):

    sqs_conn = SQSConnection()
    queue = sqs_conn.get_queue(queue_name)
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
        if key_filter is not None and not match(key_filter, key.name):
            valid = False
        if valid:
            yield key


def initiate_ppp(queue, key):

    file_info = {
        'event_name': 'ObjectCreated:Put',
        'event_time': datetime.now().isoformat() + "Z",  # ISO_8601 e.g. 1970-01-01T00:00:00.000Z
        'bucket_name': key.bucket.name,
        'file_name': key.name,
        'file_etag': key.etag.strip("\""),
        'file_size': key.size
    }
    message = {
        'workflow_name': 'PublishPerfectArticle',
        'workflow_data': file_info
    }

    print dumps(message) + "\n\n"


def get_options():

    usage = "usage: %prog [options] bucket_name workflow_starter_queue"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--prefix", default=None, action="store", type="string", dest="prefix",
                      help="only feed keys with the given prefix")
    parser.add_option("-r", "--rate", default="30", action="store", type="int",
                      dest="rate", help="how many seconds between messages")
    parser.add_option("-f", "--filter", default=None, action="store", type="string", dest="filter",
                      help="filter regex to match against keys")

    opts, ags = parser.parse_args()
    if len(ags) != 2:
        parser.error("incorrect number of arguments")

    return opts, ags


if __name__ == "__main__":

    options, args = get_options()

    # args[0] = bucket_name, args[1] = queue_name
    feed_ppp(args[0], args[1], options.rate, options.prefix, options.filter)
