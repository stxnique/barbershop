from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Номер телефона',
            'pattern': '[0-9+]+',
            'title': 'Только цифры, может начинаться с +'
        })
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Сохраняем телефон в дополнительное поле (нужно расширить модель)
        if commit:
            user.save()
            # Создаем профиль с телефоном
            Profile.objects.create(user=user, phone=self.cleaned_data['phone'])
        return user