import bse
import logging
logger = logging.getLogger(__name__)


class DataLoader(object):
    """Cache basis set metadata for faster server load"""

    def __init__(self):
        logger.info('Creating cached data')
        self.formats = bse.get_formats()
        self.metadata = bse.get_metadata()
        self.basis_sets = sorted(self.metadata.keys(), key=lambda v: v.upper())
        logger.info(self.basis_sets)

        self.element_basis = {i: [] for i in range(1, 119)}
        for element in self.element_basis:
            for basis in self.metadata:
                if element in self.metadata[basis][0]['elements']:
                    self.element_basis[element].append(basis)
