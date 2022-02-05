from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages


from evangelisation.models import Profile
from history.models import History










#================================================================
#==========================================SAVE USER==================
def save_form_user(request, form, template_name, obj=None, action=None):
    data = dict()
    context = dict()
    elmt=None
    if request.method == 'POST':
        if form.is_valid():
            if action=='ajout_user':
                #no save form directely
                new_user = form.save(commit=False)
                #set password
                new_user.set_password(form.cleaned_data['password'])
                #save user or create new user
                new_user.save()
                #create new History of new user
                History.objects.create(
                    user=request.user,
                    content_object=f"COMPTE:::Utilisateur: {new_user}",
                    action_type="ajout de"
                )
                #create new Profile of new user
                Profile.objects.create(user=new_user)
                #create new History of new Profile
                History.objects.create(
                    user=request.user,
                    content_object=f"COMPTE:::Utilisateur:: profile a: {new_user}",
                    action_type="ajout de"
                )
                messages.success(request, f"Vous avez ajouté <b>{new_user}</b> avec success")
                return redirect('user_comptes')
            elif action=='modifie_user':
                pass
    else:
        #==this is an instance of user for updated
        if elmt is not None:
            context['elmt'] = obj
        

    context['form'] = form
    context['compte'] = True
    data['html_form'] = render_to_string(
        template_name, 
        context, 
        request=request
    )
    return JsonResponse(data, safe=True)


#================================================================
#==========================================SAVE==================
def save_form(request, form, template_name, obj=None):
    data = dict()
    context = dict()
    elmt=None
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    if elmt is not None:
        context['elmt'] = obj
    context['form'] = form
    data['html_form'] = render_to_string(
        template_name, 
        context, 
        request=request
    )
    return JsonResponse(data)
