# create admin
def create_admin():
    from Musica.database.models import db, User, Library
    user = db.session.get(User, 'admin@musica')
    if not user:
        user = User(id='admin@musica',password=hash('12345678'),f_name='Admin',l_name='',role='admin')
        db.session.add(user); db.session.add(Library(user_id=user.id)); db.session.commit()
        print('admin created')
    return ''

# password hashing
def hash(password):
    import bcrypt
    password = password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)
def password_check(hashed, input):
    import bcrypt
    input = input.encode('utf-8')
    return bcrypt.checkpw(input, hashed)

# audio length calculator
def mp3_duration_cal(file_loc):
    from mutagen.mp3 import MP3
    audio = MP3(file_loc)
    audio_length = int(audio.info.length)
    print(audio_length)
    hours = audio_length//3600
    audio_length %= 3600
    mins = audio_length//60
    audio_length %= 60
    secs = audio_length
    return f'{mins:02}:{secs:02}'

# save files in static/uploads
def create_upload_folders():
    import os; cwd = os.getcwd()
    required_folders = [os.path.join(cwd,'Musica','static','uploads'),
                        os.path.join(cwd,'Musica','static','uploads','images'),
                        os.path.join(cwd,'Musica','static','uploads','images','album_covers'),
                        os.path.join(cwd,'Musica','static','uploads','images','profile_covers'),
                        os.path.join(cwd,'Musica','static','uploads','images','song_covers'),
                        os.path.join(cwd,'Musica','static','uploads','lyrics'),
                        os.path.join(cwd,'Musica','static','uploads','songs')]
    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    return ''


def save_file(type, id, file):
    import os; cwd = os.getcwd();
    if type=='image/album':
        file_extension = os.path.splitext(file.filename)[-1]
        image_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','images','album_covers',image_name)
        file.save(file_path)
        return image_name
    elif type=='image/profile':
        file_extension = os.path.splitext(file.filename)[-1]
        image_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','images','profile_covers',image_name)
        file.save(file_path)
        return image_name
    elif type=='image/song':
        file_extension = os.path.splitext(file.filename)[-1]
        image_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','images','song_covers',image_name)
        file.save(file_path)
        return image_name
    elif type=='lyrics':
        file_path = os.path.join(cwd,'Musica','static','uploads','lyrics',str(id)+'.txt')
        file_to_write = open(file_path, 'w', encoding="utf-8", newline='')
        file_to_write.write(file)
        file_to_write.close()
        return str(id)+'.txt'
    elif type=='song':
        file_extension = os.path.splitext(file.filename)[-1]
        song_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','songs',song_name)
        file.save(file_path)
        return song_name
    return 'error, not saved file'

def remove_file(type,file_name):
    import os; cwd = os.getcwd();
    if type=='image/album':
        try:
            file_path = os.path.join(cwd,'Musica','static','uploads','images','album_covers',file_name)
            os.remove(file_path)
        except FileNotFoundError:
            pass
    elif type=='image/profile':
        try:
            file_path = os.path.join(cwd,'Musica','static','uploads','images','profile_covers',file_name)
            os.remove(file_path)
        except FileNotFoundError:
            pass
    elif type=='image/song':
        try:
            file_path = os.path.join(cwd,'Musica','static','uploads','images','song_covers',file_name); 
            os.remove(file_path)
        except FileNotFoundError:
            pass
    elif type=='lyrics':
        try:
            file_path = os.path.join(cwd,'Musica','static','uploads','lyrics',file_name)
            os.remove(file_path)
        except FileNotFoundError:
            pass
    elif type=='song':
        try:
            file_path = os.path.join(cwd,'Musica','static','uploads','songs',file_name)
            os.remove(file_path)
        except FileNotFoundError:
            pass
    return 

def get_lyrics(file_name):
    import os; cwd = os.getcwd();
    file_path = os.path.join(cwd,'Musica','static','uploads','lyrics',file_name)
    lines = ('').join(open(file_path,'r',encoding='utf-8').readlines())
    return lines

def get_song(file_name):
    import os; cwd = os.getcwd();
    file_path = os.path.join(cwd,'Musica','static','uploads','songs',file_name)
    return file_path

# user liked or not?
def has_user_liked(current_user, song):
    from Musica.database.models import Rating
    rating = Rating.query.filter_by(user_id=current_user.id,song_id=song.id).first()
    return rating is not None

# update ratings
def update_rating(song):
    from Musica.database.models import db
    ratings = len(song.ratings)
    plays = len(song.plays)
    song.rating = round((ratings/plays)*100,2)
    db.session.commit()
    return ''

# update view count
def update_play_count(song):
    from Musica.database.models import db
    song.play_count = len(song.plays)
    db.session.commit()
    return ''

# linked list for album and palylist

def get_linked_list(lst):
    class Node:
        def __init__(self,value):
            self.song = value; self.next = None; self.prev = None
    if not lst: return None
    head = Node(lst[0])
    current_node = head
    for i in range(1,len(lst)):
        next_node = Node(lst[i])
        current_node.next = next_node
        next_node.prev = current_node
        current_node = current_node.next
    return head

