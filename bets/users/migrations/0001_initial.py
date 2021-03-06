# Generated by Django 3.2.4 on 2021-06-04 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_streamer', models.BooleanField(default=False)),
                ('balance', models.IntegerField(default=100, verbose_name='Текущий баланс')),
                ('total_win', models.IntegerField(default=0, verbose_name='Всего побед')),
                ('total_lose', models.IntegerField(default=0, verbose_name='Всего Поражений')),
                ('total_earn', models.IntegerField(default=0, verbose_name='Всего Заработано')),
                ('custom_username', models.CharField(default='User Name', max_length=32, verbose_name='Никнейм')),
                ('avatar', models.ImageField(default='avatars/default.png', upload_to='avatars')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user_data',
            },
        ),
        migrations.CreateModel(
            name='BetHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('bet_amount', models.PositiveIntegerField(default=1)),
                ('win_amount', models.IntegerField(default=0)),
                ('streamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bet_on', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_bets',
            },
        ),
    ]
