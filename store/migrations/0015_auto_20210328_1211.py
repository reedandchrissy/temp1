# Generated by Django 3.1.5 on 2021-03-28 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20210328_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateTimeField(max_length=100, null=True),
        ),
    ]
