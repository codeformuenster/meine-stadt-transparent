# Generated by Django 2.1.8 on 2019-04-04 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_auto_20190106_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaper',
            name='change_request_of',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='mainapp.Paper'),
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='family_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='given_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='family_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='given_name',
            field=models.CharField(max_length=100),
        ),
    ]
