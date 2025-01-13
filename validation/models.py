from django.db import models
from user.models import User

class Validation(models.Model):
    validation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')  # Changed to user for clarity
    validation_report = models.FileField(upload_to='validationReports/', null=True)  # FileField to download the validation report
    valid = models.BooleanField(default=False)  # True if validated, False if not
    validation_result = models.JSONField(null=True, blank=True)  # Store validation result as JSON
    valid_invoice = models.FileField(upload_to='uploadInvoices/', null=True) # FileField to download the invoice

    def __str__(self):
        return self.validation_report.name if self.validation_report else 'No file to be downloaded'