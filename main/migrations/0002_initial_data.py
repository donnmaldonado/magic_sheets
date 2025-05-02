from django.db import migrations

def create_initial_data(apps, schema_editor):
    GradeLevel = apps.get_model('main', 'GradeLevel')
    Subject = apps.get_model('main', 'Subject')
    Topic = apps.get_model('main', 'Topic')
    SubTopic = apps.get_model('main', 'SubTopic')

    # Create Grade Levels and store references
    grade_level_objects = {}
    grade_levels = [
        {'id': 1, 'name': 'Kindergarten', 'order': 0, 'code': 'K'},
        {'id': 2, 'name': '1st Grade', 'order': 1, 'code': '1'},
        {'id': 3, 'name': '2nd Grade', 'order': 2, 'code': '2'},
        {'id': 4, 'name': '3rd Grade', 'order': 3, 'code': '3'},
        {'id': 5, 'name': '4th Grade', 'order': 4, 'code': '4'},
        {'id': 6, 'name': '5th Grade', 'order': 5, 'code': '5'},
        {'id': 7, 'name': '6th Grade', 'order': 6, 'code': '6'},
        {'id': 8, 'name': '7th Grade', 'order': 7, 'code': '7'},
        {'id': 9, 'name': '8th Grade', 'order': 8, 'code': '8'},
        {'id': 10, 'name': '9th Grade', 'order': 9, 'code': '9'},
        {'id': 11, 'name': '10th Grade', 'order': 10, 'code': '10'},
        {'id': 12, 'name': '11th Grade', 'order': 11, 'code': '11'},
        {'id': 13, 'name': '12th Grade', 'order': 12, 'code': '12'}
    ]
    for grade in grade_levels:
        code = grade.pop('code')  # Remove code before creating object
        grade_obj = GradeLevel.objects.create(**grade)
        grade_level_objects[code] = grade_obj

    # Define the complete subject hierarchy
    subjects_data = {
        'Mathematics': {
            'topics': {
                'Addition and Subtraction': {
                    'grades': ['K', '1', '2', '3'],
                    'subtopics': [
                        {'name': 'Single Digit Addition'},
                        {'name': 'Double Digit Addition'},
                        {'name': 'Regrouping/Subtraction with Borrowing'},
                        {'name': 'Word Problems'}
                    ]
                },
                'Multiplication and Division': {
                    'grades': ['2', '3', '4', '5'],
                    'subtopics': [
                        {'name': 'Times Tables'},
                        {'name': 'Multi-Digit Multiplication'},
                        {'name': 'Basic Division'},
                        {'name': 'Long Division'}
                    ]
                },
                'Fractions and Decimals': {
                    'grades': ['3', '4', '5', '6'],
                    'subtopics': [
                        {'name': 'Understanding Fractions'},
                        {'name': 'Adding and Subtracting Fractions'},
                        {'name': 'Multiplying and Dividing Fractions'},
                        {'name': 'Decimals and Place Value'},
                        {'name': 'Converting Fractions and Decimals'}
                    ]
                },
                'Pre-Algebra': {
                    'grades': ['6', '7'],
                    'subtopics': [
                        {'name': 'Variables and Expressions'},
                        {'name': 'Order of Operations'},
                        {'name': 'Basic Equations'},
                        {'name': 'Inequalities'}
                    ]
                },
                'Algebra': {
                    'grades': ['8', '9'],
                    'subtopics': [
                        {'name': 'Linear Equations'},
                        {'name': 'Functions'},
                        {'name': 'Systems of Equations'},
                        {'name': 'Quadratic Equations'}
                    ]
                },
                'Geometry': {
                    'grades': ['8', '9', '10'],
                    'subtopics': [
                        {'name': 'Angles and Lines'},
                        {'name': 'Triangles and Circles'},
                        {'name': 'Area and Volume'},
                        {'name': 'Coordinate Geometry'}
                    ]
                },
                'Trigonometry': {
                    'grades': ['10', '11'],
                    'subtopics': [
                        {'name': 'Sine, Cosine, Tangent'},
                        {'name': 'Trigonometric Identities'},
                        {'name': 'Graphs of Trig Functions'}
                    ]
                },
                'Statistics and Probability': {
                    'grades': ['6', '7', '11', '12'],
                    'subtopics': [
                        {'name': 'Mean, Median, Mode'},
                        {'name': 'Probability Models'},
                        {'name': 'Data Analysis'},
                        {'name': 'Standard Deviation'}
                    ]
                },
                'Calculus': {
                    'grades': ['11', '12'],
                    'subtopics': [
                        {'name': 'Limits and Continuity'},
                        {'name': 'Derivatives'},
                        {'name': 'Integrals'},
                        {'name': 'Applications of Calculus'}
                    ]
                }
            }
        },
        'English Language Arts': {
            'topics': {
                'Reading Comprehension': {
                    'grades': ['1', '2', '3', '4', '5'],
                    'subtopics': [
                        {'name': 'Main Idea and Details'},
                        {'name': 'Character Analysis'},
                        {'name': 'Story Elements'},
                        {'name': 'Inference and Conclusion'}
                    ]
                },
                'Writing and Composition': {
                    'grades': ['3', '4', '5', '6', '7'],
                    'subtopics': [
                        {'name': 'Paragraph Structure'},
                        {'name': 'Persuasive Writing'},
                        {'name': 'Narrative Writing'},
                        {'name': 'Opinion Writing'}
                    ]
                },
                'Grammar and Usage': {
                    'grades': ['2', '3', '4', '5', '6'],
                    'subtopics': [
                        {'name': 'Parts of Speech'},
                        {'name': 'Sentence Structure'},
                        {'name': 'Punctuation and Capitalization'},
                        {'name': 'Subject-Verb Agreement'}
                    ]
                },
                'Literary Analysis': {
                    'grades': ['7', '8', '9', '10'],
                    'subtopics': [
                        {'name': 'Theme and Symbolism'},
                        {'name': 'Figurative Language'},
                        {'name': 'Tone and Mood'},
                        {'name': 'Comparing Texts'}
                    ]
                },
                'Research and Argumentation': {
                    'grades': ['9', '10', '11', '12'],
                    'subtopics': [
                        {'name': 'Thesis Statements'},
                        {'name': 'Using Evidence'},
                        {'name': 'Citing Sources'},
                        {'name': 'Constructing Arguments'}
                    ]
                }
            }
        },
        'Science': {
            'topics': {
                'Basic Forces and Motion': {
                    'grades': ['K', '1', '2'],
                    'subtopics': [
                        {'name': 'Push and Pull'},
                        {'name': 'Gravity'},
                        {'name': 'Friction'}
                    ]
                },
                'Earth and Space Science': {
                    'grades': ['3', '4', '5', '6'],
                    'subtopics': [
                        {'name': 'Planets and Solar System'},
                        {'name': 'Weather and Climate'},
                        {'name': 'Earth’s Layers'},
                        {'name': 'Rocks and Minerals'}
                    ]
                },
                'Life Science': {
                    'grades': ['2', '3', '4', '5', '6'],
                    'subtopics': [
                        {'name': 'Plant and Animal Life'},
                        {'name': 'Ecosystems'},
                        {'name': 'Human Body Systems'},
                        {'name': 'Cells and Genetics'}
                    ]
                },
                'Physical Science': {
                    'grades': ['6', '7', '8'],
                    'subtopics': [
                        {'name': 'Atoms and Molecules'},
                        {'name': 'States of Matter'},
                        {'name': 'Chemical Reactions'},
                        {'name': 'Energy Transfer'}
                    ]
                },
                'Biology': {
                    'grades': ['9', '10'],
                    'subtopics': [
                        {'name': 'Cell Structure'},
                        {'name': 'DNA and Heredity'},
                        {'name': 'Evolution'},
                        {'name': 'Ecology'}
                    ]
                },
                'Chemistry': {
                    'grades': ['10', '11'],
                    'subtopics': [
                        {'name': 'Periodic Table'},
                        {'name': 'Chemical Bonds'},
                        {'name': 'Stoichiometry'},
                        {'name': 'Acids and Bases'}
                    ]
                },
                'Physics': {
                    'grades': ['11', '12'],
                    'subtopics': [
                        {'name': 'Newton’s Laws'},
                        {'name': 'Kinematics'},
                        {'name': 'Electricity and Magnetism'},
                        {'name': 'Waves and Optics'}
                    ]
                },
                'Environmental Science': {
                    'grades': ['9', '10', '11'],
                    'subtopics': [
                        {'name': 'Pollution'},
                        {'name': 'Natural Resources'},
                        {'name': 'Climate Change'},
                        {'name': 'Sustainability'}
                    ]
                }
            }
        },
        'Social Studies': {
            'topics': {
                'Geography': {
                    'grades': ['K', '1', '2', '3', '4', '5'],
                    'subtopics': [
                        {'name': 'Continents and Oceans'},
                        {'name': 'Countries and Capitals'},
                        {'name': 'Physical Features'},
                        {'name': 'Map Skills'}
                    ]
                },
                'U.S. History': {
                    'grades': ['4', '5', '6', '7'],
                    'subtopics': [
                        {'name': 'Colonial America'},
                        {'name': 'American Revolution'},
                        {'name': 'Civil War'},
                        {'name': 'Civil Rights Movement'}
                    ]
                },
                'World History': {
                    'grades': ['6', '7', '8'],
                    'subtopics': [
                        {'name': 'Ancient Civilizations'},
                        {'name': 'Middle Ages'},
                        {'name': 'Industrial Revolution'},
                        {'name': 'World Wars'}
                    ]
                },
                'Civics and Government': {
                    'grades': ['6', '7', '8', '9'],
                    'subtopics': [
                        {'name': 'Branches of Government'},
                        {'name': 'Constitution'},
                        {'name': 'Voting and Elections'},
                        {'name': 'Citizenship'}
                    ]
                },
                'Economics': {
                    'grades': ['9', '10', '11'],
                    'subtopics': [
                        {'name': 'Supply and Demand'},
                        {'name': 'Personal Finance'},
                        {'name': 'Economic Systems'},
                        {'name': 'Global Trade'}
                    ]
                },
                'Sociology and Psychology': {
                    'grades': ['11', '12'],
                    'subtopics': [
                        {'name': 'Social Structures'},
                        {'name': 'Human Behavior'},
                        {'name': 'Mental Health Awareness'},
                        {'name': 'Cultural Diversity'}
                    ]
                }
            }
        }
    }



    # Create Subjects, Topics, and Subtopics
    subject_id = 1
    topic_id = 1
    subtopic_id = 1
    
    for subject_name, subject_data in subjects_data.items():
        # Create Subject
        subject = Subject.objects.create(
            id=subject_id,
            name=subject_name
        )
        subject_id += 1
        
        # Create Topics for this Subject
        for topic_name, topic_data in subject_data['topics'].items():
            # Create topic for each grade level it appears in
            for grade_code in topic_data['grades']:
                topic = Topic.objects.create(
                    id=topic_id,
                    subject=subject,
                    grade_level=grade_level_objects[grade_code],
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

def remove_initial_data(apps, schema_editor):
    GradeLevel = apps.get_model('main', 'GradeLevel')
    Subject = apps.get_model('main', 'Subject')
    
    # Due to CASCADE, this will remove all related Topics and SubTopics
    Subject.objects.all().delete()
    GradeLevel.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, remove_initial_data),
    ]