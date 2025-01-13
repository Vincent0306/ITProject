from django.db import models
from user.models import User


class InputData(models.Model):
    input_data_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    input_content = models.FileField(upload_to='uploadFiles/') #save input file in a new folder and save link in this place.

    def __str__(self):
        return self.input_content.name if self.input_content else 'No file uploaded'
