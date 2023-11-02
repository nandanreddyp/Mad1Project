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

