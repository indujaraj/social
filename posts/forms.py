from django import forms

from .models import Post, Comment, MessageModel


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 4, 'column': 4, 'placeholder': "Say something..."}))

    class Meta:
        model = Post
        fields = ('content', 'image')


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('comment',)
        widget = {
            'text': forms.TextInput(attrs={
                'id': 'post-text',
                'required': True,
                'placeholder': 'Say something...'
            }),
        }


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)


    class Meta:
        model = MessageModel
        fields = ['body']
