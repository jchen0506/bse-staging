from flask import current_app
import pytest
import json
from base64 import b64encode
from os.path import join, dirname, abspath
import pymongo


headers = {'Content-Type': 'application/json'}


@pytest.mark.usefixtures("app", "client", autouse=True)   # to use fixtures from conftest
class TestAPIs(object):
    """
        Testing the APIs by connecting to the flask app from a client.
    """

    @classmethod
    def setup_class(cls):
        cls.api_url = '/api/'
        cls.template_url = '/'

    def test_app_exists(self):
        assert current_app is not None


    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_formats(self, client):
        """Get the supported formats of the basis sets
        """

        response = client.get(self.api_url + 'formats/')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert type(data) == dict
        assert data['gamess_us'] == 'GAMESS US'

    def test_get_references_formats(self, client):
        """Get the supported references formats
        """

        response = client.get(self.api_url + 'reference_formats/')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert type(data) == dict
        assert data['bib'] == 'BibTeX'

    def test_get_metadata(self, client):
        """Get the bs metadata
        """

        response = client.get(self.api_url + 'metadata/')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert type(data) == dict

        # get the basis data of any basis set
        basis_set_name = list(data.keys())[0]
        basis_set = data[basis_set_name]
        assert 'filebase' in basis_set
        assert 'auxiliaries' in basis_set
        assert 'functiontypes' in basis_set
        assert 'latest_version' in basis_set
        assert 'display_name' in basis_set
        assert 'family' in basis_set
        assert 'role' in basis_set

    def test_get_simple_basis(self, client):
        """Get a simple basis set"""

        bs_name = '3-21g'
        bs_format = 'gaussian94'
        url = self.api_url + 'basis/{}/format/{}/'.format(bs_name, bs_format)
        response = client.get(url)
        assert response.status_code == 200
        data = response.get_data(as_text=True)
        assert 'Basis set: 3-21G' in data

    def test_get_basis_elements(self, client):
        """Get a simple basis set"""

        bs_name = '3-21g'
        bs_format = 'gaussian94'
        params = dict(elements='1,3')
        url = self.api_url + 'basis/{}/format/{}/'.format(bs_name, bs_format)
        response = client.get(url, query_string=params)
        assert response.status_code == 200
        data = response.get_data(as_text=True)
        assert 'Basis set: 3-21G' in data
        assert 'H' in data and 'Li' in data



