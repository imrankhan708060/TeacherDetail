from django.forms import ModelForm
from . models import TeacherCsvModel

class TeacherCsvModelForm(ModelForm):

    class Meta:
        model=TeacherCsvModel
        fields=('csv_file',)