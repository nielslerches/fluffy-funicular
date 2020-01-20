from attributes.models import ObjectAttributeValue, Attribute, AttributeValue


def get_all_attribute_sets():
    object_attribute_values = ObjectAttributeValue.objects.select_related(
        'attribute_value',
        'attribute_value__attribute',
    ).filter(
        deleted_at=None,
    ).order_by(
        'object_type',
        'object_id',
    )

    object_type, object_id, attribute_set = None, None, {}

    for object_attribute_value in object_attribute_values.iterator():

        if object_type != object_attribute_value.object_type or object_id != object_attribute_value.object_id:

            if None not in (object_type, object_id):
                yield (object_type, object_id), attribute_set.copy()

            object_type = object_attribute_value.object_type
            object_id = object_attribute_value.object_id
            attribute_set = {}

        key = object_attribute_value.attribute_value.attribute.name
        value = object_attribute_value.attribute_value.name

        if object_attribute_value.attribute_value.attribute.can_have_multiple_values:

            if key not in attribute_set:
                attribute_set[key] = []

            attribute_set[key].append(value)

        else:
            attribute_set[key] = value

    if None not in (object_type, object_id):
        yield (object_type, object_id), attribute_set.copy()


def get_all_attributes():
    all_attributes = {}

    attribute_values = AttributeValue.objects.select_related('attribute').filter(deleted_at=None)

    for attribute_value in attribute_values.iterator():
        key = attribute_value.attribute.name
        value = attribute_value.name

        if key not in all_attributes:
            all_attributes[key] = {
                'choices': [],
                'multiple': attribute_value.attribute.can_have_multiple_values,
            }

        all_attributes[key]['choices'].append(value)

    return all_attributes
