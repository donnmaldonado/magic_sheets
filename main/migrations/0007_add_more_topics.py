from django.db import migrations

def add_more_topics(apps, schema_editor):
    GradeLevel = apps.get_model('main', 'GradeLevel')
    Subject = apps.get_model('main', 'Subject')
    Topic = apps.get_model('main', 'Topic')
    SubTopic = apps.get_model('main', 'SubTopic')

    # Get existing grade levels
    grade_level_objects = {gl.name: gl for gl in GradeLevel.objects.all()}

    # Additional topics and subtopics for each subject
    additional_topics = {
        'Mathematics': {
            'Number Sense and Operations': {
                'grades': ['Kindergarten', '1st Grade', '2nd Grade', '3rd Grade'],
                'subtopics': [
                    {'name': 'Number Recognition'},
                    {'name': 'Place Value'},
                    {'name': 'Rounding Numbers'},
                    {'name': 'Number Patterns'},
                    {'name': 'Mental Math Strategies'}
                ]
            },
            'Measurement and Data': {
                'grades': ['1st Grade', '2nd Grade', '3rd Grade', '4th Grade', '5th Grade'],
                'subtopics': [
                    {'name': 'Length and Distance'},
                    {'name': 'Weight and Mass'},
                    {'name': 'Time and Calendar'},
                    {'name': 'Money and Currency'},
                    {'name': 'Data Representation'}
                ]
            },
            'Advanced Algebra': {
                'grades': ['10th Grade', '11th Grade'],
                'subtopics': [
                    {'name': 'Polynomial Functions'},
                    {'name': 'Rational Expressions'},
                    {'name': 'Exponential Functions'},
                    {'name': 'Logarithmic Functions'},
                    {'name': 'Complex Numbers'}
                ]
            },
            'Advanced Geometry': {
                'grades': ['11th Grade', '12th Grade'],
                'subtopics': [
                    {'name': 'Transformations'},
                    {'name': 'Similarity and Congruence'},
                    {'name': 'Circle Theorems'},
                    {'name': '3D Geometry'},
                    {'name': 'Geometric Proofs'}
                ]
            }
        },
        'English Language Arts': {
            'Vocabulary Development': {
                'grades': ['1st Grade', '2nd Grade', '3rd Grade', '4th Grade', '5th Grade'],
                'subtopics': [
                    {'name': 'Word Roots and Affixes'},
                    {'name': 'Context Clues'},
                    {'name': 'Synonyms and Antonyms'},
                    {'name': 'Multiple Meaning Words'},
                    {'name': 'Academic Vocabulary'}
                ]
            },
            'Speaking and Listening': {
                'grades': ['Kindergarten', '1st Grade', '2nd Grade', '3rd Grade', '4th Grade', '5th Grade'],
                'subtopics': [
                    {'name': 'Oral Presentations'},
                    {'name': 'Active Listening'},
                    {'name': 'Group Discussions'},
                    {'name': 'Public Speaking'},
                    {'name': 'Debate Skills'}
                ]
            },
            'Media Literacy': {
                'grades': ['6th Grade', '7th Grade', '8th Grade', '9th Grade', '10th Grade'],
                'subtopics': [
                    {'name': 'Digital Media Analysis'},
                    {'name': 'News Literacy'},
                    {'name': 'Advertising Techniques'},
                    {'name': 'Social Media Impact'},
                    {'name': 'Media Bias and Credibility'}
                ]
            },
            'Creative Writing': {
                'grades': ['4th Grade', '5th Grade', '6th Grade', '7th Grade', '8th Grade'],
                'subtopics': [
                    {'name': 'Poetry Writing'},
                    {'name': 'Short Stories'},
                    {'name': 'Character Development'},
                    {'name': 'Setting and Atmosphere'},
                    {'name': 'Dialogue Writing'}
                ]
            }
        },
        'Science': {
            'Scientific Method': {
                'grades': ['3rd Grade', '4th Grade', '5th Grade', '6th Grade'],
                'subtopics': [
                    {'name': 'Hypothesis Formation'},
                    {'name': 'Experimental Design'},
                    {'name': 'Data Collection'},
                    {'name': 'Analysis and Conclusion'},
                    {'name': 'Scientific Communication'}
                ]
            },
            'Astronomy': {
                'grades': ['6th Grade', '7th Grade', '8th Grade', '9th Grade'],
                'subtopics': [
                    {'name': 'Stars and Galaxies'},
                    {'name': 'Space Exploration'},
                    {'name': 'Cosmology'},
                    {'name': 'Space Technology'},
                    {'name': 'Astronomical Phenomena'}
                ]
            },
            'Advanced Physics': {
                'grades': ['12th Grade'],
                'subtopics': [
                    {'name': 'Quantum Mechanics'},
                    {'name': 'Relativity'},
                    {'name': 'Nuclear Physics'},
                    {'name': 'Particle Physics'},
                    {'name': 'Modern Physics Applications'}
                ]
            },
            'Marine Science': {
                'grades': ['9th Grade', '10th Grade', '11th Grade'],
                'subtopics': [
                    {'name': 'Ocean Ecosystems'},
                    {'name': 'Marine Biology'},
                    {'name': 'Oceanography'},
                    {'name': 'Marine Conservation'},
                    {'name': 'Coastal Processes'}
                ]
            }
        },
        'Social Studies': {
            'Cultural Studies': {
                'grades': ['3rd Grade', '4th Grade', '5th Grade', '6th Grade'],
                'subtopics': [
                    {'name': 'World Cultures'},
                    {'name': 'Traditions and Customs'},
                    {'name': 'Cultural Heritage'},
                    {'name': 'Global Citizenship'},
                    {'name': 'Cultural Exchange'}
                ]
            },
            'Modern World Issues': {
                'grades': ['9th Grade', '10th Grade', '11th Grade', '12th Grade'],
                'subtopics': [
                    {'name': 'Global Conflicts'},
                    {'name': 'Human Rights'},
                    {'name': 'International Relations'},
                    {'name': 'Globalization'},
                    {'name': 'Contemporary Challenges'}
                ]
            },
            'Geography Skills': {
                'grades': ['6th Grade', '7th Grade', '8th Grade'],
                'subtopics': [
                    {'name': 'Geographic Information Systems'},
                    {'name': 'Population Geography'},
                    {'name': 'Economic Geography'},
                    {'name': 'Political Geography'},
                    {'name': 'Environmental Geography'}
                ]
            },
            'Financial Literacy': {
                'grades': ['9th Grade', '10th Grade', '11th Grade', '12th Grade'],
                'subtopics': [
                    {'name': 'Budgeting and Saving'},
                    {'name': 'Investing Basics'},
                    {'name': 'Credit and Debt'},
                    {'name': 'Taxation'},
                    {'name': 'Financial Planning'}
                ]
            }
        }
    }

    # Create new topics and subtopics
    subject_id = Subject.objects.latest('id').id + 1
    topic_id = Topic.objects.latest('id').id + 1
    subtopic_id = SubTopic.objects.latest('id').id + 1
    
    for subject_name, subject_data in additional_topics.items():
        # Get existing subject
        subject = Subject.objects.get(name=subject_name)
        
        # Create Topics for this Subject
        for topic_name, topic_data in subject_data.items():
            # Create topic for each grade level it appears in
            for grade_name in topic_data['grades']:
                topic = Topic.objects.create(
                    id=topic_id,
                    subject=subject,
                    grade_level=grade_level_objects[grade_name],
                    name=topic_name,
                )
                topic_id += 1
                
                # Create Subtopics for this Topic
                for subtopic_data in topic_data['subtopics']:
                    SubTopic.objects.create(
                        id=subtopic_id,
                        topic=topic,
                        name=subtopic_data['name']
                    )
                    subtopic_id += 1

def remove_additional_topics(apps, schema_editor):
    Topic = apps.get_model('main', 'Topic')
    # Remove only the topics we added in this migration
    Topic.objects.filter(name__in=[
        'Number Sense and Operations',
        'Measurement and Data',
        'Advanced Algebra',
        'Advanced Geometry',
        'Vocabulary Development',
        'Speaking and Listening',
        'Media Literacy',
        'Creative Writing',
        'Scientific Method',
        'Astronomy',
        'Advanced Physics',
        'Marine Science',
        'Cultural Studies',
        'Modern World Issues',
        'Geography Skills',
        'Financial Literacy'
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0006_sheet_parent_sheet_sheet_updated_at_and_more'),
    ]

    operations = [
        migrations.RunPython(add_more_topics, remove_additional_topics),
    ] 