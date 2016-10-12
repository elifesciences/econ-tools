import unittest
from mock import MagicMock, call, patch
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

