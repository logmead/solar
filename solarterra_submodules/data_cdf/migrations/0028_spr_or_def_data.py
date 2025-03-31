# Generated by Django 4.2.16 on 2024-12-06 11:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_cdf', '0027_delete_wi_k0_swe_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='SPR_OR_DEF_data',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('epoch', models.BigIntegerField(blank=True, null=True)),
                ('sc_pos_gse_x', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('sc_pos_gse_y', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('sc_pos_gse_z', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('sc_pos_gsm_x', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('sc_pos_gsm_y', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('sc_pos_gsm_z', models.DecimalField(blank=True, decimal_places=6, max_digits=13, null=True)),
                ('reg', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('gap_flag', models.IntegerField(blank=True, null=True)),
                ('file_name', models.CharField(max_length=100)),
            ],
        ),
    ]
