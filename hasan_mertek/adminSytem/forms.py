from django import forms
from personalSystem.models import Personal, LeaveUsage
from adminSytem.models import Personal  # Personal modelini import etmelisiniz


class AssignLeaveForm(forms.ModelForm):
    personal = forms.ModelChoiceField(
        queryset=Personal.objects.all(),
        label='Personel',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    days = forms.IntegerField(
        min_value=1,
        label='İzin Süresi (Gün)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    leave_type = forms.ChoiceField(
        choices=LeaveUsage.LEAVE_TYPES,  # Bu, LeaveUsage modelinizde tanımlı olmalı.
        label='İzin Türü',  
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Açıklama', 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False  # Eğer açıklama zorunlu değilse
    )

    class Meta:
        model = LeaveUsage
        fields = ['personal', 'leave_type', 'description', 'days']
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 
class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['name', 'surname', 'email', 'position', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
           
        }
        labels = {
            'name': 'Ad',
            'surname': 'Soyad',
            'email': 'E-posta',
            'position': 'Pozisyon',
            'phone': 'Telefon',
        }