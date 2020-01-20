from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey

from shared.models import TimestampedModel


class Attribute(TimestampedModel, models.Model):
    name = models.CharField(max_length=255)
    can_have_multiple_values = models.BooleanField(default=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('name',),
                name='attributes_attribute_name_unique',
            ),
        )

    def __str__(self):
        return self.name


class AttributeValue(TimestampedModel, models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('attribute', 'name'),
                name='attributes_attributevalue_attribute_name_unique',
            ),
        )

    def __str__(self):
        return self.name


class ObjectAttributeValue(TimestampedModel, models.Model):
    object_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('object_type', 'object_id')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('object_type', 'object_id', 'attribute_value'),
                name='attributes_objectattributevalue_object_type_id_attribute_value_unique',
            ),
        )
