from rest_framework import serializers
from backend.models import Awards

DEPARTMENT =(
    ('1','CSE'),
    ('2','ECE'),
    ('3','EEE'),
    ('4','MECH'),
    ('5','CIVIL')
)

class AwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Awards
        #fields = ['id','facultyid','facultyname','awardname','awarddescription','awardedby']
        fields = '__all__'
