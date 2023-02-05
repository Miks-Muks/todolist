from django.forms import ModelForm


class ToDoForm(ModelForm):
    class Meta:
        fields = [
            'title',
            'memo',
            'important',
        ]