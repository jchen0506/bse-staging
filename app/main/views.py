from flask import request, render_template, flash, g, \
                redirect, url_for, current_app
import os
from . import main
from ..models.logs import save_access
import logging
from flask import jsonify
from .data_loader import DataLoader
import bse

logger = logging.getLogger(__name__)

# Cached data for faster server load
data_loader = DataLoader()


##########################
# Helper functions
##########################
def set_boolean(param) -> bool:
    if isinstance(param, bool):
        return param
    else:
        return param.lower() in ('true', '1')


#############################
# API for the website itself
#############################

@main.route('/')
def index():
    """Returns the main page of the BSE website"""

    formats = data_loader.formats
    ref_formats = data_loader.ref_formats
    basis_sets = data_loader.basis_sets

    # save_access(access=True, basis_download=False)

    return render_template('index.html', basis_sets=basis_sets,
                                         formats=formats,
                                         ref_formats=ref_formats)


@main.route('/web_metadata/')
def web_metadata():
    """Get the metadata for all basis sets
    """
    logger.info("Getting website metada")

    return jsonify({'metadata': data_loader.metadata,
                    'element_basis': data_loader.element_basis})



###########################
# Raw API
###########################

@main.route('/api/formats/')
def api_formats():
    return jsonify(data_loader.formats)


@main.route('/api/metadata/')
def api_metadata():
    """Get Metadata of the whole basis sets
    """

    logger.info("Getting metada")
    return jsonify(data_loader.metadata)


@main.route('/api/basis/<name>/format/<bs_format>/')
def api_basis(name, bs_format):
    """Get (download) specific basis set
    Optional: elements (list of int), uncontract_general (bool),
              uncontract_segmented (bool), uncontract_spdf (bool),
              optimize_general (bool)
    """

    uncontract_general = request.args.get('uncontract_general', default=False)
    uncontract_segmented = request.args.get('uncontract_segmented', default=False)
    uncontract_spdf = request.args.get('uncontract_spdf', default=False)
    optimize_general = request.args.get('optimize_general', default=False)
    version = request.args.get('version', default=None)

    uncontract_general = set_boolean(uncontract_general)
    uncontract_segmented = set_boolean(uncontract_segmented)
    uncontract_spdf = set_boolean(uncontract_spdf)
    optimize_general = set_boolean(optimize_general)

    elements = request.args.get('elements', default=None)

    if elements is not None:
        elements = [int(e) for e in elements.split(',')]

    # Log this basis set download into logging DB
    logger.info('REQUESTED BASIS SET: name=%s, elements=%s, format=%s, uncontract_general=%s',
                name, elements, bs_format, uncontract_general)

    # save_access(basis_set_name=name, basis_download=True, elements=elements, bs_format=bs_format)
    basis_set = bse.get_basis(name=name, elements=elements, fmt=bs_format,
                              version=version,
                              uncontract_general=uncontract_general,
                              uncontract_segmented=uncontract_segmented,
                              uncontract_spdf=uncontract_spdf,
                              optimize_general=optimize_general)

    return basis_set


@main.route('/api/references/<basis_set_name>/format/<cformat>')
def api_references(basis_set_name, cformat):
    """Get the refrences for a given basis set name"""

    elements = request.args.get('elements', default=None)

    if elements is not None:
        elements = [int(e) for e in elements.split(',')]

    return bse.get_references(basis_set_name, elements=elements, fmt=cformat)


@main.route('/api/notes/<basis_set_name>')
def api_notes(basis_set_name):
    return bse.get_basis_notes(basis_set_name)


@main.route('/api/family_notes/<family>')
def api_family_notes(family):
    return bse.get_family_notes(family)


###############################
# API converted to HTML
###############################

@main.route('/basis/<name>/format/<bs_format>/')
def html_basis(name, bs_format):
    """Returns basis set in an HTML file"""

    data = api_basis(name, bs_format)
    return render_template('show_data.html', data=data)


@main.route('/references/<basis_set_name>/format/<cformat>')
def html_references(basis_set_name, cformat):
    """Get citations for a given basis set name"""

    data = api_references(basis_set_name, cformat)
    return render_template('show_data.html', data=data)


@main.route('/notes/<basis_set_name>')
def html_notes(basis_set_name):
    """Get citations for a given basis set name"""

    data = api_notes(basis_set_name)
    return render_template('show_data.html', data=data)


@main.route('/family_notes/<family>')
def html_family_notes(family):
    data = api_family_notes(family)
    return render_template('show_data.html', data=data)
