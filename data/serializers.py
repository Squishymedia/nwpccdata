from models import DataSet, DataSetRevision
from rest_framework import serializers
import json

class ShortDataSetRevisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSetRevision
        fields = ('revision_number', 'created', 'user', 'comment')

class DataSetRevisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSetRevision
        fields = ('dataset', 'revision_number', 'created', 'user', 'comment', 'column_names', 'data')

class DataSetSerializer(serializers.ModelSerializer):
    revisions = ShortDataSetRevisionSerializer(source='datasetrevision_set', many=True)

    class Meta:
        model = DataSet
        fields = ('id', 'title', 'current_revision', 'created', 'revisions')

class ShortDataSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ('id', 'title', 'current_revision', 'created', 'revisions')
