import os
import logging
import basis_set_exchange as bse
from flask import request, render_template, Response, jsonify, json, current_app
from . import main
from .data_loader import DataLoader
from ..models.logs import save_access

logger = logging.getLogger(__name__)

# Cached data for faster server load
data_loader = DataLoader()


##########################
# Helper functions
##########################
def _set_boolean(param):
    """Converts param to a boolean

    If `param` is a bool, then no conversion is performed.

    If `param` is a string, the True is returned if the string
    is 'true' or '1' (case insensitive).
    """

    if isinstance(param, bool):
        return param
    else:
        return param.lower() in ('true', '1')


def _get_basis_extension(fmt):
    """Obtain the extension for a basis set file based on format"""
    return data_loader.format_ext[fmt.lower()]


def _get_ref_extension(fmt):
    """Obtain the extension for a references file based on format"""
    return data_loader.ref_format_ext[fmt.lower()]


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

    return render_template('index.html',
                           basis_sets=basis_sets,
                           formats=formats,
                           ref_formats=ref_formats)


@main.route('/web_metadata/')
def web_metadata():
    """Get the metadata for all basis sets

    The output is JSON
    """

    logger.info('WEB: getting web metadata')
    return jsonify({'metadata': data_loader.metadata,
                    'element_basis': data_loader.element_basis})


##########################################
# Raw API
# This API is expected to be used
# programmatically, and not from a browser
##########################################

@main.route('/api/formats/')
def api_formats():
    """Get the possible output formats for basis sets (as JSON)

    The output is a key->value with the key being the format
    key and the value being a human-readable name

    The format key is passed into other API calls.
    """

    logger.info('API: formats')
    return jsonify(data_loader.formats)


@main.route('/api/reference_formats/')
def api_reference_formats():
    """Get the possible output formats for references (as JSON)

    The output is a key->value with the key being the format
    key and the value being a human-readable name

    The format key is passed into other API calls.
    """

    logger.info('API: reference formats')
    return jsonify(data_loader.ref_formats)


@main.route('/api/metadata/')
def api_metadata():
    """Get the metadata for all the basis sets (as JSON)

    The metadata for a basis set contains the description, the versions,
    function types, and elements defined by the basis set.
    """

    logger.info('API: metadata')
    return jsonify(data_loader.metadata)


@main.route('/api/basis/<basis_name>/format/<fmt>/')
def api_basis(basis_name, fmt):
    """Get a basis set

    Available formats can found with `/api/formats`

    The response mimetype depends on the format. If the format
    is json, is is 'application/json'. Otherwise, it is 'text/plain'

    Optional: elements (list of str),
              uncontract_general (bool),
              uncontract_segmented (bool),
              uncontract_spdf (bool),
              optimize_general (bool),
              make_general (bool)
              header (bool)
    """

    uncontract_general = request.args.get('uncontract_general', default=False)
    uncontract_segmented = request.args.get('uncontract_segmented', default=False)
    uncontract_spdf = request.args.get('uncontract_spdf', default=False)
    optimize_general = request.args.get('optimize_general', default=False)
    make_general = request.args.get('make_general', default=False)
    header = request.args.get('header', default=True)

    uncontract_general = _set_boolean(uncontract_general)
    uncontract_segmented = _set_boolean(uncontract_segmented)
    uncontract_spdf = _set_boolean(uncontract_spdf)
    optimize_general = _set_boolean(optimize_general)
    make_general = _set_boolean(make_general)
    header = _set_boolean(header)

    version = request.args.get('version', default=None)
    elements = request.args.get('elements', default=None)

    if elements is not None:
        elements = elements.split(',')

    logger.info('API: basis: name=%s, ver=%s, elements=%s, format=%s, opts=%s,%s,%s,%s,%s',
                basis_name, version, elements, fmt, uncontract_general, uncontract_segmented,
                uncontract_spdf, optimize_general, make_general)

    basis_set = bse.get_basis(name=basis_name, elements=elements, fmt=fmt,
                              version=version,
                              uncontract_general=uncontract_general,
                              uncontract_segmented=uncontract_segmented,
                              uncontract_spdf=uncontract_spdf,
                              optimize_general=optimize_general,
                              make_general=make_general,
                              header=header)

    if current_app.config['DB_LOGGING']:
        save_access(download=True, bs_name=basis_name, elements=elements, bs_format=fmt)

    if fmt.lower() == 'json':
        return Response(basis_set, mimetype='application/json')
    else:
        return Response(basis_set, mimetype='text/plain')


@main.route('/api/references/<basis_name>/format/<fmt>/')
def api_references(basis_name, fmt):
    """Get the references/citations for a given basis set

    The elements can also be specified.

    Available reference formats can found with `/api/reference_formats`

    The response mimetype depends on the format. If the format
    is json, is is 'application/json'. Otherwise, it is 'text/plain'
    """

    elements = request.args.get('elements', default=None)

    if elements is not None:
        elements = elements.split(',')

    logger.info('API: references: name=%s elements=%s format=%s', basis_name, elements, fmt)

    refs = bse.get_references(basis_name, elements=elements, fmt=fmt)

    if fmt.lower() == 'json':
        return Response(refs, mimetype='application/json')
    else:
        return Response(refs, mimetype='text/plain')


@main.route('/api/notes/<basis_name>/')
def api_notes(basis_name):
    """Get text notes about a basis set"""

    logger.info('API: basis notes: %s', basis_name)
    notes = bse.get_basis_notes(basis_name)
    return Response(notes, mimetype='text/plain')


@main.route('/api/family_notes/<family>')
def api_family_notes(family):
    """Get text notes about a basis set family"""

    logger.info('API: family notes: %s', family)
    notes = bse.get_family_notes(family)
    return Response(notes, mimetype='text/plain')


###############################
# API converted to HTML
###############################


@main.route('/basis/<basis_name>/format/<fmt>/')
def html_basis(basis_name, fmt):
    """Render a page with basis set data"""

    data = api_basis(basis_name, fmt).get_data(as_text=True)

    root = request.url_root
    web_link = request.url
    api_link = web_link.replace(root, root + 'api/')
    dl_filename = basis_name + _get_basis_extension(fmt)
    return render_template('show_data.html',
                           data=data,
                           api_link=api_link,
                           web_link=web_link,
                           dl_filename=dl_filename)


@main.route('/references/<basis_name>/format/<fmt>/')
def html_references(basis_name, fmt):
    """Render a page with basis set reference data"""

    data = api_references(basis_name, fmt).get_data(as_text=True)

    root = request.url_root
    web_link = request.url
    api_link = web_link.replace(root, root + 'api/')
    dl_filename = basis_name + _get_ref_extension(fmt)

    return render_template('show_data.html',
                           data=data,
                           api_link=api_link,
                           web_link=web_link,
                           dl_filename=dl_filename)


@main.route('/notes/<basis_name>/')
def html_notes(basis_name):
    """Render a page with basis set notes"""

    data = api_notes(basis_name).get_data(as_text=True)

    root = request.url_root
    web_link = request.url
    api_link = web_link.replace(root, root + 'api/')
    dl_filename = basis_name + ".txt"

    return render_template('show_data.html',
                           data=data,
                           api_link=api_link,
                           web_link=web_link,
                           dl_filename=dl_filename)


@main.route('/family_notes/<family>')
def html_family_notes(family):
    """Render a page with basis set family notes"""

    data = api_family_notes(family).get_data(as_text=True)

    root = request.url_root
    web_link = request.url
    api_link = web_link.replace(root, root + 'api/')
    dl_filename = family + ".txt"

    return render_template('show_data.html',
                           data=data,
                           api_link=api_link,
                           web_link=web_link,
                           dl_filename=dl_filename)


#################################
# Help pages, documentation, etc
#################################
@main.route('/help/<page>')
def html_help_page(page):
    """Render a help page"""

    help_pages = ['about', 'basis_info']
    if page not in help_pages:
        raise RuntimeError("Help page {} does not exist".format(page))

    # Read in the partial HTML
    app_root = current_app.root_path
    html_file = os.path.join(app_root, 'help', page + '.html')
    if not os.path.isfile(html_file):
        raise RuntimeError("Help page {} does not exist".format(page))

    with open(html_file, 'r') as f:
        html_data = f.read()

    return render_template('help_page.html',  help_contents=html_data)
