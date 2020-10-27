import json
import unittest
from unittest.mock import MagicMock, patch
from econtools import econ_workflow

class TestWorkflow(unittest.TestCase):
    @patch('econtools.econ_workflow.get_queue')
    def test_feed_two_articles(self, get_queue):
        queue = MagicMock()
        get_queue.return_value = queue
        econ_workflow.start_workflow('ct-workflow-starter-queue', workflow_name='MyArticleWorkflow')

        self.assertEqual(len(queue.method_calls), 1)
        (_, args, _) = queue.method_calls[0]
        message_body = args[0].get_body()
        self.assertEqual(
            json.loads(message_body),
            {
                'workflow_name': 'MyArticleWorkflow',
                'workflow_data': {},
            }
        )
