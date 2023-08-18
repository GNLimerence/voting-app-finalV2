from django import forms
from .models import Poll
class CreatePoll (forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('question_text','op_one','op_two','op_three','op_four',)
        label = {
            'question_text': '',
            'op_one': '',
            'op_two': '',
            'op_three': '',
            'op_four': '',
        }