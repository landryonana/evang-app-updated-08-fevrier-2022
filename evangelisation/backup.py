
from evangelisation.models import Participant, Evangelisation, Site, Person, Suivi, Profile




    #=========================================================================================
    #===========================BACKUP TEST===========================================
    data = dict()
    data['evangelisations'] = list(Evangelisation.objects.values()) 
    data['sites'] = list(Site.objects.values()) 
    data['participants'] = list(Participant.objects.values()) 
    data['users'] = list(User.objects.values())
    data['profiles'] = list(Profile.objects.values())
    data['personnes'] = list(Person.objects.values())
    data['suivi'] = list(Suivi.objects.values())

    data_dumps = json.dumps(data, indent=4, sort_keys=True, default=str)
    with open('other.json', 'w') as jsonfile:
        jsonfile.write(data_dumps)

    with open('other.json', 'r') as f:
        data = json.load(f)
        try:
            for obj in data['sites']:
                Site.objects.create(
                    id=obj['id'],
                    nom_site_evangelisation=obj['nom_site_evangelisation'],
                    created=obj['created'],
                    updated=obj['updated'],
                    author_id=obj['author_id'],
                    description=obj['description'],
                    image=obj['image'],
                )
                print('====================sites', obj)

            for obj in data['participants']:
                print('====================participants', obj, '\n')

            for obj in data['evangelisations']:
                print('====================evangelisations', obj , '\n')

            for obj in data['personnes']:
                print('====================personnes', obj, '\n')
        except Exception as e:
            raise e
    #==================================END TEST================================================
    #==================================================================================
