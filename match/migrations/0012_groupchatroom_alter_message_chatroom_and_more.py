# Generated by Django 4.1.5 on 2023-04-05 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0011_profile_count_alter_interest_profile'),
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
        migrations.AlterField(
            model_name='message',
            name='chatRoom',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='match.chatroom'),
        ),
        migrations.AddField(
            model_name='message',
            name='groupChatRoom',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='match.groupchatroom'),
        ),
    ]
