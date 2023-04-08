from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class CeleryForm(forms.Form):
    email = forms.EmailField(label="Email",
                             help_text='Enter your email',
                             required=True)
    notification_text = forms.CharField(label="Notification",
                                        help_text='Enter text',
                                        required=True)
    date_time = forms.DateTimeField(label='Date and time',
                                    help_text='Enter the time for notification YYYY-MM-DD HH:MM:SS',
                                    required=True,
                                    input_formats=['%Y-%m-%d %H:%M:%S'])

    def clean_date_time(self):
        now = timezone.now()
        plus_two_days = now + timedelta(days=2)
        time = self.cleaned_data['date_time']
        if time < now or time > plus_two_days:
            raise ValidationError('Date should not be in past or more than two days ahead')
        return time
