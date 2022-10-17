from flask import current_app, url_for
from werkzeug.utils import cached_property
from flask_testing import TestCase

from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app


    def test_app_exists(self):
        self.assertIsNotNone(current_app)


    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])


    #def test_index_redirects(self):
    #    response = self.client.get(url_for('index'))
    #    self.assertRedirects(response, url_for('home'))
 

    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assert200(response)


    #Devuelve code 405 (no autorizado)
    def test_home_post(self):
        response = self.client.post(url_for('home'))
        self.assertTrue(response.status_code, 405)


    def test_auth_blueprint(self):
        self.assertIn('auth', self.app.blueprints)


    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)


    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('auth/login.html')


    #def test_auth_login_post(self):
    #    fake_form = {
    #        'username': 'fake',
    #        'password': 'fake-password'
    #    }
    #    response = self.client.post(url_for('auth.login'), data=fake_form)
    #    self.assertRedirects(response, '/')    