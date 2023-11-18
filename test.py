from Musica.functions import get_linked_list

from Musica.database.models import Album

album = Album.query.first()

head = get_linked_list(album.songs, shuffle=True)

while head:
    print(head.song.title)
    head = head.next


print( 6 in range(6))