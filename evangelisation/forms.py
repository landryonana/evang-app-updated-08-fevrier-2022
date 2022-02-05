from django import forms

from evangelisation.models import Evangelisation, Person, Site, Participant





#==================================================================================
#===========================Evangelisation form
class EvangForm(forms.ModelForm):   
    class Meta:
        model = Evangelisation
        fields = ['day', 'heure_de_debut', 'heure_de_fin', 'site', 'boss', 'observation']
    
    def clean_boss(self):
      return self.cleaned_data['boss']

    
    def clean(self):
        cleaned_data = super().clean()
        heure_de_debut = cleaned_data.get("heure_de_debut")
        heure_de_fin = cleaned_data.get("heure_de_fin")
        site = cleaned_data.get("site")

        msg1 = f"Veuillez sélectionner un site"
        if site is None:
            self.add_error('site', msg1)

        debut_minites = heure_de_debut.hour*60 + heure_de_debut.minute
        fin_minites = heure_de_fin.hour*60 + heure_de_fin.minute
        msg = "Heure de début doit etre inférieur ou égal à Heure de fin"
        if debut_minites>fin_minites:
            self.add_error('heure_de_debut', msg)
        


#==================================================================================
#===========================Participant form
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['nom_et_prenom', 'sexe']

    def clean_nom_et_prenom(self):
        nom_et_prenom = self.cleaned_data['nom_et_prenom']
        if len(str(nom_et_prenom))<3:
            raise forms.ValidationError("Problème lors du remplissage du nom et prenom d'un participant : Le champ doit avoir au moins 03 caractères ")
        return nom_et_prenom



#====================================================================================
#===========================Person form
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [ 'nom_et_prenom','evangelisation', 'accepte_jesus',
                'sexe', 'whatsapp', 'contacts', 'quartier_d_habitation',
                'boss', 'sujets_de_priere', 'temoignages'
            ]

    def clean_boss(self):
        return self.cleaned_data['boss']
    
    def clean(self):
        cleaned_data = super().clean()
        nom_prenom = cleaned_data.get("nom_et_prenom")
        accepte_jesus = cleaned_data.get("accepte_jesus")
        sexe = cleaned_data.get("sexe")

        msg2 = f"Veuillez sélectionner un site"

        msg1 = "Merci de renseigner ce champ"
        if accepte_jesus=="---------":
            self.add_error('accepte_jesus', msg1)
        if nom_prenom==None:
            self.add_error('nom_et_prenom', msg1)
        if sexe=="---------":
            self.add_error('accepte_jesus', msg1)

        msg = "Ce champ doit avoir au moins 03 caractères"
        if nom_prenom!=None and len(nom_prenom)<=2:
            self.add_error('nom_et_prenom', msg)
    
    def clean_contacts(self):
        contact = self.cleaned_data['contacts']
        
        if len(str(contact))!=9 and contact!=None:
            raise forms.ValidationError("Le numéro de télephone est invalide")
        else:
            if len(str(contact))==9:
                contact_6 = str(contact)[0]
                print(contact_6)
                if int(contact_6)!=6:
                    raise forms.ValidationError("Le numéro de télephone doit commencer par 6")

        return contact
    
    def clean_date(self):
        evangelisation = self.cleaned_data.get("evangelisation")
        date = self.cleaned_data.get("date")
        date = evangelisation.day
        return date



#====================================================================================
#===========================Person form Update
class PersonFormUpdate(forms.ModelForm):
    contacts = forms.IntegerField(label="Contact", help_text="Le numéro de téléphone doit avoir 09 chiffres")
    nom_et_prenom = forms.CharField(label="Nom et prenom", help_text="ce champ doit avoir au moins trois caractères")
    quartier_d_habitation = forms.CharField(label="Quartier d'habitation", help_text="ce champ doit avoir au moins trois caractères")
    class Meta:
        model = Person
        fields = [ 'nom_et_prenom','evangelisation', 'accepte_jesus',
                    'sexe', 'whatsapp', 'contacts', 'quartier_d_habitation',
                    'boss', 'sujets_de_priere', 'temoignages']

    def clean_boss(self):
        return self.cleaned_data['boss']
    
    def clean(self):
        cleaned_data = super().clean()
        nom_prenom = cleaned_data.get("nom_et_prenom")
        accepte_jesus = cleaned_data.get("accepte_jesus")
        sexe = cleaned_data.get("sexe")

        msg1 = "Merci de renseigner ce champ"
        if accepte_jesus=="---------":
            self.add_error('accepte_jesus', msg1)
        if nom_prenom==None:
            self.add_error('nom_et_prenom', msg1)
        if sexe=="---------":
            self.add_error('accepte_jesus', msg1)

        msg = "Ce champ doit avoir au moins 03 caractères"
        if nom_prenom!=None and len(nom_prenom)<=2:
            self.add_error('nom_et_prenom', msg)
    
    def clean_contacts(self):
        contact = self.cleaned_data['contacts']
        
        if len(str(contact))!=9 and contact!=None:
            raise forms.ValidationError("Le numéro de télephone est invalide")
        else:
            if len(str(contact))==9:
                contact_6 = str(contact)[0]
                print(contact_6)
                if int(contact_6)!=6:
                    raise forms.ValidationError("Le numéro de télephone doit commencer par 6")

        return contact
    
    def clean_date(self):
        evangelisation = self.cleaned_data.get("evangelisation")
        date = self.cleaned_data.get("date")
        date = evangelisation.day
        return date


#====================================================================================
#===========================Site form
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['nom_site_evangelisation', 'image']
    
    def clean_nom_site_evangelisation(self):
        nom_site = self.cleaned_data['nom_site_evangelisation']
        if len(str(nom_site))<3:
            raise forms.ValidationError("La valeur doit avoir au moins 03 caractères ")
        return nom_site


class FormNbre(forms.Form):
    field = forms.IntegerField(label="Entrez le nombre de formulaire que vous voulez", help_text="le nombre de formulaire sera crée")




















































