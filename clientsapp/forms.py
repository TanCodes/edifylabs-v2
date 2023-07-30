"""
>>  FORM TO BE DISPLAYED ON CLIENT DASHBOARD TO SAVE CLIENT DETIALS FROM BACKEND 
"""
from django import forms
from .models import Clients
from django.core.validators import RegexValidator
class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput
                                 (attrs={'placeholder': 'e.g: tanmay '}))

    last_name = forms.CharField(widget=forms.TextInput
                                (attrs={'placeholder': 'e.g:  barvi'}))
    company_name = forms.CharField(widget=forms.TextInput
                                   (attrs={'placeholder': 'e.g:  EdifyLabs'}))
    address = forms.CharField(widget=forms.TextInput
                              (attrs={'placeholder': 'e.g:  xyz ,Maharashtra , India '}))
    contact = forms.CharField(max_length=13, validators=[
        RegexValidator(
            regex=r'^[0-9]+$',
            message='Phone number should contain only numbers',
        ),
    ], widget=forms.TextInput
                              (attrs={'placeholder': 'e.g:  +91************'}))
    
    date_of_birth = forms.DateField(widget=DateInput)
    email_id = forms.EmailField(widget=forms.EmailInput
                                (attrs={'placeholder': 'e.g: xyz@gmail.com'}))

    class Meta:
        model = Clients
        fields = ('first_name', 'last_name', 'gender',
                  'company_name', 'email_id', 'contact', 'date_of_birth', 'address', 'coaching_type_course')

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['rows'] = 1
        self.fields['address'].widget.attrs['columns'] = 1

        self.fields['first_name'].label = ""
        self.fields['last_name'].label = ""
        self.fields['gender'].label = ""
        self.fields['company_name'].label = ""
        self.fields['email_id'].label = ""
        self.fields['contact'].label = ""
        self.fields['date_of_birth'].label = ""
        self.fields['address'].label = ""
        self.fields['coaching_type_course'].label = ""

        self.fields['company_name'].required = False
        self.fields['gender'].required = False
        self.fields['coaching_type_course'].required = True
        self.fields['coaching_type_course'].empty_label = "Select type of coaching"

    def clean_sessions(self):
        dt_obj_one = self.cleaned_data['sessions']
        dt_str = dt_obj_one.strftime('%Y-%m-%d %H:%M')
        return dt_str

    def clean_sessions_end(self):
        dt_obj_two = self.cleaned_data['sessions_end']
        dt_str_end = dt_obj_two.strftime('%Y-%m-%d %H:%M')
        return dt_str_end
