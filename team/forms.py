from django.forms import ModelForm
from .models import OpponentScoresUserUpated

class UserUpdateGameForm(ModelForm):

    class Meta:
        model = OpponentScoresUserUpated
        exclude = ['update_time', 'update_user', 'game']