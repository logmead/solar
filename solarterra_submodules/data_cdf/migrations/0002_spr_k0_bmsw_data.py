# Generated by Django 4.2.16 on 2024-11-14 12:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_cdf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SPR_K0_BMSW_data',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('epoch', models.BigIntegerField(blank=True, null=True)),
                ('vp', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('tp', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('np', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('nanp', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('qual', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('st_flag', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('gap_flag', models.IntegerField(blank=True, null=True)),
                ('file_name', models.CharField(max_length=100)),
            ],
        ),
    ]
