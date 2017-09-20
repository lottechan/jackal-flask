import os
from datetime import date
import unittest
from flask import url_for
from app import app, db
from app.models import Stock

class JackalFlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/webapp/db/test.sqlite'
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.drop_all()
        os.unlink('/opt/webapp/db/test.sqlite')
        del self.app

    def test_index(self):
        """Assert that user successfully lands on index page"""
        result = self.app.get('/index')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'wgx731', result.data)

    def test_home(self):
        """Assert that user successfully lands on home page"""
        db.session.add(Stock(
            date(1985, 11, 1),
            115.48,
            116.68,
            115.48,
            116.28,
            900900,
            'GOOGL'
        ))
        db.session.commit()
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'GOOGL', result.data)

    def test_stocks_csv(self):
        """Assert that stock csv api returns csv result"""
        db.session.add(Stock(
            date(1985, 11, 1),
            115.48,
            116.68,
            115.48,
            116.28,
            900900,
            'CSV'
        ))
        db.session.commit()
        result = self.app.get('/api/stocks.csv')
        self.assertEqual(result.status_code, 200)
        self.assertIn('text/csv', result.headers['Content-Type'])
        self.assertIn(b'CSV', result.data)

    def test_stocks_txt(self):
        """Assert that stock txt api returns txt result"""
        db.session.add(Stock(
            date(1985, 11, 1),
            115.48,
            116.68,
            115.48,
            116.28,
            900900,
            'TXT'
        ))
        result = self.app.get('/api/stocks.txt')
        self.assertEqual(result.status_code, 200)
        self.assertIn('text/plain', result.headers['Content-Type'])
        self.assertIn(b'TXT', result.data)

    def test_stocks_json(self):
        """Assert that stock json api returns json result"""
        db.session.add(Stock(
            date(1985, 11, 1),
            115.48,
            116.68,
            115.48,
            116.28,
            900900,
            'JSON'
        ))
        result = self.app.get('/api/stocks.json')
        self.assertEqual(result.status_code, 200)
        self.assertIn('application/json', result.headers['Content-Type'])
        self.assertIn(b'JSON', result.data)

    def test_stocks(self):
        """Assert that stock json api returns json result"""
        result = self.app.get('/api/stocks', headers={'Accept': 'text/csv'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('text/csv', result.headers['Content-Type'])
        result = self.app.get('/api/stocks', headers={'Accept': 'text/plain'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('text/plain', result.headers['Content-Type'])
        result = self.app.get('/api/stocks', headers={'Accept': 'application/json'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('application/json', result.headers['Content-Type'])

if __name__ == '__main__':
    unittest.main()

