# Generated by Django 4.1.5 on 2023-04-05 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0017_remove_message_groupchatroom_delete_groupchatroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(max_length=100)),
                ('mini', models.IntegerField()),
                ('maxi', models.IntegerField()),
                ('prio', models.CharField(max_length=100)),
                ('npart', models.IntegerField()),
                ('interest', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
