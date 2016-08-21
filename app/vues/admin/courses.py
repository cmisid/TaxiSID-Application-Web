from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueCourse(VueModele):

    ''' Informations sur les courses. '''

    can_create = True
    can_edit = True
    can_delete = True



    form_columns = [
    	'utilisateur',
        'entreprise',
    	'places',
    	'priorite',
        'debut',
        'commentaire',
        'bagages',
        'animaux',
	    'animaux_grands',
        'gare',
        'aeroport',
        'depart',
        'arrivee'
    ]

    column_default_sort = ('numero', True)

class VueCourseInfo(VueCourse):

    column_searchable_list = [
        'numero',
        'utilisateur',
        'conducteur',
        'entreprise',
        'finie',
        'places',
        'priorite',
        'debut',
        'fin',
        'distance_estimee'
    ]

    column_list = [
        'numero',
        'conducteur',
        'utilisateur',
        'entreprise',
        'finie',
        'places',
        'priorite',
        'debut',
        'fin',
        'distance_estimee'
    ]


admin.add_view(
	VueCourseInfo(
		modeles.Course,
		db.session,
        endpoint = 'CourseInfo',
        name ='Informations',
        category = 'Course'
	)
)

class VueCourseComplements(VueCourse):

    column_searchable_list = [
        'numero',
        'trouvee',
        'commentaire',
        'bagages',
        'animaux',
        'animaux_grands',
        'gare',
        'aeroport',
        'anglais'
    ]

    column_list = [
        'numero',
        'trouvee',
        'commentaire',
        'bagages',
        'animaux',
        'animaux_grands',
        'gare',
        'aeroport',
        'anglais'
    ]

admin.add_view(
    VueCourseComplements(
        modeles.Course,
        db.session,
        endpoint = 'CourseComplements',
        name ='Compléments',
        category = 'Course'
    )
)
