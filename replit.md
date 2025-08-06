# Overview

This is a Student Bulletin Management System (Sistema de Boletins SENAI) built for SENAI (Serviço Nacional de Aprendizagem Industrial), a Brazilian technical education institution. The application manages student records, subjects, grades, and generates academic bulletins with PDF export functionality. It provides a complete academic administration interface for technical course management, specifically defaulting to "Técnico em Desenvolvimento de Sistemas" (Technical Systems Development) course.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5.3.0 for responsive design and components
- **Styling**: Custom CSS with SENAI brand colors (red theme) and Font Awesome icons
- **JavaScript**: Vanilla JavaScript for client-side interactions including form validation, tooltips, and auto-hiding flash messages
- **Layout Structure**: Base template with navigation bar and consistent SENAI branding across all pages

## Backend Architecture
- **Web Framework**: Flask (Python) with modular route structure
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy integration
- **Form Handling**: WTForms with Flask-WTF for form validation and CSRF protection
- **Session Management**: Flask sessions with configurable secret key
- **Middleware**: ProxyFix for handling proxy headers in deployment environments

## Data Model Design
- **Student Model**: Stores student information including name, registration number, email, phone, and course
- **Subject Model**: Manages academic subjects with code, name, and workload (hours)
- **Grade Model**: Tracks multiple grades per student-subject combination (grade_1, grade_2, grade_3, final_grade) plus attendance (absences)
- **Relationships**: One-to-many relationships between Student/Subject and Grade entities with cascade delete operations

## PDF Generation
- **Library**: ReportLab for PDF creation
- **Features**: Academic bulletin generation with SENAI branding, student information, and grade tables
- **Output**: In-memory PDF generation with download capability

## Application Structure
- **Separation of Concerns**: Distinct modules for models, routes, forms, and PDF generation
- **Configuration**: Environment-based configuration for database URLs and session secrets
- **Error Handling**: Form validation with user-friendly error messages and flash notifications

# External Dependencies

## Database
- **Primary**: SQLite (default) with PostgreSQL support via DATABASE_URL environment variable
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

## Frontend Libraries
- **Bootstrap**: v5.3.0 via CDN for UI components and responsive design
- **Font Awesome**: v6.4.0 via CDN for icons throughout the interface

## Python Packages
- **Flask**: Core web framework
- **Flask-SQLAlchemy**: Database ORM integration
- **WTForms/Flask-WTF**: Form handling and validation
- **ReportLab**: PDF generation for academic bulletins
- **Werkzeug**: WSGI utilities and middleware (ProxyFix)

## Development Environment
- **Debug Mode**: Enabled for development with hot reloading
- **Logging**: Basic logging configuration for debugging
- **Static Files**: Served via Flask for CSS, JavaScript, and image assets