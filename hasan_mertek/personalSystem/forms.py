from django import forms
from adminSytem.models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['requested_days', 'reason']
        widgets = {
            'requested_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, personal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.personal = personal
        total_days = personal.annual_leave_days + (personal.annual_leave_hours / 10)
        self.fields['requested_days'].label = 'Talep Edilen İzin Süresi (Gün)'  # Türkçe Etiket
        self.fields['reason'].label = 'Sebep'
        self.fields['requested_days'].widget.attrs['max'] = int(total_days)
        self.fields['requested_days'].widget.attrs['min'] = 1

    def clean_requested_days(self):
        requested_days = self.cleaned_data['requested_days']
        total_days = self.personal.annual_leave_days + (self.personal.annual_leave_hours / 10)
        
        if requested_days > total_days:
            raise forms.ValidationError(f'En fazla {int(total_days)} gün izin talep edebilirsiniz.')
        
        return requested_days 
    
    