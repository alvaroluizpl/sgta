import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0002_tarefa_prioridade'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefa',
            name='usuario_responsavel',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='usuarios.usuario',
            ),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='prioridade',
            field=models.CharField(
                choices=[('URGENTE', 'Urgente'), ('NAO_URGENTE', 'Não urgente')],
                max_length=20,
            ),
        ),
    ]
