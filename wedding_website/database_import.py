import csv 
import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wedding_website.settings")
django.setup()

from wedding_database.models import Invitee, Group

Group.objects.all().delete()
Invitee.objects.all().delete()
         
path = os.path.abspath(os.path.dirname(sys.argv[0])) 

f = open(path + '\\wedding_database\\RSVP Database Info.csv', 'r')
reader = list(csv.reader(f))
for x in range(1, len(reader)):
	if reader[x][4] != '':
		group_data = Group(group_name = reader[x][4].rstrip(), num_invited = reader[x][5], confirmed = False, num_coming = -1)
		group_data.save()
		print(x)

for x in range(1, len(reader)):
	print(x)
	invitee_group = Group.objects.get(group_name = reader[x][2].rstrip())
	invite_data = Invitee(first_name = reader[x][0].rstrip(), last_name = reader[x][1].rstrip(), group = invitee_group)
	invite_data.save()
	
print(Group.objects.all())
print(Invitee.objects.all())