from flask import render_template, redirect, flash, abort
from http import HTTPStatus

from . import app
from .forms import YacutForm, FileUploadForm
from .models import URLMap
from .yadisk import upload_files_to_yadisk

UPLOAD_ERROR = 'Ошибка при загрузке файлов - {}'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.create(
                form.original_link.data,
                form.custom_id.data
            ).get_short_url()
        )
    except (URLMap.ObjectCreateError, URLMap.ShortGenerateError) as exc:
        flash(exc)
        return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def file():
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template('upload_files.html', form=form)
    try:
        return render_template(
            'upload_files.html',
            form=form,
            filenames_and_short_urls=[
                dict(
                    filename=file_info['filename'],
                    short_url=URLMap.create(file_info['url']).get_short_url()
                ) for file_info in await upload_files_to_yadisk(
                    form.files.data
                )
            ]
        )
    except (URLMap.ObjectCreateError, URLMap.ShortGenerateError) as exc:
        flash(exc)
        return render_template('upload_files.html', form=form)
    except Exception as exc:
        flash(UPLOAD_ERROR.format(exc))
        return render_template('upload_files.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    url_map = URLMap.get(custom_id)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)