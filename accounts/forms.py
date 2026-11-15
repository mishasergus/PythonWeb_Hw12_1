from django.contrib.auth.forms import UserCreationForm
from Shared_models.models import CustomUser, UserRole

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        default_role, created = UserRole.objects.get_or_create(name='user')
        user.role = default_role

        if commit:
            user.save()
        return user