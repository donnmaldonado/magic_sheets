from django.db import migrations

def create_initial_prompt(apps, schema_editor):
    Prompt = apps.get_model("main", "Prompt")
    
    Prompt.objects.create(
        type="GENERATE",
        name="General Use",
        text="""Create a worksheet with the following specifications:
                - If there are short answer questions, make sure to leave 4 lines for the student to write their answer.
                - Do not respond in markdown.
                - Respond in plain text.
                - Make sure that you include the correct amount of questions for each type.
                - If there is an answer key, include it at the end of the worksheet.
            """
    )

def remove_initial_prompt(apps, schema_editor):
    Prompt = apps.get_model("main", "Prompt")
    Prompt.objects.filter(type="GENERATE").delete()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_initial_data'), 
    ]

    operations = [
        migrations.RunPython(create_initial_prompt, remove_initial_prompt),
    ]