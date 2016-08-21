from flask.ext.admin import BaseView, expose
from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueAide(BaseView):
    
    @expose('/')
    def index(self):
        return self.render('admin/aide.html')
        
admin.add_view(
    VueAide(
        name='Aide',
        url='aide'
    )
)