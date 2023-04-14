from django.db import models


class Email(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    from_address = models.EmailField()
    to_address = models.EmailField()
    cc_address = models.EmailField(blank=True)
    bcc_address = models.EmailField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} ({self.to_address}) at {self.sent_at}'
