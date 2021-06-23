import unittest
from server import handle_message


class TestServer(unittest.TestCase):
    def setUp(self):
        self.client_message = {
            'action': 'presence',
            'time': 'Thu Sep 1 09:11:00 2020',
            'user': {'account_name': 'Guest'}
        }

        self.server_message = {'response': 200}

    def test_process(self):
        self.assertEqual(self.server_message, handle_message(self.client_message))
        self.assertIsInstance(handle_message(self.client_message), dict)


if __name__ == '__main__':
    unittest.main()
