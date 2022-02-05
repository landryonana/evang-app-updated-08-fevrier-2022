from fileinput import filename
from random import random
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.contrib import messages
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from evangelisation.utils import (get_form_set, get_liste_models_and_template, 
                                redirect_by_form_set, get_liste_models, get_model,
                                get_liste_models_operations, get_model, get_form_model
                                )
from evangelisation.forms import ParticipantForm, FormNbre, EvangForm
from evangelisation.models import Participant, Evangelisation, Site, Person, Suivi, Profile


import datetime

import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@login_required(login_url="user_login")
def evangelisation_app_index(request, annee=None):
    context = dict()
    evang_first = None
    evangs = None
    annees = list()
    annee = None

    
    year = int(datetime.date.today().year)
    for i in [0, 1, 2]:
        annees.append(year-i)

    evangs = Evangelisation.objects.all()
    if 'liste-evang' in request.GET:
        evang_first = Evangelisation.objects.get(id=int(request.GET['liste-evang']))
    else:
        evang_first = evangs.first()

    
    context['evang_first'] = evang_first
    context['evangs'] = evangs
    #context['annees'] = annees
    #context['anne_select'] = annee
    context['select_link'] = 'evangelisation'
    return render(request, 'index.html', context)



@login_required(login_url="user_login")
def evangelisation_app_multi_form_type_operation(request, type_opera, form_nbre):
    form_errors = None
    context = dict()
    model_set = None
    form_set = None

    model_set = get_form_set(type_opera, form_nbre)
    if request.method=='POST':
       form_set = model_set(request.POST)
       if form_set.is_valid():
            if type_opera=='personnes':
                forms = form_set.save(commit=False)
                if forms != []:
                    for instance in forms:
                        instance.save()
                        Suivi.objects.create(person=instance)
                    form_set.save_m2m()
                    messages.success(request, f'Vous avez ajouté {len(form_set)} {type_opera}')
                    return redirect_by_form_set(type_opera)
                else:
                    form_errors = form_set.errors
            else:
                form_set.save()
                messages.success(request, f'Vous avez ajouté {len(form_set)} {type_opera}')
                return redirect_by_form_set(type_opera)
       else:
           form_errors = form_set.errors
    else:
        model = get_model(type_opera)
        form_set = model_set(queryset=model.objects.none())
        
    context = {
        'form_set': form_set,
        'multi': True,
        'form_nbre': int(form_nbre),
        'type_opera': type_opera,
        'form': FormNbre(),
        'form_p': ParticipantForm(),
        'form_errors': form_errors,
    }
    context['select_link'] = 'opérations'

    if type_opera == 'personnes':    
        context['select_link_sub'] = 'opérations-pers'
    elif type_opera == 'sites':
        context['select_link_sub'] = 'opérations-site'
    elif type_opera == 'participants':
        context['select_link_sub'] = 'opérations-part'
    elif type_opera == 'évangelisations':
        context['select_link_sub'] = 'opérations-evang'
    
    return render(request, 'pages/form.html', context)



@login_required(login_url="user_login")
def evangelisation_app_form_nbre(request, type_opera):
    context = dict()
    if request.method=='POST':
        form = FormNbre(request.POST)
        if form.is_valid():
            form_nbre = request.POST['field']
            return redirect('evangelisation:evangelisation_app_multi_form_type_operation', type_opera, form_nbre)
    else:
        form = FormNbre()
    context = {
        'form': form,
        'type_opera': type_opera,
        'select_link': 'evangelisation'
    }
    context['select_link'] = 'opérations'
    if type_opera == 'personnes':    
        context['select_link_sub'] = 'opérations-pers'
    elif type_opera == 'sites':
        context['select_link_sub'] = 'opérations-site'
    elif type_opera == 'participants':
        context['select_link_sub'] = 'opérations-part'
    elif type_opera == 'évangelisations':
        context['select_link_sub'] = 'opérations-evang'
    
    return render(request, 'pages/form.html', context)


@login_required(login_url="user_login")
def evangelisation_app_operations(request, type_opera):
    return get_liste_models_and_template(request, type_opera)


@login_required(login_url="user_login")
def evangelisation_app_operations_recherche(request, type_opera):
    data = dict()
    models = None
    counter = None
    models_template = None
    if type_opera=="personnes":
        if request.GET.get('name') == 'query':
            value = request.GET.get('value')
            models = Person.objects.filter(
                Q(nom_et_prenom__contains=str(value)) 
                | Q(contacts__contains=str(value))
                | Q(quartier_d_habitation__contains=str(value))
                | Q(temoignages__contains=str(value))
                | Q(sujets_de_priere__contains=str(value))
            )
            models_template = render_to_string(
                'pages/personne/table_personne.html', 
                {'models':models}, 
                request=request
            )
        else:
            models = Person.objects.all()
            models_template = render_to_string(
                'pages/personne/table_personne.html', 
                {'models':models}, 
                request=request
            )
    elif type_opera=="participants":
        if request.GET.get('name') == 'query':
            value = request.GET.get('value')
            models = Participant.objects.filter(
                Q(nom_et_prenom__contains=str(value)) 
            )
            models_template = render_to_string(
                'pages/participant/table_participant.html', 
                {'models':models}, 
                request=request
            )
        else:
            models = Participant.objects.all()
            models_template = render_to_string(
                'pages/participant/table_participant.html', 
                {'models':models}, 
                request=request
            )
    elif type_opera=="sites":
        if request.GET.get('name') == 'query':
            value = request.GET.get('value')
            models = Site.objects.filter(
                Q(nom_site_evangelisation__contains=str(value)) 
            )
            models_template = render_to_string(
                'pages/site/table_site.html', 
                {'models':models}, 
                request=request
            )
        else:
            models = Site.objects.all()
            models_template = render_to_string(
                'pages/site/table_site.html', 
                {'models':models}, 
                request=request
            )
    elif type_opera=="évangelisations":
        if request.GET.get('name') == 'query':
            value = request.GET.get('value')
            models = Evangelisation.objects.filter(
                Q(day__contains=str(value)) 
                |Q(site__nom_site_evangelisation__contains=str(value)) 
            )
            models_template = render_to_string(
                'pages/evangelisation/table_evangelisation.html', 
                {'models':models}, 
                request=request
            )
        else:
            models = Evangelisation.objects.all()
            models_template = render_to_string(
                'pages/evangelisation/table_evangelisation.html', 
                {'models':models}, 
                request=request
            )


    if len(models) > 1:
            counter_str = f"{len(models)} resultats"
    else:
        counter_str = f"{len(models)} resultat"
        counter = len(models)
        data['counter'] = counter

    data['counter_str'] = counter_str
    data['models'] = models_template
    return  JsonResponse(data, safe=False)



@login_required(login_url="user_login")
def evangelisation_app_operations_models_supprimer(request, type_opera):
    context = dict()
    if 'selected_action' in request.POST:
        liste = request.POST.getlist('selected_action')
        if request.POST['objects'] == 'supprimer':
            context['models'] = get_liste_models_operations(type_opera, liste)
            context['type_opera'] = type_opera
            return render(request, 'pages/supprimer.html', context)
    else:
        return redirect('evangelisation:evangelisation_app_operations', type_opera)


@login_required(login_url="user_login")
def evangelisation_app_operations_supprimer(request, type_opera):
    if 'user_selected' in request.POST:
        liste = request.POST.getlist('user_selected')
        Model = get_model(type_opera)
        for id in liste:
            try:
                model = Model.objects.get(id=id)
                model.delete()
            except model.DoesNotExist:
                pass
        messages.error(request, f'Vous avez supprimer {len(liste)} {type_opera}')
        return redirect('evangelisation:evangelisation_app_operations', type_opera)
    else:
        return redirect('evangelisation:evangelisation_app_operations', type_opera)


def evangelisation_app_operations_models_modifier(request, type_opera):
    return 



@login_required(login_url="user_login")
def evangelisation_app_operations_modifier(request, type_opera, id):
    model = None
    model = get_model(type_opera)
    instance_model = None
    context = dict()
    form_model = None
    form_model = get_form_model(type_opera)

    try:
        instance_model = model.objects.get(id=id)
        if request.method=='POST':
            form_model = form_model(instance=instance_model, data=request.POST)
            if form_model.is_valid():
                form_model.save()
                messages.success(request, 'modification réussie')
                return redirect('evangelisation:evangelisation_app_operations', type_opera)
        else:
            form_model = form_model(instance=instance_model)
        context['form'] = form_model
        context['instance_model'] = instance_model
        context['type_opera'] = type_opera
        return render(request, "pages/modifier.html", context)
    except model.DoesNotExist:
        return redirect('evangelisation:evangelisation_app_operations', type_opera)
    

@login_required(login_url="user_login")
def evangelisation_app_operations_ajax(request, type_opera, form_nbre):
    form = None
    data = dict()
    if request.method=='POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('evangelisation_app_multi_form_type_operation', type_opera, form_nbre)
    else:
        form = ParticipantForm()
    data['form'] = form
    return JsonResponse(data=data, safe=True)

















