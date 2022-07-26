import json
import unittest
from unittest.mock import MagicMock, patch, call
from econtools import econ_workflow

def test_start_workflow():
    queue_mock = MagicMock()
    queue_name = 'ct-workflow-starter-queue'
    workflow_name = 'MyArticleWorkflow'

    expected_message_body = {
        'workflow_name': workflow_name,
        'workflow_data': {}}
    expected = call(QueueUrl=queue_name, MessageBody=json.dumps(expected_message_body))

    with patch('econtools.aws.get_queue', return_value=(queue_mock, queue_name)):
        econ_workflow.start_workflow(queue_name, workflow_name)
        assert len(queue_mock.method_calls) == 1
        assert queue_mock.send_message.call_args_list == [expected]
