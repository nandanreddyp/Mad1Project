from Musica import app
from Musica.database.models import *

for x in Song.query.all():
    print(x.__dict__)

# song = Song(title='butto dj',artist='unknown')
# db.session.add(song)
# db.session.commit()