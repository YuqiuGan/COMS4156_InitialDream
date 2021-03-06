"""Import required packages."""
from flask import render_template, request, Blueprint
from flaskr.db import get_db
# import our OCR function
from ocr_core import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BP = Blueprint('ocr', __name__, url_prefix='/ocr')


# function to check the file extension
def allowed_file(filename):
    """Allowed type of files."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# route and function to handle the upload page
@BP.route('/upload', methods=['GET', 'POST'])
def upload_page():  # pylint: disable=inconsistent-return-statements
    """Upload image."""
    if request.method == 'POST':
        username = request.form['username']
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('/ocr/upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('/ocr/upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)

            if 'Negative' in extracted_text:
                database = get_db()
                database.execute('DELETE FROM yellow_pool WHERE yellow_user = ?',
                                 (username,))
                database.commit()
                return render_template('/ocr/upload.html',
                                       msg='Your tests result is Negative, '
                                           'you will recieve Green Pass!')

            return render_template('/ocr/upload.html',
                                   msg='Automatic identification failed. '
                                       'Please request manual '
                                       'identification!')
