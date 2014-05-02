from django.db import models
import json

class DataSet(models.Model):
    title = models.CharField(max_length=100)
    current_revision = models.ForeignKey('DataSetRevision', null=True, blank=True, related_name='dataset_current_revision')
    created = models.DateTimeField(auto_now_add=True)
    newest_revision = models.ForeignKey('DataSetRevision', null=True, blank=True, related_name='dataset_newest_revision')
    revisions = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return self.title

class DataSetRevision(models.Model):
    dataset = models.ForeignKey('DataSet')
    data = models.TextField()
    column_names = models.TextField()
    revision_number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=20)
    comment = models.CharField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.dataset.title + ' revision ' + str(self.revision_number)

    def save(self, *args, **kwargs):
        super(DataSetRevision, self).save(*args, **kwargs)
        # Update num_revisions and newest_revision on DataSet.
        revisions = DataSetRevision.objects.filter(dataset=self.dataset)
        num_revisions = revisions.count()
        latest_revision = revisions.order_by('-created')[0]
        self.dataset.revisions = num_revisions
        self.dataset.newest_revision = latest_revision
        self.dataset.save()
