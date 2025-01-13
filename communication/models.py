from django.db import models
from user.models import User
from ubl.models import Ubl
from validation.models import Validation

class Communication(models.Model):
    communication_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", default=1)
    validation_id = models.ForeignKey(Validation, on_delete=models.CASCADE, db_column="validation_id", default=1)
    ubl_id = models.ForeignKey(Ubl, on_delete=models.CASCADE, db_column="ubl_id", default=1)

    def __str__(self):
        return self.communication_report.name if self.communication_report else 'No file uploaded'
 