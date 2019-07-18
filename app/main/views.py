import os
import logging
import basis_set_exchange as bse
import basis_set_exchange_archive as bsea
from flask import (request, render_template, Response, jsonify, current_app,
                   send_from_directory, safe_join, flash)
from . import main
from .data_loader import DataLoader
from ..models.logs import save_access
from ..models.feedback import BasisRequest
from .forms import BasisRequestForm

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

@main.route('/', methods=['GET', 'POST'])
def index():
    """Returns the main page of the BSE website"""

    formats = data_loader.formats
    ref_formats = data_loader.ref_formats
    basis_sets = data_loader.basis_sets
    roles = data_loader.roles

    save_access(access_type='homepage')

    return render_template('index.html',
                           basis_sets=basis_sets,
                           formats=formats,
                           ref_formats=ref_formats,
                           roles=roles)


@main.route('/web_metadata/')
def web_metadata():
    """Get the metadata for all basis sets

    The output is JSON
    """

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

    save_access(access_type='get_formats')
    return jsonify(data_loader.formats)


@main.route('/api/reference_formats/')
def api_reference_formats():
    """Get the possible output formats for references (as JSON)

    The output is a key->value with the key being the format
    key and the value being a human-readable name

    The format key is passed into other API calls.
    """

    save_access(access_type='get_ref_formats')
    return jsonify(data_loader.ref_formats)


@main.route('/api/metadata/')
def api_metadata():
    """Get the metadata for all the basis sets (as JSON)

    The metadata for a basis set contains the description, the versions,
    function types, and elements defined by the basis set.
    """

    save_access(access_type='get_metadata')
    return jsonify(data_loader.metadata)


@main.route('/api/basis/<basis_name>/format/<fmt>/')
@main.route('/download_basis/basis/<basis_name>/format/<fmt>/')
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

    # Force the latest version if none
    if version is None:
        basis_name = bse.misc.transform_basis_name(basis_name)
        basis_md = data_loader.metadata[basis_name]
        version = basis_md['latest_version']

    elements = request.args.getlist('elements')


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

    access_type = 'get_basis'

    # Is this a download?
    if request.path.lower().startswith('/download_basis/'):
        access_type = 'download_basis'

    save_access(access_type=access_type, basis_name=basis_name, basis_version=version, elements=elements, basis_format=fmt,
                uncontract_general=uncontract_general, uncontract_segmented=uncontract_general,
                uncontract_spdf=uncontract_spdf, make_general=make_general, optimize_general=optimize_general)

    if fmt.lower() == 'json':
        return Response(basis_set, mimetype='application/json')
    else:
        return Response(basis_set, mimetype='text/plain')


@main.route('/api/references/<basis_name>/format/<fmt>/')
@main.route('/download_references/references/<basis_name>/format/<fmt>/')
def api_references(basis_name, fmt):
    """Get the references/citations for a given basis set

    The elements can also be specified.

    Available reference formats can found with `/api/reference_formats`

    The response mimetype depends on the format. If the format
    is json, is is 'application/json'. Otherwise, it is 'text/plain'
    """

    elements = request.args.getlist('elements')
    version = request.args.get('version', default=None)
    refs = bse.get_references(basis_name, elements=elements, fmt=fmt, version=version)

    access_type = 'get_references'

    # Is this a download?
    if request.path.lower().startswith('/download_references/'):
        access_type = 'download_references'

    save_access(access_type=access_type, basis_name=basis_name, basis_version=version, elements=elements, reference_format=fmt)

    # Force the latest version if none
    if version is None:
        basis_name = bse.misc.transform_basis_name(basis_name)
        basis_md = data_loader.metadata[basis_name]
        version = basis_md['latest_version']

    if fmt.lower() == 'json':
        return Response(refs, mimetype='application/json')
    else:
        return Response(refs, mimetype='text/plain')


@main.route('/api/notes/<basis_name>/')
def api_notes(basis_name):
    """Get text notes about a basis set"""

    notes = bse.get_basis_notes(basis_name)
    if notes == '':
        notes = 'Notes for the basis set "{}" do not exist'.format(basis_name)

    save_access(access_type='get_notes', basis_name=basis_name)
    return Response(notes, mimetype='text/plain')


@main.route('/api/family_notes/<family>/')
def api_family_notes(family):
    """Get text notes about a basis set family"""

    notes = bse.get_family_notes(family)
    if notes == '':
        notes = 'Notes for the family "{}" do not exist'.format(family)

    save_access(access_type='get_family_notes', family_name=family)
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
    dl_link = web_link.replace(root, root + 'download_basis/')

    # Construct an appropriate filename
    version = request.args.get('version', default=None)
    if version is None:
        basis_name = bse.misc.transform_basis_name(basis_name)
        basis_md = data_loader.metadata[basis_name]
        version = basis_md['latest_version']

    # Note that _get_basis_extension already includes the leading dot
    bs_filename = bse.misc.basis_name_to_filename(basis_name)
    dl_filename = '{}.{}{}'.format(bs_filename, version, _get_basis_extension(fmt))

    return render_template('show_data.html',
                           data=data,
                           api_link=api_link,
                           dl_link=dl_link,
                           web_link=web_link,
                           dl_filename=dl_filename,
                           show_topbox=True)


@main.route('/references/<basis_name>/format/<fmt>/')
def html_references(basis_name, fmt):
    """Render a page with basis set reference data"""

    data = api_references(basis_name, fmt).get_data(as_text=True)

    root = request.url_root
    web_link = request.url
    api_link = web_link.replace(root, root + 'api/')
    dl_link = web_link.replace(root, root + 'download_references/')

    # Construct an appropriate filename
    version = request.args.get('version', default=None)
    if version is None:
        basis_name = bse.misc.transform_basis_name(basis_name)
        basis_md = data_loader.metadata[basis_name]
        version = basis_md['latest_version']

    # Note that _get_ref_extension already includes the leading dot
    bs_filename = bse.misc.basis_name_to_filename(basis_name)
    dl_filename = '{}.{}{}'.format(bs_filename, version, _get_ref_extension(fmt))

    return render_template('show_data.html',
                           data=data,
                           api_link=api_link,
                           dl_link=dl_link,
                           web_link=web_link,
                           dl_filename=dl_filename,
                           show_topbox=True)


@main.route('/notes/<basis_name>/')
def html_notes(basis_name):
    """Render a page with basis set notes"""

    data = api_notes(basis_name).get_data(as_text=True)

    return render_template('show_data.html',
                           data=data,
                           show_topbox=False)


@main.route('/family_notes/<family>/')
def html_family_notes(family):
    """Render a page with basis set family notes"""

    data = api_family_notes(family).get_data(as_text=True)

    return render_template('show_data.html',
                           data=data,
                           show_topbox=False)


#################################
# Help pages, documentation, etc
#################################

@main.route('/help/<page>')
def html_help_page(page):
    """Render a help page"""

    # Left for future uses
    help_pages = ['help_page']
    if page not in help_pages:
        raise RuntimeError("Help page {} does not exist".format(page))

    page_name = page + '.html'

    save_access(access_type='help_page', help_page=page)

    return render_template('help/' + page_name)


###################################
# Downloads
###################################

@main.route('/api/download/<ver>/<fmt>/<archive_type>')
@main.route('/download/<ver>/<fmt>/<archive_type>')
def download_file(fmt, archive_type, ver):
    if not fmt in data_loader.formats:
        raise RuntimeError("'{}' is not a valid format".format(fmt))
    if not archive_type in data_loader.archive_types:
        raise RuntimeError("'{} is not a valid archive type".format(archive_type))

    ext = data_loader.archive_types[archive_type]['extension']

    if ver == 'current':
        ver = bse.version()

    filename = 'basis_sets-' + fmt + '-' + ver + ext
    filedir = safe_join(bsea.get_data_ver_dir())
    fullpath = safe_join(filedir, filename)

    if os.path.isfile(fullpath):
        save_access(access_type='download_all', basis_format=fmt)

    return send_from_directory(filedir, filename, as_attachment=True, attachment_filename=filename)

######################################
# Feedback and Basis request
######################################

@main.route('/request_basis/', methods=['GET', 'POST'])
def request_basis():

    form = BasisRequestForm()
    if form.validate_on_submit():
        basis_request = BasisRequest(
            name=form.name.data,
            email = form.email.data,
            requested_basis = form.requested_basis.data,
            other_basis = form.other_basis.data,
            basis_format = form.basis_format.data,
            comments=form.comments.data,
        )
        basis_request.save()
        flash('Your request has been submitted successfully!', 'success')
        return jsonify({'status': True})

    save_access(access_type='basis_request')

    return render_template('request_basis.html', form=form)
