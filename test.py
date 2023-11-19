from Musica.functions import get_linked_list, create_upload_folders

from Musica.database.models import User, db, Blacklist

# admin = User.query.get('admin@musica')
# db.session.add(admin); db.session.commit()

for item in Blacklist.query.all():
    print(item.__dict__)