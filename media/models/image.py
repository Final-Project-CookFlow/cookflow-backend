from django.db import models

class Image(models.Model):
    class ImageType(models.TextChoices):
        USER = 'USER', 'User'
        RECIPE = 'RECIPE', 'Recipe'
        STEP = 'STEP', 'Step'
    class ImageStatus(models.TextChoices):
        UPLOADED = 'UPLOADED', 'Uploaded'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=15,
        choices=ImageType.choices
    )
    url = models.CharField(max_length=100)
    processing_status = models.CharField(
        max_length=15,
        choices=ImageStatus.choices,
        default=ImageStatus.UPLOADED
    )
    external_id = models.BigIntegerField(null=True, blank=True) # <--- MODIFIED THIS LINE
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'images'
    
    def __str__(self):
        return self.name