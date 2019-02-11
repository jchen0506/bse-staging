from flask import current_app
import pytest
import re
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

    def test_log(self):
        # with context, to be able to use request and session
        with current_app.test_request_context():
            save_access('test_access', bs_name='3-21g',
                        elements=[1, 3], bs_fmt='gaussian94')

            assert Log.objects().count() != 0
            log = Log.objects().first()

            expect = r'access:test_access, api: False, bs_name: 3-21g, '\
                     r'fam_name: None, elements: \[1, 3\], bs_fmt: gaussian94, '\
                     r'ref_fmt: None, help_page: None, '\
                     r'user_agent: None, header_email: None, ip_address: None, ' \
                     r'date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'\

            assert bool(re.match(expect, str(log)))


    def test_homepage_log(self):
        # with context
        with current_app.test_request_context():
            save_access('homepage')
            log = Log.objects(access_type='homepage').first()

            expect = r'access:homepage, api: False, bs_name: None, fam_name: None, '\
                     r'elements: \[\], bs_fmt: None, '\
                     r'ref_fmt: None, help_page: None, '\
                     r'user_agent: None, header_email: None, ip_address: None, ' \
                     r'date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'\

            assert bool(re.match(expect, str(log)))
