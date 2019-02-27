from flask import request, jsonify, render_template
import basis_set_exchange as bse
from . import main
from .views import data_loader


@main.app_errorhandler(404)
def not_found(error):
    error_data = {'error': True,
                  'message': str(error),
                  'url': request.url
                 }

    if request.path.startswith('/api/'):
        return jsonify(error_data), 404
    return render_template('404.html', error_data=error_data, formats=data_loader.formats,
                           help_data=data_loader.help_data), 404


@main.app_errorhandler(500)
def bse_library_exception(error):
    error_data = {'error': True,
                  'message': str(error),
                  'url': request.url
                 }

    if request.path.startswith('/api/'):
        return jsonify(error_data), 500
    return render_template('error.html', error_data=error_data, formats=data_loader.formats,
                           help_data=data_loader.help_data), 500
