from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from extensions import basic_auth


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not basic_auth.authenticate():
            return basic_auth.challenge()
        return super(MyAdminIndexView, self).index()


class SecureModelView(ModelView):
    def is_accessible(self):
        return basic_auth.authenticate()

    def inaccessible_callback(self, name, **kwargs):
        return basic_auth.challenge()
