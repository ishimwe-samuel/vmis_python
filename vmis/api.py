import rest_framework
from rest_framework.generics import get_object_or_404
from .serializers import VaccineStockSerializer, VaccinesSerializer
from .models import VaccineStock, Vaccine
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
# vaccine list viewset


class VaccineListViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VaccinesSerializer


class VaccineStockViewSet(viewsets.ModelViewSet):
    queryset = VaccineStock.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VaccineStockSerializer

    def get_queryset(self):
        queryset = VaccineStock.objects.filter(
            orgunitid=self.request.user.orgunitid)
        return queryset

    def create(self, request, *args, **kwargs):
        vaccine=get_object_or_404(Vaccine,vaccine_uuid=request.data['vaccine'])
        batch_number=request.data['batch_number']
        expiration_date=request.data['expiration_date']
        quantity=request.data['quantity']
        dose_per_vial=request.data['dose_per_vial']
        vvm_status=request.data['vvm_status']
        orgunitid=request.data['orgunitid']
        orgunitname=request.data['orgunitname']
        obj,created=VaccineStock.objects.update_or_create(orgunitid=orgunitid,batch_number=batch_number,
            defaults={
            'vaccine':vaccine,
            'batch_number':batch_number,
            'expiration_date':expiration_date,
            'quantity':quantity,
            'dose_per_vial':dose_per_vial,
            'vvm_status':vvm_status,
            'orgunitid':orgunitid,
            'orgunitname':orgunitname,
            })
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if created:
            return Response(serializer.validated_data,status=HTTP_201_CREATED)
        else:
            return Response(serializer.validated_data,status=HTTP_200_OK)

        

