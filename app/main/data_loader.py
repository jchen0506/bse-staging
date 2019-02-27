import os
import basis_set_exchange as bse
from basis_set_exchange import converters, refconverters
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

        self.format_ext = {fmt: converters.get_format_extension(fmt)
                           for fmt in self.formats}
        self.ref_format_ext = {fmt: refconverters.get_format_extension(fmt)
                               for fmt in self.ref_formats}

        self.element_basis = {str(i): [] for i in range(1, 119)}
        for element in self.element_basis:
            for basis in self.metadata:
                latest = self.metadata[basis]['latest_version']
                if element in self.metadata[basis]['versions'][latest]['elements']:
                    self.element_basis[element].append(basis)


        # Load contents of help, feedback, etc
        self.help_data = {'feedback':
                               { 'title': 'Feedback',
                               },
                          'about':
                               { 'title': 'About',
                               },
                         }

        for k,v in self.help_data.items():
            help_path = os.path.join(self.my_dir, 'help', k + '.html')
            with open(help_path, 'r') as hf:
                v['contents'] =  hf.read()
