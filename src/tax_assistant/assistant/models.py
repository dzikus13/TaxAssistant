from django.db import models

from django.utils.translation import gettext as _
# Create your models here.

SESSION_STATUS = {
    "ongoing": _("Ongoing"),
    "finished": _("Finished"),
    "aborted": _("Aborted"),
}

class Session(models.Model):
    user_id = models.UUIDField()
    topic = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20,
                               choices=[(k, v) for k, v in SESSION_STATUS.items()],
                               default="ongoing")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def collect_knowledge(self):
        dataset = {}
        for item in self.interaction_set.all():
            for field in item.response_json.get("declaration_info", []):
                dataset.update(field)
        return dataset


class Interaction(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_input = models.CharField(max_length=1024)
    response = models.TextField(null=True)
    response_json = models.JSONField(null=True)
