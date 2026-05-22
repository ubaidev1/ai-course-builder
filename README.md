# 🎓 Course Builder

Welcome to **Course Builder**, a comprehensive, AI-powered Learning Management System (LMS) built with Django. This platform provides an intuitive interface for both students and administrators, featuring dynamic course generation via AI, customizable UI, user invitations, and robust progress tracking.

---

## 🌟 Key Features

### 👨‍🎓 User & Admin Roles
The platform supports two primary roles: **Normal User** and **Admin**, each with distinct capabilities tailored to their needs.

#### User Features
- **Authentication & Enrollment:** Users can sign up, log in, and enroll in available courses.
- **Course Navigation:** Seamlessly view course details, track progress via visual progress bars, and navigate through modules and lessons.
- **Lesson Structure:** Each course is broken down into structured modules, containing detailed lessons and embedded videos.
- **Quizzes & Scores:** Test your knowledge at the end of lessons. Users can retake quizzes to improve their scores, which are recorded and displayed upon completion.
- **User Assistance:** Optimized for accessibility, the interface includes a dynamic sidebar for quick access to indexes, modules, and lessons, alongside breadcrumb navigation.

#### Admin Features
- **AI-Powered Course Generation:** Admins can effortlessly create full courses by simply **uploading a PDF file**. The platform uses the **Anthropic Claude API** to extract text, determine structure, and generate corresponding modules, lessons, and quizzes automatically.
- **Course Extension:** Easily append new modules, lessons, or quizzes to existing courses. 
- **Dashboards & Tracking:** Access a centralized dashboard to oversee course completion statuses, calculate percentages, and monitor student performance.
- **Result Management:** A dedicated Results table allows admins to view obtained scores, search via username/email, and filter results by course.

### 🎨 Customization & Branding (Admin Only)
Ensure the platform matches your branding by leveraging the built-in UI customization tools.
- Set global **Navbar Color**, **Background Color**, **Heading Color**, **Button Color**, and **Points Color**.
- Changes are applied globally to enhance the tailored learning experience.

### ✉️ User Invitations (Admin Only)
- Admins can directly invite new users to specific courses by sending automated email invitations.
- Status tracking allows admins to see if invitations are `Pending` or `Accepted`.

### 🤖 AI Integration Module (`antropic_api`)
The backbone of the automated content builder. 
- **PDF Extraction:** Seamlessly reads page content from uploaded PDFs.
- **LLM Prompting:** Uses the powerful `Claude` models to parse educational text and assemble it into structured JSON data.
- **Intelligent Parsing:** The system automatically identifies concepts, divides them into cohesive modules, generates teaching material for lessons, and formulates quiz questions with valid options.

---

## 🏗️ Architecture & Tech Stack

- **Backend:** Django, Python
- **Database:** SQLite (default for development), supports PostgreSQL
- **AI/ML:** Anthropic API (Claude) for intelligent content structuring, PyPDF2 for text extraction
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Django Templates

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Anthropic API Key (for the AI course generation feature)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/course_builder.git
   cd course_builder
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   - Add your Anthropic API Key in `config.json` inside the repository.
   - Configure email backend variables if using the email invitation functionality.

5. **Run Migrations & Start Server:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
   
6. **Access the platform:**
   - Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 📸 Interface Sneak Peek

- **Dynamic Courses:** Generate courses from PDFs in minutes instead of manually typing them out.
- **Engaging UI:** Customize colors using the Customization Settings through the Django Admin or Custom Dashboard.

*This project is continuously evolving. Feedback and contributions are welcome!*
