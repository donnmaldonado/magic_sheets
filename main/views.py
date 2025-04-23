from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm, SheetCreationForm, ReviewForm
from .models import Sheet, Topic, SubTopic, Prompt, SavedSheet, LikedSheet, GradeLevel, Subject, Review
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .worksheet_utils.file_utils import create_sheet, create_worksheet_files
from .worksheet_utils.generation import regenerate_worksheet_content
from django.db import models
# Create your views here.

def home(request):
    return render(request, "home.html")

def login(request):
    # If POST request, process form data
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        # If GET request, create empty form
        form = UserLoginForm()
    
    return render(request, "login.html", {'form': form})

def signup(request):
    # If POST request, process form data
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        # If GET request, create empty form
        form = UserRegistrationForm()
    
    return render(request, "signup.html", {'form': form})

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def createsheet(request):
    if request.method == 'POST':
        print("Form submitted")  # Debug print
        form = SheetCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug print
            is_published = form.cleaned_data['published']
            # Create the sheet
            sheet = Sheet.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                published=is_published,
                grade_level=form.cleaned_data['grade_level'],
                subject=form.cleaned_data['subject'],
                topic=form.cleaned_data['topic'],
                sub_topic=form.cleaned_data['subtopic'],
                true_false_count=int(form.cleaned_data['true_false_questions']),
                fill_in_the_blank_count=int(form.cleaned_data['fill_blank_questions']),
                multiple_choice_count=int(form.cleaned_data['multiple_choice_questions']),
                short_answer_count=int(form.cleaned_data['short_answer_questions']),
                include_answer_key=form.cleaned_data['include_answer_sheet'],
                prompt = form.cleaned_data['prompt']
            )
            print(f"Sheet created with ID: {sheet.id}")  # Debug print
            
            # Generate the worksheet content and files
            try:
                #generate_worksheet_files(sheet)
                create_sheet(sheet)
                messages.success(request, 'Worksheet created successfully!')
            except Exception as e:
                messages.error(request, f'Error generating worksheet: {str(e)}')
                return redirect('createsheet')
            
            return redirect('viewsheet', sheet_id=sheet.id)
        else:
            print("Form errors:", form.errors)  # Debug print
    else:
        form = SheetCreationForm()
    
    return render(request, 'createsheet.html', {'form': form})

def get_topics(request):
    grade_level_id = request.GET.get('grade_level')
    subject_id = request.GET.get('subject')
    
    topics = Topic.objects.filter(grade_level_id=grade_level_id, subject_id=subject_id)
    return JsonResponse(list(topics.values('id', 'name')), safe=False)

def get_subtopics(request):
    topic_id = request.GET.get('topic')
    subtopics = SubTopic.objects.filter(topic_id=topic_id)
    return JsonResponse(list(subtopics.values('id', 'name')), safe=False)

#View worksheet view 
@login_required
def viewsheet(request, sheet_id):
    sheet = get_object_or_404(Sheet, id=sheet_id)
    
    # Only show permission error if trying to access private sheet of another user thats not published
    if not sheet.published and sheet.user != request.user:
        messages.error(request, 'You do not have permission to view this private worksheet.')
        return redirect('home')

    # Check if the worksheet is saved by the current user
    is_saved = SavedSheet.objects.filter(user=request.user, sheet=sheet).exists()
    is_liked = LikedSheet.objects.filter(user=request.user, sheet=sheet).exists()
    
    # Get all regenerate prompts for the dropdown
    regenerate_prompts = Prompt.objects.all()

    # Get reviews for the sheet
    reviews = Review.objects.filter(sheet=sheet).order_by('-created_at')
    
    # Check if user has already reviewed this sheet
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, sheet=sheet).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = int(form.cleaned_data['rating'])
            comment = form.cleaned_data['comment']
            
            # Update existing review or create new one
            if user_review:
                user_review.rating = rating
                print(user_review.rating)
                user_review.comment = comment
                user_review.save()
                messages.success(request, 'Your review has been updated!')
            else:
                Review.objects.create(
                    user=request.user,
                    sheet=sheet,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Thank you for your review!')
            return redirect('viewsheet', sheet_id=sheet_id)
    else:
        form = ReviewForm()

    context = {
        'sheet': sheet,
        'is_creator': sheet.user == request.user,
        'is_saved': is_saved,
        'is_liked': is_liked,
        'regenerate_prompts': regenerate_prompts,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': form
    }
    
    return render(request, 'viewsheet.html', context)

@require_POST
@login_required
def toggle_like(request, sheet_id):
    sheet = get_object_or_404(Sheet, id=sheet_id)
    like, created = LikedSheet.objects.get_or_create(user=request.user, sheet=sheet)
    
    if not created:
        # User already liked the sheet, so unlike it
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': sheet.like_count
    })

@require_POST
@login_required
def toggle_save(request, sheet_id):
    sheet = get_object_or_404(Sheet, id=sheet_id)
    saved_sheet, created = SavedSheet.objects.get_or_create(user=request.user, sheet=sheet)
    
    if not created:
        # User already saved the sheet, so unsave it
        saved_sheet.delete()
        saved = False
    else:
        saved = True

    return JsonResponse({
        'saved': saved
    })

@login_required
def editsheet(request, sheet_id):
    sheet = get_object_or_404(Sheet, id=sheet_id)
    
    # Only allow the creator to edit the sheet
    if sheet.user != request.user:
        messages.error(request, 'You do not have permission to edit this worksheet.')
        return redirect('viewsheet', sheet_id=sheet_id)
    
    if request.method == 'POST':
        new_content = request.POST.get('content', '')
        if new_content:
            sheet.content = new_content
            sheet.save()
            create_worksheet_files(sheet)
            
            return redirect('viewsheet', sheet_id=sheet_id)
        else:
            messages.error(request, 'Content cannot be empty.')
    
    context = {
        'sheet': sheet,
        'content': sheet.content
    }
    
    return render(request, 'editsheet.html', context)

@login_required
def regenerate_sheet(request, sheet_id):
    sheet = get_object_or_404(Sheet, id=sheet_id)
    
    # Only allow the creator to regenerate
    if sheet.user != request.user:
        messages.error(request, 'You do not have permission to regenerate this worksheet.')
        return redirect('viewsheet', sheet_id=sheet_id)
    
    if request.method == 'POST':
        prompt_id = request.POST.get('prompt_id')
        if prompt_id:
            try:
                # Update the sheet's prompt
                sheet.prompt = Prompt.objects.get(id=prompt_id)
                # Regenerate the content and files
                sheet.content = regenerate_worksheet_content(sheet, Prompt.objects.get(id=prompt_id))
                sheet.save()
                create_worksheet_files(sheet)
                messages.success(request, 'Worksheet regenerated successfully!')
            except Exception as e:
                messages.error(request, f'Error regenerating worksheet: {str(e)}')
        else:
            messages.warning(request, 'Please select a regeneration option.')
    
    return redirect('viewsheet', sheet_id=sheet_id)

def communitysheets(request):
    # Get all published sheets ordered by creation date (newest first)
    published_sheets = Sheet.objects.filter(published=True)
    
    # Get filter parameters from request
    grade_level = request.GET.get('grade_level')
    subject = request.GET.get('subject')
    topic = request.GET.get('topic')
    subtopic = request.GET.get('subtopic')
    sort_by = request.GET.get('sort_by', 'date_desc')  # Default to newest first
    
    # Apply filters if they exist
    if grade_level:
        published_sheets = published_sheets.filter(grade_level_id=grade_level)
    if subject:
        published_sheets = published_sheets.filter(subject_id=subject)
    if topic:
        published_sheets = published_sheets.filter(topic_id=topic)
    if subtopic:
        published_sheets = published_sheets.filter(sub_topic_id=subtopic)
    
    # Apply sorting
    if sort_by == 'date_desc':
        published_sheets = published_sheets.order_by('-created_at')
    elif sort_by == 'date_asc':
        published_sheets = published_sheets.order_by('created_at')
    elif sort_by == 'likes_desc':
        published_sheets = published_sheets.annotate(total_likes=models.Count('likes')).order_by('-total_likes')
    elif sort_by == 'likes_asc':
        published_sheets = published_sheets.annotate(total_likes=models.Count('likes')).order_by('total_likes')
    
    # Get all available options for filters
    grade_levels = GradeLevel.objects.all()
    subjects = Subject.objects.all()
    topics = Topic.objects.all()
    subtopics = SubTopic.objects.all()
    
    # Add is_saved information and average rating to each sheet
    if request.user.is_authenticated:
        saved_sheet_ids = set(SavedSheet.objects.filter(user=request.user).values_list('sheet_id', flat=True))
        for sheet in published_sheets:
            sheet.is_saved = sheet.id in saved_sheet_ids
            # Calculate average rating
            avg_rating = sheet.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
            sheet.avg_rating = round(avg_rating) if avg_rating else None
            # Calculate review count
            sheet.review_count = sheet.reviews.count()
    else:
        for sheet in published_sheets:
            sheet.is_saved = False
            # Calculate average rating
            avg_rating = sheet.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
            sheet.avg_rating = round(avg_rating) if avg_rating else None
            # Calculate review count
            sheet.review_count = sheet.reviews.count()
    
    context = {
        'published_sheets': published_sheets,
        'grade_levels': grade_levels,
        'subjects': subjects,
        'topics': topics,
        'subtopics': subtopics,
        'selected_grade': grade_level,
        'selected_subject': subject,
        'selected_topic': topic,
        'selected_subtopic': subtopic,
        'selected_sort': sort_by,
    }
    return render(request, 'communitysheets.html', context)

@login_required
def savedsheets(request):
    # Get all sheets saved by the current user
    saved_sheets = Sheet.objects.filter(
        savedsheet__user=request.user,
        published=True  # Only show published sheets
    )
    
    # Get filter parameters from request
    grade_level = request.GET.get('grade_level')
    subject = request.GET.get('subject')
    topic = request.GET.get('topic')
    subtopic = request.GET.get('subtopic')
    sort_by = request.GET.get('sort_by', 'date_desc')  # Default to newest first
    
    # Apply filters if they exist
    if grade_level:
        saved_sheets = saved_sheets.filter(grade_level_id=grade_level)
    if subject:
        saved_sheets = saved_sheets.filter(subject_id=subject)
    if topic:
        saved_sheets = saved_sheets.filter(topic_id=topic)
    if subtopic:
        saved_sheets = saved_sheets.filter(sub_topic_id=subtopic)
    
    # Apply sorting
    if sort_by == 'date_desc':
        saved_sheets = saved_sheets.order_by('-created_at')
    elif sort_by == 'date_asc':
        saved_sheets = saved_sheets.order_by('created_at')
    elif sort_by == 'likes_desc':
        saved_sheets = saved_sheets.annotate(total_likes=models.Count('likes')).order_by('-total_likes')
    elif sort_by == 'likes_asc':
        saved_sheets = saved_sheets.annotate(total_likes=models.Count('likes')).order_by('total_likes')
    
    # Get all available options for filters
    grade_levels = GradeLevel.objects.all()
    subjects = Subject.objects.all()
    topics = Topic.objects.all()
    subtopics = SubTopic.objects.all()
    
    context = {
        'saved_sheets': saved_sheets,
        'grade_levels': grade_levels,
        'subjects': subjects,
        'topics': topics,
        'subtopics': subtopics,
        'selected_grade': grade_level,
        'selected_subject': subject,
        'selected_topic': topic,
        'selected_subtopic': subtopic,
        'selected_sort': sort_by,
    }
    return render(request, 'savedsheets.html', context)