from flask import Flask, render_template, request, redirect, url_for, flash
from transformers import pipeline
import textstat

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Load summarization model (first time may take a minute)
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

# def summarize_text(text, max_length=150, min_length=50):
#     # If text > ~1000 words, split and summarize in chunks for long input
#     words = text.split()
#     if len(words) > 900:
#         chunks = [' '.join(words[i:i+900]) for i in range(0, len(words), 900)]
#         summaries = [summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text'] for chunk in chunks]
#         combined_summary = ' '.join(summaries)
#         # (Optional) Summarize again if combined is long
#         if len(combined_summary.split()) > 500:
#             return summarizer(combined_summary, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
#         return combined_summary
#     return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
def summarize_text(text, max_length=150, min_length=50):
    # BART has a token limit of 1024 -- safe limit is about 950 words per chunk
    max_words = 950
    words = text.split()
    if len(words) > max_words:
        # Do chunking
        chunks = []
        for i in range(0, len(words), max_words):
            chunk = ' '.join(words[i:i + max_words])
            # Don't send empty chunk
            if chunk.strip():
                try:
                    result = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                    summary = result[0]['summary_text'] if result else ""
                except Exception:
                    summary = ""
                if summary.strip():
                    chunks.append(summary)
        combined_summary = ' '.join(chunks)
        # If still too long, recursively summarize again (but now it will fit)
        if len(combined_summary.split()) > max_words:
            return summarize_text(combined_summary, max_length, min_length)
        return combined_summary
    else:
        result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]['summary_text']

def get_metrics(text, summary):
    return {
        'original_word_count': len(text.split()),
        'summary_word_count': len(summary.split()),
        'flesch_reading_ease': textstat.flesch_reading_ease(summary),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(summary),
        'gunning_fog': textstat.gunning_fog(summary),
        'smog_index': textstat.smog_index(summary),
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if not text:
            flash('Please enter some text to summarize.', 'error')
            return redirect(url_for('index'))
        summary = summarize_text(text)
        metrics = get_metrics(text, summary)
        return render_template('index.html', summary=summary, original_text=text, **metrics)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
