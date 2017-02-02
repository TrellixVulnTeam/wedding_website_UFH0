from django.db import models

class Group(models.Model):
	group_name = models.CharField(max_length = 30)
	num_invited = models.IntegerField()
	confirmed = models.BooleanField(default = False)
	num_coming = models.IntegerField()
	
	def __str__(self):
		return self.group_name

class Invitee(models.Model):
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
	group = models.ForeignKey(Group)
	confirmed = models.BooleanField(default = False)
	
	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)
		

