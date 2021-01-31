from rest_framework import  serializers
from .models import VaccineStock, Vaccine


class VaccinesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vaccine
        fields = ('url','vaccine_uuid', 'vaccine_shortname', 'vaccine_name', 'description')


class VaccineStockSerializer(serializers.HyperlinkedModelSerializer):
    vaccine=serializers.SerializerMethodField()
    class Meta:
        model = VaccineStock
        fields = ('url', 'vaccine','vaccine_id','batch_number', 'expiration_date',
                  'quantity', 'dose_per_vial', 'vvm_status', 'orgunitid', 'orgunitname')
    def get_vaccine(self,obj):
        return str(obj.vaccine.vaccine_shortname)

