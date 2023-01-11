from django import forms


from mgcapp.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'document', 'prediction', 'prediction_text', 'recommender')