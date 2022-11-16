import string
import random
import os
from distutils.dir_util import copy_tree

# Create new User folders
new_user_count = 255

for i in range(0, new_user_count):
	usr_name = 'ucmc2020ss' + format(i, '03d')
	usr_folder = 'volume/userdata/' + usr_name
	if not os.path.exists('uvolume/serdata/' + usr_name):
		os.makedirs('volume/userdata/' + usr_name)
	copy_tree('volume/userdata/ucmc2020ssRoot', 'userdata/' + usr_name)

os.system('chmod 777 -R volume/userdata')








