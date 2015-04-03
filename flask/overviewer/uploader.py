from flask import Blueprint, flash, render_template, redirect, url_for, request, make_response
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired

from . import auth
from .models import db, UploadedFile

uploader = Blueprint('uploader', __name__)

class UploadForm(Form):
    file = FileField('file', validators=[FileRequired()])

@uploader.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        m = UploadedFile.upload(form.file.data)
        flash('File {0} ({1}) uploaded successfully. MD5: {2}'.format(m.name, m.nice_size, m.md5))
        return redirect(url_for('.index'))

    files = None
    if auth.is_developer():
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        files = UploadedFile.query.order_by(UploadedFile.timestamp.desc()).paginate(page, per_page=50)

    return render_template('uploader_index.html', form=form, files=files)

@uploader.route('/progress')
def progress():
    # not used here
    return '{}'

@uploader.route('/<int:id>/<name>')
def download(id, name):
    # do not require login to facilitate wgettage
    m = UploadedFile.query.get_or_404(id)
    response = make_response('')
    response.headers['Content-Type'] = ''
    response.headers['X-Accel-Redirect'] = m.internal_url
    return response

@uploader.route('/<int:id>/delete')
@auth.developer_only
def delete(id):
    m = UploadedFile.query.get_or_404(id)
    m.delete()
    flash('File {0} deleted.'.format(m.name))
    return redirect(url_for('.index'))
    
