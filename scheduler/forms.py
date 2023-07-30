from django import forms
from .models import ScheduleClients


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ScheduleForm(forms.ModelForm):

    sessions = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    # sessions_end = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    my_time_field = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = ScheduleClients
        fields = ('first_name_S', 'last_name_S', 'coaching_type_course',
                  'review_call', 'sessions' , 'my_time_field')

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)

        self.fields['first_name_S'].label = ""
        self.fields['last_name_S'].label = ""
        self.fields['coaching_type_course'].label = ""
        self.fields['review_call'].label = ""
        self.fields['sessions'].label = ""
        self.fields['my_time_field'].label = ""

        self.fields['coaching_type_course'].empty_label = "Select type of coaching"

    def clean_sessions(self):
        dt_obj_one = self.cleaned_data['sessions']
        dt_str = dt_obj_one.strftime('%Y-%m-%d %H:%M')
        return dt_str

    # def clean_sessions_end(self):
    #     dt_obj_two = self.cleaned_data['my_time_field']
    #     dt_str_end = dt_obj_two.strftime('%Y-%m-%d %H:%M')
    #     return dt_str_end
    def clean_sessions_end(self):
        dt_obj = self.cleaned_data['my_time_field']
        dt_str_end = dt_obj.strftime('%H:%M')
        return dt_str_end
