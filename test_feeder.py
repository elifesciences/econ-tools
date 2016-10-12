from datetime import datetime
import json
import unittest
from mock import MagicMock, call, patch
from boto.s3.bucket import Bucket
from boto.s3.key import Key
from boto.sqs.message import Message
import econ_article_feeder

class TestFeeder(unittest.TestCase):
    @patch('econ_article_feeder.get_queue')
    @patch('econ_article_feeder.get_filtered_keys')
    @patch('econ_article_feeder.initiate_econ_feed')
    @patch('time.sleep')
    def test_feed_two_articles(self, sleep, initiate_econ_feed, get_filtered_keys, get_queue):
        queue = MagicMock()
        get_queue.return_value = queue
        get_filtered_keys.return_value = [
            'elife-12345-vor-r1.zip',
            'elife-67890-vor-r1.zip',
        ]
        econ_article_feeder.feed_econ('ct-elife-production-final', 'ct-workflow-starter-queue', workflow_name='MyArticleWorkflow')
        self.assertEqual(
            initiate_econ_feed.mock_calls,
            [
                call(queue, 'elife-12345-vor-r1.zip', 'MyArticleWorkflow'),
                call(queue, 'elife-67890-vor-r1.zip', 'MyArticleWorkflow'),
            ]
        )
        self.assertEqual(
            sleep.mock_calls,
            [
                call(30),
                call(30)
            ]
        )

    @patch('econ_article_feeder.now')
    def test_feeding_sends_an_sqs_message(self, now):
        now.return_value = datetime.strptime('2016-01-01', '%Y-%m-%d')
        queue = MagicMock()
        key = Key()
        key.bucket = Bucket()
        key.bucket.name = 'ct-elife-production-final'
        key.name = 'elife-12345-vor-r1.zip'
        key.etag = '...'
        key.size = 2 * 1024 * 1024
        econ_article_feeder.initiate_econ_feed(queue, key, 'MyArticleWorkflow')
        self.assertEqual(len(queue.method_calls), 1)
        (_, args, _) = queue.method_calls[0]
        message_body = args[0].get_body()
        self.assertEqual(
            json.loads(message_body),
            {
                'workflow_name': 'MyArticleWorkflow',
                'workflow_data': {
                    'event_time': '2016-01-01T00:00:00Z',
                    'event_name': 'ObjectCreated:Put',
                    'file_name': 'elife-12345-vor-r1.zip',
                    'file_etag': '...',
                    'bucket_name': 'ct-elife-production-final',
                    'file_size': 2 * 1024 * 1024,
                },
            }
        )
