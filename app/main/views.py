from flask import request, render_template, flash, g, \
                render_template_string, session, \
                redirect, url_for, send_from_directory,\
                current_app
import os
import json
from . import main
from ..models.logs import save_access
import logging
from flask_login import login_required, current_user
from flask import jsonify
from .data_loader import DataLoader
import bse

logger = logging.getLogger(__name__)

# Cached data for faster server load
data_loader = DataLoader()


@main.route('/')
def index():
    """Returns the main page of the BSE website"""

    formats = data_loader.formats
    basis_sets = data_loader.basis_sets

    # save_access(access=True, basis_download=False)

    return render_template('index.html', basis_sets=basis_sets, formats=formats)


@main.route('/web_metadata/')
def get_website_metadata():
    """Get Metadata of the whole basis sets
    """
    logger.info("Getting website metada")

    return jsonify({'metadata': data_loader.metadata,
                    'element_basis': data_loader.element_basis})


@main.route('/api/get_metadata/')
def get_meta_data():
    """Get Metadata of the whole basis sets
    """
    logger.info("Getting metada")

    return jsonify(data_loader.metadata)


def set_boolean(param: str) -> bool:
    if param in ('True', 'true', 1):
        return True
    else:
        return False


@main.route('/api/get_basis_set/<name>/')
@main.route('/api/get_basis_set/<name>/elements/<elements>/')
@main.route('/api/get_basis_set/<name>/format/<bs_format>/')
@main.route('/api/get_basis_set/<name>/elements/<elements>/format/<bs_format>/')
def get_basis_set(name, elements=None, bs_format='gaussian94'):
    """Get (download) specific basis set
    Note: can't use the fmt type dict in the api
    """
    uncontract_general = request.args.get('uncontract_general', default=False)
    uncontract_general = set_boolean(uncontract_general)

    if elements is not None:
        elements = [int(e) for e in elements.split(',')]

    # Log this basis set download into logging DB
    logger.info('REQUESTED BASIS SET: name=%s, elements=%s, format=%s, uncontract_general=%s',
                name, elements, bs_format, uncontract_general)
    # save_access(basis_set_name=name, basis_download=True, elements=elements, bs_format=bs_format)
    basis_set = bse.get_basis_set(name=name, elements=elements, fmt=bs_format,
                                  uncontract_general=uncontract_general)

    return basis_set


@main.route('/get_basis_set/<name>/')
@main.route('/get_basis_set/<name>/elements/<elements>/')
@main.route('/get_basis_set/<name>/format/<bs_format>/')
@main.route('/get_basis_set/<name>/elements/<elements>/format/<bs_format>/')
def get_basis_set_html(name, elements=None, bs_format='gaussian94'):
    results = get_basis_set(name, elements, bs_format)

    return render_template('show_basis_set.html', results=results)
