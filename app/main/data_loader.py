import os
import datetime
import basis_set_exchange as bse
from basis_set_exchange import writers, refconverters
import logging
logger = logging.getLogger(__name__)


class DataLoader(object):
    """Cache basis set metadata for faster server load"""

    def __init__(self):
        logger.info('Creating cached data')
        self.my_dir = os.path.dirname(os.path.abspath(__file__))

        self.metadata = bse.get_metadata()
        self.formats = bse.get_formats()
        self.ref_formats = bse.get_reference_formats()
        self.roles = bse.get_roles()
        self.basis_sets = sorted((k, v['display_name']) for k, v in self.metadata.items())

        self.format_ext = {fmt: writers.get_format_extension(fmt)
                           for fmt in self.formats}
        self.ref_format_ext = {fmt: refconverters.get_format_extension(fmt)
                               for fmt in self.ref_formats}
        self.archive_types = bse.get_archive_types()

        # Change dates to be more readable
        for bs_data in self.metadata.values():
            for ver_data in bs_data['versions'].values():
                revdate = datetime.date.fromisoformat(ver_data['revdate'])
                ver_data['revdate'] = revdate.strftime('%B %-d, %Y')

        # Store whether notes exist for basis sets/families
        for bs in self.metadata.keys():
            fam = self.metadata[bs]['family']
            self.metadata[bs]['notes_exist'] = (bse.has_basis_notes(bs), bse.has_family_notes(fam))

        self.element_basis = {str(i): [] for i in range(1, 119)}
        for element in self.element_basis:
            for basis in self.metadata:
                latest = self.metadata[basis]['latest_version']
                if element in self.metadata[basis]['versions'][latest]['elements']:
                    self.element_basis[element].append(basis)
