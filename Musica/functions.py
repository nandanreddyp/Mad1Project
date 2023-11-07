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

def save_file(type, id, file):
    import os; cwd = os.getcwd();
    if type=='image/album':
        file_extension = os.path.splitext(file.filename)[1]
        image_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','images','album_covers',image_name)
        file.save(file_path)
    elif type=='image/profile':
        file_extension = os.path.splitext(file.filename)[1]
        image_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','images','profile_covers',image_name)
        file.save(file_path)
    elif type=='image/song':
        file_extension = os.path.splitext(file.filename)[1]
        image_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','images','song_covers',image_name)
        file.save(file_path)
    elif type=='lyrics':
        file_path = os.path.join(cwd,'Musica','static','uploads','lyrics',str(id)+'.txt')
        file_to_write = open(file_path, 'w')
        file_to_write.write(file)
        file_to_write.close()
    elif type=='song':
        file_extension = os.path.splitext(file.filename)[1]
        song_name = str(id)+file_extension
        file_path = os.path.join(cwd,'Musica','static','uploads','songs',song_name)
        file.save(file_path)
    return 