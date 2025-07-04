# Generated by Django 5.2 on 2025-04-18 23:10

from django.db import migrations

def add_prompts(apps, schema_editor):
    Prompt = apps.get_model('main', 'Prompt')
    
    prompts = [
        {
            'type': 'GENERATE',
            'name': 'Focus-Friendly (ADHD Support)',
            'text': """Make this worksheet clear and concise, with short instructions and simple formatting. 
            Use numbered steps and avoid long paragraphs to help students with attention challenges. Explain what is expected in the answer of each question.""",
        },
        {
            'type': 'GENERATE',
            'name': 'Neurodiverse-Friendly (ASD Support)',
            'text': """Keep the structure consistent and avoid figurative language or idioms.
            Use literal, clear language with straightforward questions. Explain what is expected in the answer of each question.""",
        },
        {
            'type': 'GENERATE',
            'name': 'English Language Learner Version',
            'text': """Use simple vocabulary and short sentences. Avoid complex grammar and idioms.
		    Include a definition in parentheses for any difficult word. Explain what is expected in the answer of each question.""",
        },
        {
            'type': 'GENERATE', 
            'name': 'Adult Learner Version',
            'text': """Use professional or real-world examples instead of school-themed content.
		    Avoid childish tone or vocabulary — keep it mature and respectful.""",
        },
        {
            'type': 'GENERATE',
            'name': 'Simpler Language Version',
            'text': """Simplify the language and make it more understandable for the student. Explain steps needed to solve the question.""",
        },
        {
            'type': 'GENERATE',
            'name': 'Extra Descriptive Version',
            'text': """Make the worksheet more descriptive and detailed. Make all questions more descriptive and detailed.""",
        },
        {
            'type': 'CORRECTIVE',
            'name': 'Fix Incorrect Answers',
            'text': """Review the answers, there is one or more that are incorrect.""",
        },
        {
            'type': 'CORRECTIVE',
            'name': 'Fix Notation Errors',
            'text': """Review the notation, there is one or more that are incorrect.""",
        },
    ]
    
    for prompt_data in prompts:
        Prompt.objects.create(**prompt_data)

def remove_prompts(apps, schema_editor):
    Prompt = apps.get_model('main', 'Prompt')
    Prompt.objects.filter(type='REGENERATE').delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_populate_prompt_table"),
    ]

    operations = [
        migrations.RunPython(add_prompts, remove_prompts),
    ]
