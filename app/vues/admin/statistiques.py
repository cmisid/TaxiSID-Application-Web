from flask.ext.admin import BaseView, expose
from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueStatistiques(BaseView):
    
    @expose('/')
    def index(self):
        return self.render('admin/statistiques.html')
        
admin.add_view(
    VueStatistiques(
        name='Statistiques',
        url='statistiques'
    )
)