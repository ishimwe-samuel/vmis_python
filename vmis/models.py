from django.db import models
from django.db.models import UniqueConstraint
import uuid
pcv_status = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
)
dose_per_vial = (
    (2, 2),
    (4, 4),
    (10, 10),
    (20, 20),
)


class Vaccine(models.Model):
    vaccine_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    vaccine_shortname = models.CharField(max_length=50)
    vaccine_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.vaccine_shortname


class VaccineStock(models.Model):
    vaccinestock_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    vaccine = models.OneToOneField(
        "Vaccine", verbose_name="vaccine", on_delete=models.CASCADE)
    batch_number = models.CharField(
        max_length=100)
    expiration_date = models.DateField(auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    dose_per_vial = models.IntegerField(choices=dose_per_vial)
    vvm_status = models.IntegerField(choices=pcv_status)
    orgunitid = models.CharField(
        max_length=50, unique=True, verbose_name="organisation unit id")
    orgunitname = models.CharField(
        max_length=100, verbose_name='organisation unit name')
    stock_creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.orgunitname


class Request(models.Model):
    request_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    source_orgunit_id = models.CharField(
        verbose_name="Source orgunit id", max_length=50)
    source_orgunit_name = models.CharField(
        verbose_name="Source orgunit name", max_length=100)
    destination_orgunit_id = models.CharField(
        verbose_name="Destination orgunit id", max_length=50)
    destination_orgunit_name = models.CharField(
        verbose_name="Destination orgunit name", max_length=100)

    def __str__(self):
        return self.source_orgunit_name


class RequestVaccine(models.Model):
    request_vaccine_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.SET_NULL, null=True)
    quantity_requested = models.BigIntegerField()
    person_vaccinated = models.IntegerField()


class Distribution(models.Model):
    distribution_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    distribution_orgunit_id = models.CharField(
        verbose_name="distribution orgunit source id", max_length=50)
    distribution_orgunit_name = models.CharField(
        verbose_name="distribution orgunit source name", max_length=100)
    request_orgunit_id = models.CharField(
        verbose_name="distribution orgunit source id", max_length=50)
    request_orgunit_name = models.CharField(
        verbose_name="distribution orgunit source name", max_length=100)

    def __str__(self):
        return self.distribution_orgunit_name


class DistributionVaccine(models.Model):
    distribution_vaccine = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.SET_NULL, null=True)
    quantity_requested = models.IntegerField()
    quantity_supplied = models.IntegerField()
    acknowledged = models.BooleanField(default=False)


class Acknowledge(models.Model):
    acknowledge_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    from_orgunit = models.CharField(max_length=70)
    from_orgunit_name = models.CharField(max_length=100)
    to_orgunit = models.CharField(max_length=70)
    to_orgunit_name = models.CharField(max_length=100)
    acknowledgement_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.from_orgunit_name


class AcknowledgeVaccine(models.Model):
    acknowledge_vaccine_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    acknowledge = models.ForeignKey(Acknowledge, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.SET_NULL, null=True)
    vaccine_quantity = models.IntegerField()
    expiration_date = models.DateField(auto_now=False, auto_now_add=False)
    pcv_status = models.IntegerField(choices=pcv_status)
    comment = models.TextField(blank=True, null=True)


class Wastage(models.Model):
    wastage_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    source_orgunitid = models.CharField(max_length=50)
    source_orgunitiname = models.CharField(max_length=100)
    destination_orgunitid = models.CharField(max_length=50)
    destination_orgunitiname = models.CharField(max_length=100)
    wastage_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.source_orgunitiname


class WastageVaccine(models.Model):
    wastage_vaccine_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    wastage = models.ForeignKey(Wastage, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.SET_NULL, null=True)
    batch_number = models.CharField(max_length=100)
    damagetype = models.CharField(max_length=50)
    quantity = models.IntegerField()
    expiration_date = models.DateField(auto_now=False, auto_now_add=False)
    comment = models.TextField(blank=True, null=True)


class Dispense(models.Model):
    dispense_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    orgunitid = models.CharField(max_length=50)
    orgunitname = models.CharField(max_length=100)
    dispense_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.orgunitname


class DispenseVaccine(models.Model):
    dispense_vaccine_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    dispense = models.ForeignKey(Dispense, on_delete=models.CASCADE)
    vaccines = models.ForeignKey(
        Vaccine, on_delete=models.SET_NULL, null=True)
    person_vaccinated = models.IntegerField()
    dispense_quantity = models.IntegerField()
    batch_number = models.CharField(max_length=100)


class Return(models.Model):
    return_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    source_orgunitid = models.CharField(max_length=50)
    source_orgunitiname = models.CharField(max_length=100)
    destination_orgunitid = models.CharField(max_length=50)
    destination_orgunitiname = models.CharField(max_length=100)
    return_date = models.DateField(auto_now_add=True)


class ReturnVaccine(models.Model):
    return_vaccine_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    returns = models.ForeignKey(Return, on_delete=models.CASCADE)
    vaccines = models.ForeignKey(
        Vaccine, on_delete=models.SET_NULL, null=True)
    batch_number = models.CharField(max_length=100)
    quantity = models.IntegerField()


class Redistribute(models.Model):
    redistribute_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    source_orgunitid = models.CharField(max_length=50)
    source_orgunitiname = models.CharField(max_length=100)
    destination_orgunitid = models.CharField(max_length=50)
    destination_orgunitiname = models.CharField(max_length=100)
    reditribution_date = models.DateField(auto_now_add=True)


class RedistributeVaccine(models.Model):
    redistribute_uuid_vaccine_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    redistribute = models.ForeignKey(Redistribute, on_delete=models.CASCADE)
    vaccines = models.ForeignKey(
        Vaccine, on_delete=models.SET_NULL, null=True)
    batch_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
