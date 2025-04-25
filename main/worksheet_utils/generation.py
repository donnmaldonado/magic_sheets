import openai
from dotenv import load_dotenv
import os   
from main.models import Prompt
import re
load_dotenv()


def generate_worksheet_content(sheet):
    """
    Generate worksheet content using OpenAI API
    """
    # OPENAI API KEY
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # If the prompt is not General Use, add it to the prompt
    prompt = sheet.prompt.text
    if sheet.prompt.name != "General Use":
        prompt = Prompt.objects.get(name="General Use").text + "\n" + prompt

    specifications = f"""
    Subject: {sheet.subject.name}
    Grade Level: {sheet.grade_level.name}
    Topic: {sheet.topic.name}
    Subtopic: {sheet.sub_topic.name}
    Include Answer Key: {sheet.include_answer_key}
    
    Include the exact number questions for each type:
    - {sheet.true_false_count} True/False questions
    - {sheet.fill_in_the_blank_count} Fill in the blank questions
    - {sheet.multiple_choice_count} Multiple choice questions
    - {sheet.short_answer_count} Short answer questions
    
    Number the questions consecutively.
    """

    format = 'Please deliver the worksheet response inside triple quotes (""") and ensure there is no Markdown formatting, no special characters, and no extra spaces. Deliver the response as plain text within the quotes.'

    

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional educator creating a worksheet."},
                {"role": "user", "content": prompt + specifications + format}
            ],
            max_tokens=3000
        )
        print("\nToken Usage:")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        content = response.choices[0].message.content
        cleaned_content = re.sub(r'"{3}', '', content).strip()
        return cleaned_content
    
    except Exception as e:
        print(f"Error generating content: {e}")
        raise
    
def regenerate_worksheet_content(sheet, prompt, additional_questions):
    """
    Regenerate worksheet content using OpenAI API
    """
    # OPENAI API KEY
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Get the content of the worksheet
    content = sheet.content

    specifications = f"""
    Use the following instruction as a guide to regenerate the worksheet: 

    Keep the original questions but add the additional questions for each type so that the total number of questions is:
    - {sheet.true_false_count} True/False questions
    - {sheet.fill_in_the_blank_count} Fill in the blank questions
    - {sheet.multiple_choice_count} Multiple choice questions
    - {sheet.short_answer_count} Short answer questions

    Remember:
    Include Answer Key: {sheet.include_answer_key}
    If there are extra questions, group them with their respective question type and renumber all the question so they are consecutive. 
    Make sure to include all the additional questions in the response.
    {prompt.text}
    """
    format = 'Please deliver the worksheet response inside triple quotes (""") and ensure there is no Markdown formatting, no special characters, and no extra spaces. Deliver the response as plain text within the quotes.'

    # Replace prompt associated with the worksheet if it is not General Use or Corrective
    if prompt.name not in ["General Use", "Corrective"]:
        sheet.prompt = prompt
        sheet.save()
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional educator creating a worksheet."},
                {"role": "user", "content": specifications + "Here is the original worksheet: " + content + "\nMake sure to" + format}
            ],
            max_tokens=3000
        )
        print("\nToken Usage:")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        content = response.choices[0].message.content
        cleaned_content = re.sub(r'"{3}', '', content).strip()
        return cleaned_content
    
    except Exception as e:
        print(f"Error generating content: {e}")
        raise
    
    