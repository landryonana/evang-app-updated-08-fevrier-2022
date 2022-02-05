from django.shortcuts import render, redirect
from django.forms import modelformset_factory
import datetime
from datetime import date

from evangelisation.models import Participant, Person, Site, Evangelisation
from evangelisation.forms import *


def get_personne_evang_by_mois_and_year(mois, year):
    evangs = None
    models = []

    evangs = Evangelisation.objects.filter(day__month=mois, day__year=year)
    for evang in evangs:
        for ps in evang.personnes.all():
            models.append(ps)
    return models


def get_personne_evang_by_year(year):
    evangs = None
    models = []
    evangs = Evangelisation.objects.filter(day__year=year)
    for evang in evangs:
        for ps in evang.personnes.all():
            models.append(ps)
    return models


def get_personne_evang_by_jour_and_mois_and_year(jour, mois, year):
    evangs = None
    models = []

    evangs = Evangelisation.objects.filter(day__day=jour, day__month=mois, day__year=year)
    for evang in evangs:
        for ps in evang.personnes.all():
            models.append(ps)
    return models


def month_numer(name_mois):
    if name_mois == "Janvier":
        return 1
    elif name_mois == "Févier":
        return 2
    elif name_mois == "Mars":
        return 3
    elif name_mois == "Avril":
        return 4
    elif name_mois == "Mai":
        return 5
    elif name_mois == "Juin":
        return 6
    elif name_mois == "Juillet":
        return 7
    elif name_mois == "Aout":
        return 8
    elif name_mois == "Septembre":
        return 9
    elif name_mois == "Octobre":
        return 10
    elif name_mois == "Novembre":
        return 11
    elif name_mois == "Décembre":
        return 12


def month_name(number):
    if number == 1:
        return "Janvier"
    elif number == 2:
        return "Févier"
    elif number == 3:
        return "Mars"
    elif number == 4:
        return "Avril"
    elif number == 5:
        return "Mai"
    elif number == 6:
        return "Juin"
    elif number == 7:
        return "Juillet"
    elif number == 8:
        return "Aout"
    elif number == 9:
        return "Septembre"
    elif number == 10:
        return "Octobre"
    elif number == 11:
        return "Novembre"
    elif number == 12:
        return "Décembre"



def get_personne_total(all_evang):
    #==================================Total==================================================================
    all_count_sortie = 0
    all_ps_evg = 0
    all_oui_JESUS = 0
    all_prc_oui_JESUS = 0
    all_rester = 0
    all_count_femme = 0
    all_count_homme = 0
    all_count_boss = 0
    mois = None

    for all in all_evang:
        mois = all['mois']
        all_count_sortie = all_count_sortie + all['count_sortie']
        all_ps_evg = all_ps_evg + all['ps_evg']
        all_oui_JESUS = all_oui_JESUS + all['oui_JESUS']

        prc_oui_JESUS = 0
        if all['prc_oui_JESUS']:
            prc_oui_JESUS = all['prc_oui_JESUS']
        else:
            prc_oui_JESUS = 0
        all_prc_oui_JESUS = all_prc_oui_JESUS + float(prc_oui_JESUS)
        all_rester = all_rester + all['rester']
        all_count_homme = all_count_homme + all['count_homme']
        all_count_femme = all_count_femme + all['count_femme']
        all_count_boss = all_count_boss + all['count_boss']
    
    all_prc_oui_JESUS = float("{:.2f}".format(all_prc_oui_JESUS/12))
    
    total = {
        'all_count_sortie':all_count_sortie,
        'all_ps_evg': all_ps_evg,
        'all_oui_JESUS': all_oui_JESUS,
        'all_prc_oui_JESUS': all_prc_oui_JESUS,
        'all_rester': all_rester,
        'all_count_homme': all_count_homme,
        'all_count_femme': all_count_femme,
        'all_count_boss': all_count_boss,
    }
    return total


def get_personne_evang_all_by_mois_and_year(mois, annee):
    all_evang = []
    try:
        evangs = Evangelisation.objects.filter(day__month=month_numer(mois), day__year=int(annee))
        evang_mois = month_evang(evangs, month_numer(mois))
        all_evang.append(evang_mois)
    except:
        pass
    return all_evang


def get_personne_evang_all_by_jour_and_mois_and_year(jour, mois, annee):
    all_evang = []
    try:
        evangs = Evangelisation.objects.filter(day__day=jour, day__month=month_numer(mois), day__year=int(annee))
        evang_mois = month_evang(evangs, month_numer(mois))
        all_evang.append(evang_mois)
    except:
        pass
    return all_evang


def get_personne_evang_all_by__year(annee):
    all_evang = []
    liste_mois = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for mois in liste_mois:
        try:
            evangs = Evangelisation.objects.filter(day__month=mois, day__year=annee)
            print('=========evangs', list(evangs))
            evang_mois = month_evang(evangs, mois)
            all_evang.append(evang_mois)
        except:
            evangs = Evangelisation.objects.filter(day__month=mois, day__year=annee)
            evang_mois = month_evang(evangs, mois)
            all_evang.append(evang_mois)
            print('=========evangs******except', list(evangs))
    print('=====get_personne_evang_all_by__year', len(all_evang))
    return all_evang
    


def get_form_set(type_opera, form_nbre):
    form_set = None
    if type_opera=="participants":
        form_set = modelformset_factory(Participant, fields=('nom_et_prenom', 'sexe',), extra=form_nbre, can_delete=True)
    elif type_opera=="personnes":
        form_set = modelformset_factory(Person, form=PersonForm, extra=form_nbre, can_delete=True)
    elif type_opera=="sites":
        form_set = modelformset_factory(Site, fields=('nom_site_evangelisation', 'description',
        'image'), extra=form_nbre, can_delete=True)
    elif type_opera=="évangelisations":
        form_set = modelformset_factory(Evangelisation, fields=(
            'day', 'heure_de_debut', 'heure_de_fin', 
            'site', 'boss', 'observation'), extra=form_nbre, can_delete=True)
    return form_set


def get_form_model(type_opera):
    form_model = None
    if type_opera=="participants":
        form_model = ParticipantForm
    elif type_opera=="personnes":
        form_model = PersonForm
    elif type_opera=="sites":
        form_model = SiteForm
    elif type_opera=="évangelisations":
        form_model = EvangForm
    return form_model


def redirect_by_form_set(type_opera):
    if type_opera=="participants":
        return redirect('evangelisation:evangelisation_app_operations', type_opera)
    elif type_opera=="personnes":
        return redirect('evangelisation:evangelisation_app_operations', type_opera)
    elif type_opera=="sites":
        return redirect('evangelisation:evangelisation_app_operations', type_opera)
    elif type_opera=="évangelisations":
        return redirect('evangelisation:evangelisation_app_operations', type_opera)

def get_model(type_opera):
    if type_opera=="participants":
        return Participant
    elif type_opera=="personnes":
        return Person
    elif type_opera=="sites":
        return Site
    elif type_opera=="évangelisations":
        return Evangelisation

def get_liste_models(type_opera):
    if type_opera=="participants":
        return Participant.objects.all()
    elif type_opera=="personnes":
        return Person.objects.all()
    elif type_opera=="sites":
        return Site.objects.all()
    elif type_opera=="évangelisations":
        return Evangelisation.objects.all()


def get_model(type_opera):
    if type_opera=="participants":
        return Participant
    elif type_opera=="personnes":
        return Person
    elif type_opera=="sites":
        return Site
    elif type_opera=="évangelisations":
        return Evangelisation


def get_liste_models_operations(type_opera, liste):
    models = []
    if type_opera=="participants":
        for i in liste:
            try:
                participant = Participant.objects.get(id=i)
                models.append(participant)
            except Participant.DoesNotExist:
                pass
    elif type_opera=="personnes":
        for i in liste:
            try:
                person = Person.objects.get(id=i)
                models.append(person)
            except Person.DoesNotExist:
                pass
    elif type_opera=="sites":
        for i in liste:
            try:
                site = Site.objects.get(id=i)
                models.append(site)
            except Site.DoesNotExist:
                pass
    elif type_opera=="évangelisations":
        for i in liste:
            try:
                evang = Evangelisation.objects.get(id=i)
                models.append(evang)
            except Evangelisation.DoesNotExist:
                pass
    return models
 
 
def get_liste_models_and_template(request, type_opera):
    models = None
    context = dict()
    if type_opera=="évangelisations":
        models = Evangelisation.objects.all()
        context['type_opera'] = type_opera
        context['models'] = get_liste_models(type_opera)
        context['select_link'] = 'opérations'
        context['select_link_sub'] = 'opérations-evang'
        return render(request, 'pages/liste.html', context)
    elif type_opera=="sites":
        context['type_opera'] = type_opera
        context['models'] = get_liste_models(type_opera)
        context['select_link'] = 'opérations'
        context['select_link_sub'] = 'opérations-site'
        return render(request, 'pages/liste.html', context)
    elif type_opera=="participants":
        context['type_opera'] = type_opera
        context['models'] = get_liste_models(type_opera)
        context['select_link'] = 'opérations'
        context['select_link_sub'] = 'opérations-part'
        return render(request, 'pages/liste.html', context)
    elif type_opera=="personnes":
        models = Person.objects.all()
        pers_oui = Person.objects.filter(accepte_jesus='oui')
        pers_non = Person.objects.filter(accepte_jesus='non')
        pers_deja = Person.objects.filter(accepte_jesus='déjà')
        pers_ras = Person.objects.filter(accepte_jesus='ras')
        pers_whatsapp_oui = Person.objects.filter(whatsapp='oui')
        pers_whatsapp_non = Person.objects.filter(whatsapp='non')

        context['pers_oui'] = pers_oui
        context['pers_non'] = pers_non
        context['pers_deja'] = pers_deja
        context['pers_ras'] = pers_ras
        context['pers_whatsapp_oui'] = pers_whatsapp_oui
        context['pers_whatsapp_non'] = pers_whatsapp_non
        context['type_opera'] = type_opera
        context['models'] = get_liste_models(type_opera)
        context['select_link'] = 'opérations'
        context['select_link_sub'] = 'opérations-pers'
        return render(request, 'pages/liste.html', context)
    return render(request, 'partials/404.html')


def get_stat_evang_person_infos(jour=None, mois=None, year=None, autre=None):
    context = dict()
    if jour==None and mois==None and year:
        models = get_personne_evang_by_year(year)
        context['annee'] = year
    elif jour and mois and year:
        models = get_personne_evang_by_jour_and_mois_and_year(jour, mois, year)
        context['jour'] = jour
        context['mois'] = month_name(mois)
        context['annee'] = year
    elif mois and year and jour==None:
        models = get_personne_evang_by_mois_and_year(mois, year)
        context['mois'] = month_name(mois)
        context['annee'] = year
    else:
        models = get_personne_evang_by_year(autre)

    if models:
        
        pers_oui = [ps for ps in models if ps.accepte_jesus=='oui']
        pers_non = [ps for ps in models if ps.accepte_jesus=='non']
        pers_deja = [ps for ps in models if ps.accepte_jesus=='déjà']
        pers_ras = [ps for ps in models if ps.accepte_jesus=='ras']
        pers_whatsapp_oui = [ps for ps in models if ps.whatsapp=='oui']
        pers_whatsapp_non = [ps for ps in models if ps.whatsapp=='non']

        context['pers_oui'] = pers_oui
        context['pers_non'] = pers_non
        context['pers_deja'] = pers_deja
        context['pers_ras'] = pers_ras
        context['pers_whatsapp_oui'] = pers_whatsapp_oui
        context['pers_whatsapp_non'] = pers_whatsapp_non
        context['models'] = models
    return context






def month_evang(evangs, mois):
    stat_par_mois = []
    evang = None
    prc_oui_JESUS = None
    count_sortie = 0
    count_boss = 0
    count_femme = 0
    count_homme = 0
    oui_JESUS = 0
    liste_evang = []
    rester = 0
    ps_evg = 0
    observ = []


    if len(evangs)!=0:
        count_sortie = evangs.count()
        for evang in evangs:
            count_boss = count_boss + evang.boss.all().count()
            count_femme = count_femme + len([boss.sexe for boss in evang.boss.all() if boss.sexe=='féminin'])
            count_homme = count_homme + len([boss.sexe for boss in evang.boss.all() if boss.sexe=='masculin'])
            oui_JESUS = oui_JESUS +  evang.personnes.filter(accepte_jesus='oui').count()
            rester = rester + len([ps for ps in list(evang.personnes.all()) if ps.suivi.choix_person=='rester'])
            try:
                prc_oui_JESUS = ( (evang.personnes.filter(accepte_jesus='oui').count())/(evang.personnes.all().count()) )*100
                prc_oui_JESUS = float("{:.2f}".format(prc_oui_JESUS))
            except (ZeroDivisionError, Person.DoesNotExist):
                prc_oui_JESUS = 0
            ps_evg = ps_evg + evang.personnes.all().count()
            liste_evang.append(evang)
            observ.append(evang.observation)

    stat_par_mois = {
        'mois_id':int(mois),
        'mois':month_name(int(mois)),
        'count_sortie': count_sortie,
        'count_boss': count_boss,
        'count_femme': count_femme,
        'count_homme': count_homme,
        'oui_JESUS': oui_JESUS,
        'rester': rester,
        'prc_oui_JESUS': prc_oui_JESUS,
        'ps_evg': ps_evg,
        'liste_evang':liste_evang,
        'observations':observ
    }

    print('=====stat_par_mois', stat_par_mois['mois'])

    return stat_par_mois



def get_stat_oui_jesus_by_mois(all_evang):
    #==================================Total==================================================================
    all_oui_JESUS = 0
    liste_oui_by_mois = list()
    for all in all_evang:
        if all['oui_JESUS']!=0:
            all_oui_JESUS = all_oui_JESUS + all['oui_JESUS']
        else:
            all_oui_JESUS = 0
        liste_oui_by_mois.append(all_oui_JESUS)
    return liste_oui_by_mois














































