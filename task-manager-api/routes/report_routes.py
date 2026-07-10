from flask import Blueprint, request, jsonify
from controllers import report_controller, category_controller
from middlewares.error_handler import AppError

report_bp = Blueprint('reports', __name__)


@report_bp.route('/reports/summary', methods=['GET'])
def summary_report_route():
    report = report_controller.get_summary_report()
    return jsonify(report), 200


@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report_route(user_id):
    report, error = report_controller.get_user_report(user_id)
    if error:
        raise AppError(error, 404)
    return jsonify(report), 200
