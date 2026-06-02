from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model("memo", "Category")

    defaults = [
        {"name": "생활", "icon": "🏠", "order": 1},
        {"name": "업무", "icon": "💼", "order": 2},
        {"name": "학습", "icon": "📚", "order": 3},
        {"name": "임시", "icon": "📝", "order": 4},
        {"name": "이벤트", "icon": "🎉", "order": 5},
    ]

    for item in defaults:
        Category.objects.update_or_create(
            name=item["name"],
            defaults={"icon": item["icon"], "order": item["order"]},
        )

def unseed_categories(apps, schema_editor):
    Category = apps.get_model("memo", "Category")
    Category.objects.filter(name__in=["생활", "업무", "학습", "임시", "이벤트"]).delete()

class Migration(migrations.Migration):

    dependencies = [
    ("memo", "0001_initial"),
]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
