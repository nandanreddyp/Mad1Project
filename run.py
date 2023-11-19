from Musica import app
from Musica.database.models import *
from Musica.functions import create_upload_folders, create_admin

# run flask on local host
if __name__ == "__main__":
    create_upload_folders()
    db.create_all()
    admin = User.query.get('admin@musica')
    if not admin : create_admin()
    app.run(debug=True)

# # run falsk on local network
# if __name__ == "__main__":
#     db.create_all()
#     app.run(host='192.168.1.2',port='5000',debug=True)