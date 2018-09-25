from flask import current_app
import pytest
import json
from base64 import b64encode
from os.path import join, dirname, abspath


@pytest.mark.usefixtures("app", "client", autouse=True)   # to use fixtures from conftest
class TestWebAPIs(object):
    """
        Testing the APIs by connecting to the flask app from a client.
    """

    @classmethod
    def setup_class(cls):
        cls.api_url = '/api/'
        cls.template_url = '/'

    def test_app_exists(self):
        assert current_app is not None

    def test_home_page(self, client):
        """Go to homepage - root of the application"""

        response = client.get('/')
        assert response.status_code == 200
        assert 'Basis Set Exchange' in response.get_data(as_text=True)
        assert 'Download basis set' in response.get_data(as_text=True)

    def test_web_get_metadata(self, client):
        """Default (empty) search results in all none pending software
         in the DB
         """

        response = client.get('/web_metadata/')
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))

        assert 'metadata' in json_data
        assert 'element_basis' in json_data

        # print(json_data['metadata'])
        # print(json_data['element_basis'])


    def test_get_basis_elements(self, client):
        """Get a simple basis set"""

        bs_name = '3-21g'
        bs_format = 'gaussian94'
        params = dict(elements='1,3')
        url = self.template_url + 'basis/{}/format/{}/'.format(bs_name, bs_format)
        response = client.get(url, query_string=params)
        assert response.status_code == 200
        data = response.get_data(as_text=True)
        assert 'Basis set: 3-21G' in data
        assert 'H' in data and 'Li' in data

    def test_get_references(self, client):
        """Get references for a basis set with different formats"""

        bs_name = '3-21g'
        params = dict(elements='1,3')
        rf_format = 'json'
        url = self.template_url + 'references/{}/format/{}/'.format(bs_name, rf_format)
        response = client.get(url, query_string=params)
        assert response.status_code == 200
        data = response.get_data(as_text=True)
        assert data

        # without elements
        response = client.get(url)
        assert response.status_code == 200

    def test_get_notes(self, client):
        """Get notes of a basis set"""

        bs_name = '3-21g'
        url = self.template_url + 'notes/{}/'.format(bs_name)
        response = client.get(url)
        assert response.status_code == 200
        assert response.get_data(as_text=True)