from django import forms
from .models import *

class AdminDataForm(forms.ModelForm):
	class Meta:
		model = AdminData
		fields = '__all__'