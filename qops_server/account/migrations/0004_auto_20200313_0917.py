# Generated by Django 3.0.3 on 2020-03-13 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200311_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nick_name',
            field=models.CharField(max_length=50, null=True, verbose_name='nick name'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='method',
            field=models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('ALL', 'ALL')], default='ALL', max_length=10, verbose_name='HTTP method'),
        ),
    ]
