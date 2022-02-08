from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.text import slugify



#override username(max_length, help_text), email(_unique) and password(max_length, help_text)
User._meta.get_field('username').validators[1].limit_value = 150
User._meta.get_field('email')._unique = True
User._meta.get_field('username').help_text = 'Obligatoire. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.'
User._meta.get_field('password').help_text = 'Il doit contenir au moins 8 caractères.<br> Ne doit pas etre courant.<br> doit etre alphanuméric'



#==========site d'évengélisation
class Site(models.Model):
    status = (
        ('oui', 'Oui'),
        ('non', 'Non')
    )
    nom_site_evangelisation = models.CharField(max_length=200, 
                        verbose_name="site d'évangélisation",
                        help_text="le nom du site doit avoir au moins 03 caractères",
                        unique=True,
                        error_messages={'unique':"Un site avec ce nom existe déjà"})
    description = models.TextField(null=True, blank=True, verbose_name="Description", help_text="ajouter une description du site")
    image = models.ImageField(upload_to='images/site/%Y/%m/%d/', null=True, blank=True, help_text="ajouter une image")
    author = models.ForeignKey(User, related_name='sites', 
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name="ajouter par ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site d'évangélisation"
    

    def __str__(self):
        return self.nom_site_evangelisation


#==========Participants à l'évangelisation
class Participant(models.Model):
    SEXE = (
        ('masculin', 'Masculin'),
        ('féminin', 'Féminin')
    )
    nom_et_prenom = models.CharField(max_length=200, unique=True, error_messages={'unique':"Un participant avec ce nom et\ou prénom existe déjà"})
    sexe = models.CharField(choices=SEXE, max_length=15, verbose_name='Sexe')
    author = models.ForeignKey(User, related_name='participants', 
                                on_delete=models.SET_NULL, 
                                blank=True,  
                                null=True,
                                verbose_name="créer par ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom_et_prenom



#==========évengélisations
class Evangelisation(models.Model): 
    status = (
        ('oui', 'Oui'),
        ('non', 'Non')
    )
    day = models.DateField(verbose_name="Jour d'évangélisation", 
            default=timezone.now, unique=True, 
            error_messages={'unique':"ce moment d'évangelisation existe déjà"})
    heure_de_debut = models.TimeField(default=timezone.now, verbose_name="Heure de début")
    heure_de_fin = models.TimeField(default=timezone.now, verbose_name="Heure de fin")
    site = models.ForeignKey(Site, related_name="evangelisations", verbose_name="Lieu d'évangelisation", 
                            on_delete=models.SET_NULL, blank=True,  null=True)
    author = models.ForeignKey(User, related_name='evangs', on_delete=models.SET_NULL, 
                                blank=True, null=True, verbose_name="créer par ")
    boss = models.ManyToManyField(Participant, related_name='participations', 
                                blank=True, verbose_name="Qui sont présents ?")
    observation = models.TextField(verbose_name="Observations", null=True, blank=True)


    def __str__(self):
        if self.day.month >=10:
            return f"Évangelisation du {self.day.day}/{self.day.month}/{self.day.year}"
        else:
            return f"Évangelisation du {self.day.day}/0{self.day.month}/{self.day.year}"

    def dure(self):
        rest = None
        debut_minites = self.heure_de_debut.hour*60 + self.heure_de_debut.minute
        fin_minites = self.heure_de_fin.hour*60 + self.heure_de_fin.minute
        if debut_minites<=fin_minites:
            heure = (fin_minites - debut_minites)//60
            mini = (fin_minites - debut_minites)%60
            if 0<=heure<=9:
                if 0<=mini<=9:
                    rest = f"0{int(heure)}:0{mini}"
                else:
                    rest = f"0{int(heure)}:{mini}"
            else:
                if 0<=mini<=9:
                    rest = f"{int(heure)}:0{mini}"
                rest = f"{heure}:{mini}"
        else:
            return f"calcule impossible"
        return rest


#==========Personne évangelisé
class Person(models.Model):
    ACCEPTE_JESUS = (
        ('oui', 'Oui'),
        ('non', 'Non'),
        ('ras', 'Indécis'),
        ('déjà', 'Déjà')
    )
    SEXE = (
        ('masculin', 'Masculin'),
        ('féminin', 'Féminin')
    )
    WHATSAPP = (
        ('oui', 'Oui'),
        ('non', 'Non'),
    )
    author = models.ForeignKey(User, related_name='auth_personnes',
                                            on_delete=models.SET_NULL, 
                                            blank=True,  
                                            null=True,
                                            verbose_name="Enrgistré par ")
    evangelisation = models.ForeignKey(Evangelisation, related_name='personnes',
                                            on_delete=models.SET_NULL, 
                                            blank=True,
                                            null=True,
                                            verbose_name="Moment d'évangelisation")
    date = models.DateField(auto_now_add=True)
    nom_et_prenom = models.CharField(max_length=200,
        verbose_name='Nom et Prénom', 
        unique=True,
        null=False,
        help_text="ce champ doit avoir au moins trois caractères",
        error_messages={'unique':"Une personne avec ce nom existe déjà"})
    contacts = models.PositiveIntegerField(
                verbose_name="Numéro de téléphone",
                blank=True,  
                null=True,
                unique=True,
                help_text="Le numéro de téléphone doit avoir 09 chiffres",
                error_messages={'unique':"Le numéro de télephone existe déjà"}
        )
    quartier_d_habitation = models.CharField(
        max_length=200, 
        verbose_name="Quartier d'habitation", 
        help_text="ce champ doit avoir au moins trois caractères",
        blank=True,  
        null=True,
        default="---"
    )
    accepte_jesus = models.CharField(choices=ACCEPTE_JESUS, max_length=15, verbose_name='Accepté JÉSUS')
    sexe = models.CharField(choices=SEXE, max_length=15, verbose_name='Sexe')
    whatsapp = models.CharField(choices=WHATSAPP, max_length=15, verbose_name='Whatsapp', blank=True,  null=True)
    boss = models.ManyToManyField(Participant, related_name='personnes', 
                        verbose_name="Qui l'ont évangelisé ?",
                        help_text="selectionner les personnes ayant évangelisés cette personne", blank=True)
    sujets_de_priere = models.TextField(verbose_name="Prière et observation", null=True, blank=True, help_text="ce champ est optionnel")
    temoignages = models.TextField(verbose_name="Témoignage", null=True, blank=True, help_text="ce champ est optionnel")
    created = models.DateTimeField(auto_now_add=True, verbose_name='créer à')
    updated = models.DateTimeField(auto_now=True, verbose_name='mis à jour à')

    class Meta:
        verbose_name = "Personne évangélisé"
        ordering = ('-nom_et_prenom',)


    def __str__(self):
        return self.nom_et_prenom


#==========Suivie par Personne évangelisé
class Suivi(models.Model):
    choix = (
        ('---', '---'),
        ('rester', 'Rester'),
        ('passager', 'Passager'),
        ('indécis', 'Indécis')
    )
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="suivi",
                                    blank=True,  null=True, verbose_name='Personne')
    nbre_appel = models.PositiveIntegerField(default=0, verbose_name="Nombre d'appel")
    nbre_visite_au_culte = models.PositiveIntegerField(default=0,
                                                        verbose_name="Nombre de visite")
    nbre_invitation_au_culte = models.PositiveIntegerField(default=0, verbose_name="Nombre d'invitation au culte")
    nbre_presence_total_au_culte = models.PositiveIntegerField(default=0, verbose_name="Nombre de présence éffective au culte")
    choix_person = models.CharField(max_length=25, choices=choix, default=0, verbose_name="Choix de la personne")
    boos_suivi = models.TextField(verbose_name='Boss ayant éffectuer le suivi')
    author = models.ForeignKey(User, related_name='suivis', 
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name="ajouter par ")
    sujets_de_priere_suivi = models.TextField(verbose_name="Sujet de prière", null=True, blank=True, help_text="ce champ est optionnel")
    temoignages_suivi = models.TextField(verbose_name="Témoignage", null=True, blank=True, help_text="ce champ est optionnel")
    observation_suivi = models.TextField(verbose_name="Observation", null=True, blank=True, help_text="ce champ est optionnel")
    

    def __str__(self):
        return f"suivi de {self.person}"


#==========Profile utilisateur
class Profile(models.Model):
    SEXE = (
        ('masculin', 'Masculin'),
        ('féminin', 'Féminin')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,  null=True)
    image = models.ImageField(upload_to='images/profile/%Y/', null=True, blank=True, help_text="ajouter une photo")
    phone = models.PositiveIntegerField(null=True, unique=True, blank=True, 
        help_text="le numéro de télephone doit avoir 9 chiffres",
        error_messages={'unique':"Une boss avec ce numéro de télephone existe déjà"})
    sexe = models.CharField(choices=SEXE, max_length=15, verbose_name='Sexe')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile de {self.user}"

 
#==========Image de l'évangelisation
class Image(models.Model):
    titre = models.CharField(max_length=250, verbose_name='Titre', error_messages={'unique':"Une image avec ce titre existe déjà"})
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    image = models.ImageField(upload_to='images/gallerie/%Y/%m/%d/', blank=True, null=False)
    author = models.ForeignKey(User, related_name='images', 
                                on_delete=models.DO_NOTHING,
                                blank=True,
                                verbose_name="créer par ")
    evangelisation = models.ForeignKey(Evangelisation, related_name='images', 
                                        on_delete=models.DO_NOTHING, 
                                        blank=True, verbose_name="Évangelsation du ")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Publier le ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"image de {self.evangelisation} publier le {self.publish}"
