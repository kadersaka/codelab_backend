# Generated by Django 4.1 on 2023-02-22 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iso', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('enabled', models.BooleanField(default=True, verbose_name='Show on app')),
                ('flag', models.ImageField(blank=True, null=True, upload_to='country_flags')),
            ],
            options={
                'verbose_name': 'County',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iso', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('enabled', models.BooleanField(default=True, verbose_name='Show on app')),
                ('flag', models.ImageField(blank=True, null=True, upload_to='country_flags')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='network_country', to='pal.country', verbose_name='Country')),
            ],
        ),
        migrations.AlterField(
            model_name='paltransaction',
            name='processed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='precessed_user', to=settings.AUTH_USER_MODEL, verbose_name='Processor'),
        ),
        migrations.AlterField(
            model_name='paltransaction',
            name='status',
            field=models.IntegerField(choices=[(0, 'CANCELLED'), (1, 'PENDING'), (2, 'PROCESSING'), (3, 'ERROR'), (4, 'RETRY'), (5, 'COMPLETED')], default=1),
        ),
        migrations.CreateModel(
            name='TransactionRemark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.CharField(max_length=255)),
                ('current_users', models.ManyToManyField(blank=True, related_name='remark_users', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_remarks', to='pal.paltransaction')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='network_phones', to='pal.network', verbose_name='network_phones')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paltransaction',
            name='network',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_network', to='pal.network', verbose_name='Network'),
        ),
    ]
