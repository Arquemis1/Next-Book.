from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 

class CustomUserCreationForm(UserCreationForm):
    # Aquí puedes añadir campos adicionales si tuvieras más información que pedir al usuario
    # Por ejemplo, un campo para la biografía:
    # bio = forms.CharField(label='Biografía', max_length=200, widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # Agrega el campo de email

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email