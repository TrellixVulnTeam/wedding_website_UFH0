from django.shortcuts import render
from wedding_website.forms import SearchForm, RSVPForm
from django.http import HttpResponse
from wedding_database.models import Invitee, Group
from django.forms import formset_factory

	
def base(request):
	return render(request, 'base.html')
	
def home(request):
	return render(request, 'home.html')
	
def about(request):
	return render(request, 'about.html')
	
def wedding_info(request):
	return render(request, 'weddinginfo.html')

def rsvp(request):
	if request.method == 'POST':
		if 'search' in request.POST:
			form = SearchForm(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data['first_name']
				last_name = form.cleaned_data['last_name']
				try:
					group = Invitee.objects.get(first_name__icontains = str(first_name), last_name__icontains = str(last_name))
					coming = Group.objects.get(group_name = group.group)
					form.fields['first_name'].initial = first_name
					form.fields['last_name'].initial = last_name
					invitees = coming.invitee_set.all()
				except:
					try:
						list1 = []
						group = Invitee.objects.filter(first_name__icontains = str(first_name), last_name__icontains = str(last_name))
						for person in group:
							list1.append(str(person.group))
						form.fields['first_name'].initial = first_name
						form.fields['last_name'].initial = last_name
						if len(list1) > 0:
							return render(request, 'rsvp.html', {'form' : form, 'group_list': list1, 'first_name': first_name, 'last_name': last_name})
					except:
						pass
					try:
						list1 = []
						try:
							first_group = Invitee.objects.filter(first_name__icontains = str(first_name))
							for person in first_group:
								list1.append(str(person.first_name) + " " + str(person.last_name))
						except:
							pass
						try:
							last_group = Invitee.objects.filter(last_name__icontains = str(last_name))
							for person in last_group:
								list1.append(str(person.first_name) + " " + str(person.last_name))
						except:
							pass
						form.fields['first_name'].initial = first_name
						form.fields['last_name'].initial = last_name
						if len(list1) > 0:
							return render(request, 'rsvp.html', {'form' : form, 'first_last_list': list1, 'first_name': first_name, 'last_name': last_name})
						else:
							from django.forms.utils import ErrorList
							form.add_error('first_name', u"No records were found with that first and last name.")
							return render(request, 'rsvp.html', {'form': form})
					except:
						from django.forms.utils import ErrorList
						form.add_error('first_name', u"No records were found with that first and last name.")
						return render(request, 'rsvp.html', {'form': form})
				return render(request, 'rsvp.html', {'form' : form, 'group_name' : coming.group_name, 'num_coming' : coming.num_coming, 'num_invited' : coming.num_invited, 'invitees' : invitees})
			
			else:
				form = SearchForm()
				return render(request, 'rsvp.html', {'form' : form})
		elif 'Choose Group' in request.POST:
			form = SearchForm(request.POST)
			request_list = []
			for item in request.POST:
				request_list.append(item)
			group_selected = request.POST.get('radio')
			#if len(group_selected) != 1:
			#	return HttpResponse(request_list)
			coming = Group.objects.get(group_name = group_selected)
			form.fields['first_name'].initial = request.POST.get('first_name')
			form.fields['last_name'].initial = request.POST.get('last_name')
			invitees = coming.invitee_set.all()
			return render(request, 'rsvp.html', {'form' : form, 'group_name' : coming.group_name, 'num_coming' : coming.num_coming, 'num_invited' : coming.num_invited, 'invitees' : invitees})
		elif 'Choose Name' in request.POST:
			form = SearchForm(request.POST)
			first_name = request.POST.get('radio').split(' ')[0]
			last_name = request.POST.get('radio').split(' ')[1]
			group = Invitee.objects.get(first_name__icontains = first_name, last_name__icontains = last_name)
			coming = Group.objects.get(group_name = group.group)
			form.fields['first_name'].initial = request.POST.get('first_name')
			form.fields['last_name'].initial = request.POST.get('last_name')
			invitees = coming.invitee_set.all()
			return render(request, 'rsvp.html', {'form' : form, 'group_name' : coming.group_name, 'num_coming' : coming.num_coming, 'num_invited' : coming.num_invited, 'invitees' : invitees})
		else:
			confirmed_list = list(request.POST.getlist('checkbox'))
			group_name = request.POST.get('group_name')
			group = Group.objects.get(group_name = group_name)
			group.confirmed = True
			group.num_coming = len(confirmed_list)
			group.save()
			for person in confirmed_list:
				person_list = person.split()
				invitee = Invitee.objects.get(first_name__iexact = person_list[0], last_name__iexact = person_list[1], group__group_name = group_name)
				invitee.confirmed = True
				invitee.save()
				
			#print str(confirmed_list) + " " + str(group_name) + "length of list: " + str(len(list(confirmed_list)))
			return render(request, 'weddinginfo.html', {'rsvp' : True})
	else:
		form = SearchForm()
	return render(request, 'rsvp.html', {'form' : form})
	
	
def rsvp_thanks(request):
	return render(request, 'rsvp-thanks.html')

	

	
def registry(request):
	return render(request, 'registry.html')
	
def contact(request):
	return render(request, 'contact.html')
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	