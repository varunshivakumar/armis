# test_collector.py

from unittest import TestCase
from collector import publish_node_load

class TryTesting(TestCase):
    def test_publish_node_load(self):
        res = publish_node_load()
        self.assertaTrue(res)

    # Test Database connection with Mocked database