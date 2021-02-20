from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_game_board(self):
        """Make sure information is in the session and HTML is diplayed"""

        with self.client:
            response = self.client.get('/boggle')
            self.assertIn('game_board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'Time Remaining', response.data)
            self.assertIn(b'Score Board', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the sessions"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['game_board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/guess?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/boggle')
        response = self.client.get(
            '/guess?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')
 

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/boggle')
        response = self.client.get('/guess?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')



