from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
import datetime
from datetime import date
from io import BytesIO
from django.template.loader import get_template, render_to_string
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
from django.shortcuts import render, redirect
import random


from evangelisation.utils import (get_stat_evang_person_infos, month_name, month_evang, month_numer,
    get_personne_evang_all_by__year, get_personne_evang_all_by_jour_and_mois_and_year, get_personne_evang_all_by_mois_and_year,
    get_personne_evang_by_jour_and_mois_and_year, get_personne_evang_by_mois_and_year, get_personne_evang_by_year,
    get_personne_total, get_stat_oui_jesus_by_mois)
from evangelisation.models import Evangelisation, Person
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@login_required(login_url="user_login")
def generate_pdf(request, orientation, annee=None):
    context = dict()
    all_evang = None
    image_src = os.path.join(BASE_DIR, 'static\images_root')
    context['image_src'] = image_src

    if annee:
        all_evang = get_personne_evang_all_by__year(annee)
        context['annee'] = annee
    else:
        all_evang = get_personne_evang_all_by__year(date.today().year)
        context['annee'] = date.today().year

    if orientation == 'paysage':
        context['orientation'] = 'paysage'
    else:
        context['orientation'] = 'portrait'

    total = get_personne_total(all_evang)
    liste_oui_by_mois = get_stat_oui_jesus_by_mois(all_evang)
    
    context['janvier_oui'] = liste_oui_by_mois[0]
    context['fevrier_oui'] = liste_oui_by_mois[1]
    context['mars_oui'] = liste_oui_by_mois[2]
    context['avril_oui'] = liste_oui_by_mois[3]
    context['mai_oui'] = liste_oui_by_mois[4]
    context['juin_oui'] = liste_oui_by_mois[5]
    context['juillet_oui'] = liste_oui_by_mois[6]
    context['aout_oui'] = liste_oui_by_mois[7]
    context['septembre_oui'] = liste_oui_by_mois[8]
    context['octobre_oui'] = liste_oui_by_mois[9]
    context['novembre_oui'] = liste_oui_by_mois[10]
    context['decembre_oui'] = liste_oui_by_mois[11]
    #===========+++END++++
    context['total'] = total
    context['all_evang'] = all_evang

    random.seed(0)
    report_name = f"rapport-evangelisation{annee}-n°{random.randint(1, 1000)}"
    template_path = 'pages/pdf-report.html'

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={report_name}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('il y\'a certains erreurs <pre>' + html + '</pre>')
    return response


@login_required(login_url="user_login")
def rapport_app_index(request):
    stat = None
    all_evang = []
    total = {}
    context = dict()
    liste_mois = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    if ('jour' and 'mois' and 'annee') in request.GET:
        jour = request.GET['jour']
        mois = request.GET['mois']
        annee = request.GET['annee']
        
        if jour == '----' and mois != '----' and annee != '----':
            context = get_stat_evang_person_infos(mois=month_numer(mois), year=annee)
            all_evang = get_personne_evang_all_by_mois_and_year(mois, annee)
            total = get_personne_total(all_evang)
            context['total'] = total
            context['all_evang'] = all_evang
        elif jour != '----' and mois != '----' and annee != '----':
            context = get_stat_evang_person_infos(jour=jour, mois=month_numer(mois), year=annee)
            all_evang = get_personne_evang_all_by_jour_and_mois_and_year(jour, mois, annee)
            total = get_personne_total(all_evang)
            context['total'] = total
            context['all_evang'] = all_evang
        elif jour == '----' and mois == '----' and annee != '----':
            context = get_stat_evang_person_infos(year=annee)
            all_evang = get_personne_evang_all_by__year(annee)
            total = get_personne_total(all_evang)
            liste_oui_by_mois = get_stat_oui_jesus_by_mois(all_evang)
            context['janvier_oui'] = liste_oui_by_mois[0]
            context['fevrier_oui'] = liste_oui_by_mois[1]
            context['mars_oui'] = liste_oui_by_mois[2]
            context['avril_oui'] = liste_oui_by_mois[3]
            context['mai_oui'] = liste_oui_by_mois[4]
            context['juin_oui'] = liste_oui_by_mois[5]
            context['juillet_oui'] = liste_oui_by_mois[6]
            context['aout_oui'] = liste_oui_by_mois[7]
            context['septembre_oui'] = liste_oui_by_mois[8]
            context['octobre_oui'] = liste_oui_by_mois[9]
            context['novembre_oui'] = liste_oui_by_mois[10]
            context['decembre_oui'] = liste_oui_by_mois[11]
            context['total'] = total
            context['all_evang'] = all_evang
        elif jour == '----' and mois == '----' and annee == '----':
            try:
                context = get_stat_evang_person_infos(jour='----', mois='----', year='----')
                if context:
                    print(context)
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
        elif jour != '----' and mois == '----' and annee == '----':
            try:
                context = get_stat_evang_person_infos(jour=jour, mois=mois, year=annee)
                if context:
                    print(context)
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
        elif jour != '----' and mois != '----' and annee == '----':
            print("=========annee=====",'errorrrrrrrrrrr3333')
            try:
                context = get_stat_evang_person_infos(jour=jour, mois=mois, year=annee)
                if context:
                    print(context)
                else:
                    context['error'] = True
                    context['jour'] = jour
            except ValueError:
                context['error'] = True
                print("=========anneeexceptexcept=====",'errorrrrrrrrrrr3333')
        elif jour == '----' and mois != '----' and annee == '----':
            print("=========annee=====",'errorrrrrrrrrrr2222')
            try:
                context = get_stat_evang_person_infos(jour='----', mois=month_numer(mois), year='----')
                if context:
                    print(context)
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
                print("=========annee except except=====",'errorrrrrrrrrrr2222')
        elif jour != '----' and mois == '----' and annee != '----':
            print("=========annee=====",'errorrrrrrrrrrr44444')
            try:
                context = get_stat_evang_person_infos(jour='----', mois=month_numer(mois), year='----')
                if context:
                    print(context)
                else:
                    context['error'] = True
            except ValueError:
                context['error'] = True
                print("=========annee except except=====",'errorrrrrrrrrrr44444')
    else:
        context = get_stat_evang_person_infos(autre=date.today().year)
        if context:
            pass
        else: 
            context['not_stat'] = True
        all_evang = get_personne_evang_all_by__year(date.today().year)
        print('===========////all_evang', len(all_evang))
        total = get_personne_total(all_evang)
        liste_oui_by_mois = get_stat_oui_jesus_by_mois(all_evang)
        
        context['janvier_oui'] = liste_oui_by_mois[0]
        context['fevrier_oui'] = liste_oui_by_mois[1]
        context['mars_oui'] = liste_oui_by_mois[2]
        context['avril_oui'] = liste_oui_by_mois[3]
        context['mai_oui'] = liste_oui_by_mois[4]
        context['juin_oui'] = liste_oui_by_mois[5]
        context['juillet_oui'] = liste_oui_by_mois[6]
        context['aout_oui'] = liste_oui_by_mois[7]
        context['septembre_oui'] = liste_oui_by_mois[8]
        context['octobre_oui'] = liste_oui_by_mois[9]
        context['novembre_oui'] = liste_oui_by_mois[10]
        context['decembre_oui'] = liste_oui_by_mois[11]
        #===========+++END++++
        context['total'] = total
        context['annee'] = date.today().year
        context['all'] = True
        context['all_evang'] = all_evang
    context['select_link'] = 'rapport'
    return render(request, 'pages/rapport/index.html', context)



@login_required(login_url="user_login")
def rapport_app_detail(request, pk):
    data = dict()
    context = dict()

    evangs_mois = Evangelisation.objects.filter(day__month=pk)
    html_table = render_to_string('pages/rapport/modal-rapport-detail.html', {
        'evangs_mois': evangs_mois,
    })
    
    data['html_table'] = html_table
    print('===== evangs_mois', evangs_mois)

    return JsonResponse(data, safe=False)





















