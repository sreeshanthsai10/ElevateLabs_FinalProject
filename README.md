# AI Text Summarizer

A modern web application that generates concise summaries from long articles or documents using transformer-based NLP models (BART/T5).  
Built using Flask and Hugging Face Transformers, the app provides instant summaries, readability scores, and word statistics.

---

# Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [License](#license)
- [Support](#support)

---

# Overview

The AI Text Summarizer produces human-like abstractive summaries using state-of-the-art NLP models.  
It supports long-text chunking, readability metrics, modern UI design, and is fully deployment-ready.

---

# Features

- Abstractive text summarization (BART/T5)
- Readability metrics:
  - Flesch Reading Ease  
  - Flesch-Kincaid Grade  
  - Gunning Fog Index  
  - SMOG Index  
- Word count & compression ratio
- Responsive UI with loading spinner
- Mobile-friendly layout
- Automatic chunking for long texts
- Deployable to Heroku, Render, or any WSGI platform
- Optional SQLite summary history

---

# Tech Stack

## Backend
- Python 3.9+
- Flask
- Hugging Face Transformers
- PyTorch
- NLTK
- Textstat
- SQLite (optional)

## Frontend
- HTML5, CSS3
- Bootstrap 5
- JavaScript ES6

## Deployment
- Gunicorn
- Heroku / Render
- Git & GitHub

---

# File Structure

```text
ai-text-summarizer/
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
