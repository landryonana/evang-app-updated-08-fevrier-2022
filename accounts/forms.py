from django import forms
from django.contrib.auth.models import User


from evangelisation.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", min_length=3)
    password = forms.CharField(label="Mot de passe",widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur", 
        help_text="Obligatoire. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.")
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput, 
        help_text=f"<li>Votre mot de passe doit contenir au moins 8 caractères</li>\
                    <li>Votre mot de passe doit etre alphanuméric</li>\
                    <li>Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.</li>\
                    <li>Votre mot de passe ne peut pas être entièrement numérique.</li>\
                    <li>Votre mot de passe ne peut pas être un mot de passe couramment utilisé.</li>")
    password2 = forms.CharField(label='Repeter le mot de passe', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Nom et Prenom', help_text="ce champ est optionnel")
    class Meta:
        model=User
        fields = ('username', 'first_name','email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Un utilisateur avec cet email exist déjà')
        return email

    def clean_first_name(self):
        cd = self.cleaned_data
        if len(cd['first_name']) <3:
            raise forms.ValidationError('ce champ doit avoir au moins 03 caractères!!!')
        return cd['first_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('les deux valeurs ne sont pas identique !!!')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label='Nom et Prenom', help_text="ce champ est optionnel")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'is_superuser')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        msg = "Ce champ doit avoir au moins 03 caractères"
        if len(first_name)<3:
            self.add_error('first_name', msg)



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'sexe', 'image']
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone))!=9:
            raise forms.ValidationError("Le numéro de télephone est invalide")
        else:
            if len(str(phone))==9:
                phone_6 = str(phone)[0]
                if int(phone_6)!=6:
                    raise forms.ValidationError("Le numéro de télephone doit commencer par 6")
        return phone