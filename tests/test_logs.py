from flask import current_app
import pytest
from app.models.logs import Log, save_access


@pytest.mark.usefixtures("app", "client")
class TestDatabase(object):
    """
        Testing Log DB CRUD operations
    """

    def test_app_exists(self):
        assert current_app is not None

    def test_db_exit(self):
        Log.objects.delete()
        assert Log.objects().count() == 0

    def test_add_log(self):
        # with context, to be able to use request and session
        with current_app.test_request_context():
            save_access(download=True, bs_name='3-21g', bs_format='gaussian94',
                        elements=[1, 3])

            assert Log.objects().count() != 0
            log = Log.objects().first()
            assert str(log) == 'Download:True, basis_set_name: 3-21g, ' \
                               'bs_format: gaussian94, IP_address: None'

    def test_non_doanload_log(self):
        # with context
        with current_app.test_request_context():
            save_access(download=False)

            log = Log.objects(download=False).first()
            assert not log.download
            assert not log.bs_name
