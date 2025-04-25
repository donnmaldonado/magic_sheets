from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Sheet, GradeLevel, Subject, Topic, SubTopic, Prompt
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        # Specifying the model to use
        model = User    
        # Specifying the fields to include in the form
        fields = ('username', 'email', 'password1', 'password2') 

    # Customizing the form to use bootstrap classes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to all fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to username and password fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })

class SheetCreationForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    grade_level = forms.ModelChoiceField(
        queryset=GradeLevel.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),  # Changed from none() to all()
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subtopic = forms.ModelChoiceField(
        queryset=SubTopic.objects.all(),  # Changed from none() to all()
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    prompt = forms.ModelChoiceField(
        queryset=Prompt.objects.filter(type="GENERATE"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    NUMBER_CHOICES = [(i, str(i)) for i in range(26)]  # 0 to 25

    true_false_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='True/False'
    )
    
    fill_blank_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Fill in the Blank'
    )
    
    multiple_choice_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Multiple Choice'
    )
    
    short_answer_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Short Answer'
    )
    
    include_answer_key = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        initial=True
    )
    published = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        initial=True
    )
    def clean(self):
            cleaned_data = super().clean()
            
            # Get all question counts
            true_false = int(cleaned_data.get('true_false_questions', 0))
            fill_blank = int(cleaned_data.get('fill_blank_questions', 0))
            multiple_choice = int(cleaned_data.get('multiple_choice_questions', 0))
            short_answer = int(cleaned_data.get('short_answer_questions', 0))
            
            # Calculate total
            total = true_false + fill_blank + multiple_choice + short_answer
            
            # Validate total
            if total > 25:
                raise forms.ValidationError("Total number of questions cannot exceed 25")
            elif total == 0:
                raise forms.ValidationError("Please select at least one question")
                
            return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If the form is being submitted (POST)
        if args and args[0]:
            if 'subject' in args[0] and 'grade_level' in args[0]:
                subject_id = args[0].get('subject')
                grade_level_id = args[0].get('grade_level')
                # Update topic queryset based on selected subject and grade level
                self.fields['topic'].queryset = Topic.objects.filter(
                    subject_id=subject_id,
                    grade_level_id=grade_level_id
                )
            
            if 'topic' in args[0]:
                topic_id = args[0].get('topic')
                # Update subtopic queryset based on selected topic
                self.fields['subtopic'].queryset = SubTopic.objects.filter(
                    topic_id=topic_id
                )
        else:
            # For initial form load, set empty querysets
            self.fields['topic'].queryset = Topic.objects.none()
            self.fields['subtopic'].queryset = SubTopic.objects.none()

class RegenerateSheetForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    prompt = forms.ModelChoiceField(
        queryset=Prompt.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Store current counts as hidden fields
    current_true_false = forms.IntegerField(widget=forms.HiddenInput())
    current_fill_blank = forms.IntegerField(widget=forms.HiddenInput())
    current_multiple_choice = forms.IntegerField(widget=forms.HiddenInput())
    current_short_answer = forms.IntegerField(widget=forms.HiddenInput())
    
    # Additional questions fields with dynamic max value
    NUMBER_CHOICES = [(i, str(i)) for i in range(26)]  # 0 to 25

    true_false_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Additional True/False Questions'
    )
    
    fill_blank_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Additional Fill in the Blank Questions'
    )
    
    multiple_choice_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Additional Multiple Choice Questions'
    )
    
    short_answer_questions = forms.ChoiceField(
        choices=NUMBER_CHOICES,
        initial='0',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Additional Short Answer Questions'
    )
    
    include_answer_key = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        initial=True
    )
    published = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        initial=True
    )
    
    def __init__(self, *args, **kwargs):
        current_counts = kwargs.pop('current_counts', None)
        super().__init__(*args, **kwargs)
        
        if current_counts:
            # Set initial values for current counts
            self.fields['current_true_false'].initial = current_counts['true_false']
            self.fields['current_fill_blank'].initial = current_counts['fill_blank']
            self.fields['current_multiple_choice'].initial = current_counts['multiple_choice']
            self.fields['current_short_answer'].initial = current_counts['short_answer']
            
            # Update the data-current attribute for each field
            self.fields['true_false_questions'].widget.attrs['data-current'] = current_counts['true_false']
            self.fields['fill_blank_questions'].widget.attrs['data-current'] = current_counts['fill_blank']
            self.fields['multiple_choice_questions'].widget.attrs['data-current'] = current_counts['multiple_choice']
            self.fields['short_answer_questions'].widget.attrs['data-current'] = current_counts['short_answer']

class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )