from django import forms

from MovieListViewer.models import Request


class RequestMetaForm(forms.ModelForm):
    def save(self, user, commit=True):
        # get the instance so we can add the user to it.
        instance = super(RequestMetaForm, self).save(commit=False)
        instance.user = user

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance
class RequestForm(RequestMetaForm):
    class Meta:
        model = Request
        fields = ['name', 'year']