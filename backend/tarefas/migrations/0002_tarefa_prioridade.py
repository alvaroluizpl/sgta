from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefa',
            name='prioridade',
            field=models.CharField(
                choices=[('URGENTE', 'Urgente'), ('NAO_URGENTE', 'Não urgente')],
                default='NAO_URGENTE',
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
