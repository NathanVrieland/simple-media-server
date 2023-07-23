import os

# put this file in a directory with files that have a common label (spotifydown.com - <song name>)
# replace LABEL with the common label to be removed
# run the file

LABEL = "spotifydown.com - "

dir_list = os.listdir()

for i in dir_list:
    if LABEL in i:
        os.rename(i, i.replace(LABEL, ""))
