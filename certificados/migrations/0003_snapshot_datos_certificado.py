from django.db import migrations, models


def copiar_datos_vecino(apps, schema_editor):

    Certificado = apps.get_model(
        "certificados",
        "Certificado",
    )

    certificados = (
        Certificado.objects
        .select_related(
            "solicitud__vecino"
        )
        .all()
    )

    for certificado in certificados.iterator():

        vecino = certificado.solicitud.vecino

        certificado.nombre_vecino = vecino.nombre
        certificado.apellido_vecino = vecino.apellido
        certificado.identificacion_vecino = vecino.identificacion
        certificado.direccion_vecino = vecino.direccion

        certificado.save(
            update_fields=[
                "nombre_vecino",
                "apellido_vecino",
                "identificacion_vecino",
                "direccion_vecino",
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        (
            "certificados",
            "0002_solicitudcertificado_solicitud_certificado_activa_unica_por_vecino",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="certificado",
            name="nombre_vecino",
            field=models.CharField(
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="certificado",
            name="apellido_vecino",
            field=models.CharField(
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="certificado",
            name="identificacion_vecino",
            field=models.CharField(
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="certificado",
            name="direccion_vecino",
            field=models.CharField(
                max_length=255,
                null=True,
            ),
        ),
        migrations.RunPython(
            copiar_datos_vecino,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="certificado",
            name="nombre_vecino",
            field=models.CharField(
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="certificado",
            name="apellido_vecino",
            field=models.CharField(
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="certificado",
            name="identificacion_vecino",
            field=models.CharField(
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="certificado",
            name="direccion_vecino",
            field=models.CharField(
                max_length=255,
            ),
        ),
    ]