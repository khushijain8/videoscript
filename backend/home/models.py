from django.db import models

class Script(models.Model):
    prompt = models.CharField(max_length=255)
    content = models.TextField()
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt
