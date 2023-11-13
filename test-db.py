from Musica import app, db
from Musica.database.models import *

# db.create_all()

# users = [User(id='user@',password='1234',f_name='user'),
#         User(id='user0@',password='1234',f_name='user0')]

# songs = [Song(title='song',duration='01:00',user_id='user@'),
#          Song(title='song0',duration='01:00',user_id='user0@'),
#          Song(title='song1',duration='01:00',user_id='user@'),
#          Song(title='song2',duration='01:00',user_id='user0@')]

# albumsNplaylists = [Album(title='album',user_id='user@'),
#           Album(title='album0',user_id='user0@'),
#           Playlist(title='playlist',user_id='user@'),
#           Playlist(title='playlist0',user_id='user0@')]

# album = Album.query.get(1)
# album.songs.append(Song.query.get(3))
# # db.session.add()
# # db.session.delete(Song.query.get(2))
# db.session.commit()

# songs = [(x.id,x.title) for x in Song.query.all()]
# albums = [x.songs for x in Album.query.all()]
# # playlists = [x.songs for x in Playlist.query.all()]
# print('songs',songs,'\n','albums',albums,'\n')

user = session.query(User).get('new@gmail.com')
print(user.library.__dict__)