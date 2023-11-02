from Musica import app
from Musica.database.models import *

##local pc
# if __name__ == "__main__":
#     app.run(debug=True)

#local network
if __name__ == "__main__":
    app.run(host='192.168.1.7',port='5000',debug=True)