from django.db import models
# Create your models here.
from apps.accounts.models import User


class TeacherCsvModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    csv_file=models.FileField(upload_to='media/csv_file')
    uploaded=models.DateTimeField(auto_now_add=True)
    activated=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username