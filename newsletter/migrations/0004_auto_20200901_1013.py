# Generated by Django 2.2.6 on 2020-09-01 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0003_userdetailssocialnetworks_vkurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='awardnumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='patientnumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
