# MagicSheets

MagicSheets is a generative AI-powered platform that helps educators, parents, and students quickly create and customize worksheets for K–12 learning. Users can generate worksheets by topic, type (e.g. multiple choice, short answer), and complexity, then refine them, regenerate with special instructions, and save or share them with the community.

## Features

- **Worksheet Generator**  
  Choose subject, grade, topic, and worksheet type. Supports Multiple Choice, Fill-in-the-Blank, True/False, and more.

- **Custom Regeneration**  
  Regenerate worksheets with smart prompts like "make it more descriptive" or "simplify."

- **Answer Sheets**  
  Toggle answer key generation with each worksheet.

- **Powered by LLMs**  
  Uses OpenAI’s API for fast, context-aware worksheet creation.

- **Curriculum-Based Structure**  
  Organized by subject, grade, topic, and subtopic to support standards-aligned learning.

- **Community Tools**  
  Save, vote, and remix worksheets from others in the MagicSheets ecosystem.

- **In-Browser DOCX Editing**  
  Users can modify worksheets directly in the browser before downloading.

## Tech Stack

- **Backend:** Django, PostgreSQL  
- **Frontend:** Django templates, JavaScript  
- **AI Integration:** OpenAI GPT-4o  
- **Document Handling:** python-docx, ReportLab  
- **Deployment:** Render, Gunicorn, WhiteNoise  
- **Environment Management:** Python 3.11, virtualenv  

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/donnmaldonado/magic_sheets
   cd magic_sheets
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Create a `.env` file in the root directory and add:
   ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    OPENAI_API_KEY=your_openai_key
    EMAIL_HOST=email_host
    EMAIL_PORT=email_port
    EMAIL_HOST_USER=email_user
    EMAIL_HOST_PASSWORD=email_password
    DB_SERVICE=your_postgres_url
   ```

5. **Run the Server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
