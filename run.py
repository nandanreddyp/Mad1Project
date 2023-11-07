from Musica import app
from Musica.database.models import *

#local pc
if __name__ == "__main__":
    app.run(debug=True)

# #local network
# if __name__ == "__main__":
#     db.create_all()
#     app.run(host='192.168.1.2',port='5000',debug=True)