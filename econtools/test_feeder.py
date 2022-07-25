from datetime import datetime
import json
import unittest
from unittest.mock import MagicMock, call, patch
from econtools import econ_article_feeder

class TestFeeder(unittest.TestCase):
    @patch('econtools.aws.get_queue')
    @patch('econtools.econ_article_feeder.get_filtered_keys')
    @patch('econtools.econ_article_feeder.initiate_econ_feed')
    @patch('time.sleep')
    def test_feed_two_articles(self, sleep, initiate_econ_feed, get_filtered_keys, get_queue):
        queue_mock = MagicMock()
        bucket_name = 'ct-elife-production-final'
        queue_name = 'ct-workflow-starter-queue'
        workflow_name='MyArticleWorkflow'
        get_queue.return_value = [queue_mock, queue_name]
        get_filtered_keys.return_value = [
            'elife-12345-vor-r1.zip',
            'elife-67890-vor-r1.zip',
        ]

        expected = [
            call(queue_name, bucket_name, 'elife-12345-vor-r1.zip', workflow_name),
            call(queue_name, bucket_name, 'elife-67890-vor-r1.zip', workflow_name)
        ]
        econ_article_feeder.feed_econ(bucket_name, queue_name, workflow_name=workflow_name)
        self.assertEqual(initiate_econ_feed.mock_calls, expected)

        expected_sleeps = [
            call(30),
            call(30)
        ]
        self.assertEqual(sleep.mock_calls, expected_sleeps)

    @patch('econtools.aws.get_queue')
    @patch('econtools.econ_article_feeder.now')
    def test_feeding_sends_an_sqs_message(self, now, get_queue):
        now.return_value = datetime.strptime('2016-01-01', '%Y-%m-%d')
        queue_mock = MagicMock()
        queue_name = 'foo'
        get_queue.return_value = [queue_mock, queue_name]
        bucket_name = 'ct-elife-production-final'
        key = {
            'Name': 'elife-12345-vor-r1.zip',
            'ETag': '"123"',
            'Size': 2 * 1024 * 1024
        }
        workflow_name = 'MyArticleWorkflow'
        econ_article_feeder.initiate_econ_feed(queue_name, bucket_name, key, workflow_name)
        
        self.assertEqual(len(queue_mock.method_calls), 1)

        expected_message_body = {
            'workflow_name': 'MyArticleWorkflow',
            'workflow_data': {
                'event_time': '2016-01-01T00:00:00Z',
                'event_name': 'ObjectCreated:Put',
                'file_name': 'elife-12345-vor-r1.zip',
                'file_etag': '123',
                'bucket_name': 'ct-elife-production-final',
                'file_size': 2 * 1024 * 1024,
            }
        }

        _, _, args = queue_mock.method_calls[0]
        message_body = args['MessageBody']

        self.assertEqual(json.loads(message_body), expected_message_body)
