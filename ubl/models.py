from django.db import models
from user.models import User


class Ubl(models.Model):
    ubl_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    ubl_xml = models.FileField(upload_to='generatedUbls/') #save generated ubl files

    def __str__(self):
        return self.ubl_xml.name if self.ubl_xml else 'No file to be downloaded'




