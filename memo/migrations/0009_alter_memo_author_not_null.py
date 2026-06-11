from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def remove_authorless_memos(apps, schema_editor):
    Memo = apps.get_model("memo", "Memo")
    Memo.objects.filter(author__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("memo", "0008_memo_is_pinned_memo_is_secret_memo_user_tags_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(remove_authorless_memos, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="memo",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="memos",
                to=settings.AUTH_USER_MODEL,
                verbose_name="작성자",
            ),
        ),
    ]
