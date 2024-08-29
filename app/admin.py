from flask_admin import Admin, BaseView, expose, form
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import current_user
from flask_babel import Babel
from sqlalchemy.event import listens_for
from flask import url_for
from markupsafe import Markup
from .widgets import CKTextAreaField
from .utils import get_locale
from .models import  db, RoleEnum, Category, User, Book, Tag

import os, os.path as op

path = op.join(op.dirname(__file__), 'static')
file_path = op.join(op.dirname(__file__),
                      f"static/images/")

try:
    os.mkdir(file_path)
except OSError:
    pass


@listens_for(Book, 'after_delete')
def del_image(mapper, connection, target):
    if target.image:
        try:
            os.remove(op.join(file_path, target.image))
        except OSError:
            pass

        try:
            os.remove(op.join(file_path, form.thumbgen_filename(target.image)))
        except OSError:
            pass


class AuthModelView(BaseView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.role == RoleEnum.ADMIN
    
    pass


class EBookModelView(AuthModelView, ModelView):
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    can_export = True
    can_delete = True
    column_list = ["active", "date_created"]
    column_filters = ["active"]
    column_editable_list = ["active"]
    column_sortable_list = ["date_created"]

    
class UserModelView(EBookModelView):
    column_list = ["username", "email"] + EBookModelView.column_list
    column_searchable_list = ["username", "email"]
    column_editable_list = ["username"] + EBookModelView.column_editable_list
    column_sortable_list = ["username"] + EBookModelView.column_sortable_list
    column_exclude_list = ['password']
    
    
class CategoryModelView(EBookModelView):
    column_list = ["name", "books"] + EBookModelView.column_list
    column_searchable_list = ["name"]
    column_sortable_list = ["name"] + EBookModelView.column_sortable_list
    column_editable_list = ["name"] + EBookModelView.column_editable_list
    

class BookModelView(EBookModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'description': CKTextAreaField
    }
    
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return Markup(f'<img src="{model.image}" alt="{model.title}" class="img-thumbnail rounded-circle shadow" />')

        return Markup(f'<img src="{url_for('static', filename=f"images/{form.thumbgen_filename(model.image)}")}" alt="{model.title}" width="80" height="80" class="img-thumbnail rounded-circle shadow" />')

    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'image': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }
    
    column_list = ["title", "image", "price", "category"] + EBookModelView.column_list
    column_searchable_list = ["title"]
    create_modal = False
    edit_modal = False
    column_sortable_list = ["title", "price"] + EBookModelView.column_sortable_list
    column_editable_list = ["title", "price", "category"] + EBookModelView.column_editable_list
    column_filters = ["price"] + EBookModelView.column_filters
    inline_models = [Tag]
    
    
class TagModelView(EBookModelView):
    column_list = ["name", "books"] + EBookModelView.column_list
    column_sortable_list = ["name"] + EBookModelView.column_sortable_list
    column_editable_list = ["name"] + EBookModelView.column_editable_list
 
 
class AnalyticsView(AuthModelView):
    @expose('/')
    def index(self):
        return self.render('admin/analytics.html')
    
    
class UploadFilesView(AuthModelView, FileAdmin):
    pass


babel = Babel(locale_selector=get_locale)
admin_manager = Admin(name='eBook 📖', template_mode='bootstrap4')
admin_manager.add_view(UserModelView(User, db.session, category="Collections"))
admin_manager.add_view(CategoryModelView(Category, db.session, category="Collections"))
admin_manager.add_view(BookModelView(Book, db.session, category="Collections"))
admin_manager.add_view(TagModelView(Tag, db.session, category="Collections"))
admin_manager.add_view(AnalyticsView(name='Analytics', endpoint='analytics', category="Utils")) 
admin_manager.add_view(UploadFilesView(path, '/static/', name='Files', endpoint="files", category="Utils"))