from django import forms


class TimeForm(forms.Form):

    time_frame = forms.IntegerField(label="Number of Minutes", min_value=5, max_value=1000)