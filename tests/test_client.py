import pytest


@pytest.mark.usefixtures("app", "client")
class TestFlaskClient(object):
    """
        Test creating a Flask app and a client
        connect to the client without access to DB
    """

    @pytest.mark.parametrize('url', ['/'])
    def test_home_page(self, url, client):
        """Test accessing the website from alternative paths of homepage"""

        response = client.get(url)
        assert response.status_code == 200
        assert 'Basis Set Exchange' in response.get_data(as_text=True)

    def test_404(self, client):
        response = client.get('/wrong/url')
        assert response.status_code == 404
        assert 'Page Not Found' in response.get_data(as_text=True)
