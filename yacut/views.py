from flask import abort, flash, render_template, redirect, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap

from utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if not short_id:
            short_id = get_unique_short_id()
            if URLMap.query.filter_by(short=short_id).first() is not None:
                short_id = get_unique_short_id()
        if URLMap.query.filter_by(short=short_id).first() is not None:
            flash(f'Имя {short_id} уже занято!')
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(url_map)
        db.session.commit()
        flash(url_for('short_id_view', short_id=short_id, _external=True))
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def short_id_view(short_id):
    short_link = URLMap.query.filter_by(short=short_id).first()
    if short_link is not None:
        return redirect(short_link.original)
    abort(404)
