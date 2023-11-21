from Musica.functions import get_linked_list, create_upload_folders

from Musica.database.models import User, db

user = db.session.get(User,'userkk0@musica')
print(user)