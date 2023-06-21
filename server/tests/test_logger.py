import logging
import sys
import unittest
from unittest.mock import patch
from server.app.log import logger as logger


class LoadLogTest(unittest.TestCase):
    @patch('logging.StreamHandler')
    @patch('logging.basicConfig')
    @patch('logging.getLogger')
    def test_load_log(self, mock_get_logger, mock_basic_config, mock_stream_handler):
        logger_mock = mock_get_logger.return_value

        result = logger.load_log()

        mock_basic_config.assert_called_once_with(
            level=logging.INFO,
            handlers=[mock_stream_handler.return_value],
            format='%(asctime)s - %(name)s - %(filename)s - %(lineno)s - %(funcName)s - %(levelname)s - %(message)s'
        )
        mock_get_logger.assert_called_once_with('VoiceCollectorEntry')
        logger_mock.setLevel.assert_called_once_with(logging.INFO)
        self.assertEqual(result, logger_mock)


if __name__ == '__main__':
    unittest.main()
