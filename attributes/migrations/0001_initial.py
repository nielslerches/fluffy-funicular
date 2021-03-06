# Generated by Django 2.2.6 on 2019-10-22 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('can_have_multiple_values', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.AttributeValue')),
                ('object_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.AddConstraint(
            model_name='attribute',
            constraint=models.UniqueConstraint(fields=('name',), name='attributes_attribute_name_unique'),
        ),
        migrations.AddConstraint(
            model_name='objectattributevalue',
            constraint=models.UniqueConstraint(fields=('object_type', 'object_id', 'attribute_value'), name='attributes_objectattributevalue_object_type_id_attribute_value_unique'),
        ),
        migrations.AddConstraint(
            model_name='attributevalue',
            constraint=models.UniqueConstraint(fields=('attribute', 'name'), name='attributes_attributevalue_attribute_name_unique'),
        ),
    ]
