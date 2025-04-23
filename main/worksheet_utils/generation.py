import openai
from dotenv import load_dotenv
import os   
from main.models import Prompt
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
    
    """

    

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional educator creating a worksheet."},
                {"role": "user", "content": prompt + specifications}
            ],
            max_tokens=2000
        )
        print("\nToken Usage:")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        content = response.choices[0].message.content.replace("**", "").replace("---", "")
        return content
    
    except Exception as e:
        print(f"Error generating content: {e}")
        raise
    
def regenerate_worksheet_content(sheet, prompt):
    """
    Regenerate worksheet content using OpenAI API
    """
    # OPENAI API KEY
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Get the content of the worksheet
    content = sheet.content

    # Replace prompt associated with the worksheet if it is not General Use or Corrective
    if prompt.name not in ["General Use", "Corrective"]:
        sheet.prompt = prompt
    sheet.save()
    print(sheet.prompt.name)
    # Get the specifications for the worksheet
    specifications = "Use the following instruction as a guide to regenerate the worksheet: " + prompt.text
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional educator creating a worksheet."},
                {"role": "user", "content": specifications + "Here is the original worksheet: " + content}
            ],
            max_tokens=2000
        )
        print("\nToken Usage:")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        content = response.choices[0].message.content.replace("**", "").replace("---", "")
        return content
    
    except Exception as e:
        print(f"Error generating content: {e}")
        raise
    
    