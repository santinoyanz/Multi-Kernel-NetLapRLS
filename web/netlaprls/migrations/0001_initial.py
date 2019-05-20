# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-05-20 05:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enzyme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_id', models.CharField(max_length=16)),
                ('target_id', models.CharField(max_length=16)),
                ('score', models.FloatField(max_length=16)),
                ('kegg', models.CharField(default='', max_length=1)),
                ('drugbank', models.CharField(default='', max_length=1)),
                ('chembl', models.CharField(default='', max_length=1)),
                ('matador', models.CharField(default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='GPCR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_id', models.CharField(max_length=16)),
                ('target_id', models.CharField(max_length=16)),
                ('score', models.FloatField(max_length=16)),
                ('kegg', models.CharField(default='', max_length=1)),
                ('drugbank', models.CharField(default='', max_length=1)),
                ('chembl', models.CharField(default='', max_length=1)),
                ('matador', models.CharField(default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Ion_Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_id', models.CharField(max_length=16)),
                ('target_id', models.CharField(max_length=16)),
                ('score', models.FloatField(max_length=16)),
                ('kegg', models.CharField(default='', max_length=1)),
                ('drugbank', models.CharField(default='', max_length=1)),
                ('chembl', models.CharField(default='', max_length=1)),
                ('matador', models.CharField(default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Nuclear_Receptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_id', models.CharField(max_length=16)),
                ('target_id', models.CharField(max_length=16)),
                ('score', models.FloatField(max_length=16)),
                ('kegg', models.CharField(default='', max_length=1)),
                ('drugbank', models.CharField(default='', max_length=1)),
                ('chembl', models.CharField(default='', max_length=1)),
                ('matador', models.CharField(default='', max_length=1)),
            ],
        ),
    ]
