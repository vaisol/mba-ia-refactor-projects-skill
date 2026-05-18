from flask import Blueprint, request, jsonify
from services.report_service import ReportService

report_bp = Blueprint('reports', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    try:
        report = ReportService.get_summary_report()
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report(user_id):
    try:
        report = ReportService.get_user_report(user_id)
        if not report:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
