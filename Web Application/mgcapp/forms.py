
# GenRec - The Smash Group
    # Music Genre Recommender and Classifier
    # Project during Data Science 2
    # WiSe 2022/2023
    # TU Darmstadt

# File forms.py
    # Description: 
        # Definitions for Django Database-Admin Page 


from django import forms


from mgcapp.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'document', 'prediction', 'prediction_text', 'recommender')