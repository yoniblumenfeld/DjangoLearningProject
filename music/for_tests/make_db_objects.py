from music.models import Album,Song
from music.views import get_object_fields_list

def createArbitraryObject(Model):
    arbitrary = Model()
    fields = get_object_fields_list(arbitrary)
    res =""
    for field in fields:
        res+= str(type(field))+"<br>"
    return HttpResponse(res)

createArbitraryObject(Album)

