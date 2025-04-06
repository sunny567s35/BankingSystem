from django import forms
from app.models import Announcements

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = ['title', 'message', 'is_active']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


# forms.py
from django import forms
from app.models import Ticket

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'admin_notes', 'resolution']
        widgets = {
            'admin_notes': forms.Textarea(attrs={'rows': 3}),
            'resolution': forms.Textarea(attrs={'rows': 3}),
        }