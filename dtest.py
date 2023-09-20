import os


# print('hi',os.listdir('uploads'))
# for song in os.listdir('uploads'):
#     print(song, os.path.join(os.path.abspath(song))
for x in os.walk('uploads'):
    print(x)