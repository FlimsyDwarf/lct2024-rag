from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from report_generator import ReportGenerator
from time import ctime
import shutil

# Create a blueprint
api = Blueprint('api', __name__, url_prefix='/api/1')

# Allowed extensions for file upload
# ALLOWED_EXTENSIONS = {'pdf', 'txt'}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER_DOCS = './data'
'''
request consists of: files, userSources, dateRange, useInternet.
useInternet: boolean
userSources: list of user sources
dateRange: list of dates, of size 1 or 2.
'''


@api.route('/make_request', methods=['POST'])
def make_request():
    suffix = ctime().replace(' ', '_').replace(':', '_')
    data = request.form
    files = request.files
    user_sources = data.get('userSources', None)
    use_internet = True if (data.get('useInternet', 'false') == 'true') else False
    date_range = data.get('dateRange', None)

    # save tempalte
    template = files['template']
    filename = secure_filename(template.filename)
    dir_path = os.path.join(UPLOAD_FOLDER_DOCS, suffix)
    os.mkdir(dir_path)
    template.save(os.path.join(dir_path, "shablon.docx"))

    # save user docs
    for i in range(len(files) - 1):
        f = files['file' + str(i)]
        filename = secure_filename(f.filename)
        f.save(os.path.join(dir_path, filename))

    # generate report
    report_generator = ReportGenerator(
        use_internet, user_sources, date_range, suffix)
    report_generator.generate_report()

    # send_file('./backend/data/report.docx', as_attachment=True)
    shutil.rmtree(dir_path)
    return jsonify({'OK': suffix}), 200


@api.route('/download_result', methods=['POST'])
def download_result():
    data = request.form
    suffix = data.get('suffix', '')
    return send_file(os.path.join(UPLOAD_FOLDER_DOCS, suffix + "report.docx"),
                     as_attachment=True,
                     download_name='report.docx')
