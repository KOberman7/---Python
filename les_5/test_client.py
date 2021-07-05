import unittest
from client import main, create_presence_message


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client_message = main()
        self.required_keys = ['action', 'time', 'user']
        self.test_message = {
            'action': 'presence',
            'time': 'Thu Sep 1 09:11:00 2020',
            'user': {'account_name': 'Guest'}
        }

        self.server_message = {'response': 200}

    def test_presence(self):
        self.client_message['time'] = self.test_message['time']
        self.assertEqual(self.test_message, self.client_message)
        self.assertTrue([key in create_presence_message('Guest').keys() for key in self.required_keys])


if __name__ == '__main__':
    unittest.main()
