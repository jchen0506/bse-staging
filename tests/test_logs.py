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
            save_access('test_access', basis_name='3-21g',
                        elements=[1, 3], basis_format='gaussian94')

            assert Log.objects().count() != 0
            log = Log.objects().first()

            expect = r'access: test_access, api: False, basis_name: 3-21g, basis_version: None, '\
                     r'family_name: None, elements: \[1, 3\], basis_format: gaussian94, '\
                     r'reference_format: None, help_page: None, '\
                     r'user_agent: None, header_email: None, ip_address: None, referrer: None, ' \
                     r'uncontract_general: False, uncontract_segmented: False, uncontract_spdf: False, ' \
                     r'make_general: False, optimize_general: False, ' \
                     r'date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'\

            assert bool(re.match(expect, str(log)))


    def test_homepage_log(self):
        # with context
        with current_app.test_request_context():
            save_access('homepage')
            log = Log.objects(access_type='homepage').first()

            expect = r'access: homepage, api: False, basis_name: None, basis_version: None, '\
                     r'family_name: None, elements: \[\], basis_format: None, '\
                     r'reference_format: None, help_page: None, '\
                     r'user_agent: None, header_email: None, ip_address: None, referrer: None, ' \
                     r'uncontract_general: False, uncontract_segmented: False, uncontract_spdf: False, ' \
                     r'make_general: False, optimize_general: False, ' \
                     r'date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'\

            assert bool(re.match(expect, str(log)))
