from django import forms

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	
class SignUpForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	password_again = forms.CharField(widget=forms.PasswordInput())
	
	def clean_password_again(self):
		password_again = self.cleaned_data['password_again']
		password = self.cleaned_data['password']
		if password != password_again:
			raise forms. ValidationError("Passwords Must Match Exactly.")
		return password_again
		
class SearchForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	
class RSVPForm(forms.Form):
	confirmed = forms.BooleanField()
