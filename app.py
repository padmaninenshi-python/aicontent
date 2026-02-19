from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# Initialize Groq client
# Set your Groq API key as an environment variable: GROQ_API_KEY
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        topic = data.get('topic', '')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Generate blog titles
        titles_prompt = f"""Generate 5 creative and engaging blog post titles about: {topic}
        
Make them SEO-friendly, attention-grabbing, and diverse in style.
Return only the titles, numbered 1-5."""

        titles_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": titles_prompt}],
            temperature=0.8,
            max_tokens=500
        )
        
        titles = titles_response.choices[0].message.content.strip()
        
        # Generate blog content
        blog_prompt = f"""Write a comprehensive, well-structured blog post about: {topic}

Requirements:
- Write 800-1200 words
- Use engaging, conversational tone
- Include an introduction, main points with subheadings, and conclusion
- Make it informative and valuable to readers
- Use clear paragraphs and proper formatting

Write the complete blog post:"""

        blog_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": blog_prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        blog_content = blog_response.choices[0].message.content.strip()
        
        # Generate SEO keywords
        keywords_prompt = f"""Based on this topic: {topic}

Generate 15-20 SEO keywords and phrases that would help this content rank well.
Include:
- Primary keywords (high search volume)
- Long-tail keywords (specific phrases)
- Related terms and semantic keywords

Return only the keywords, separated by commas."""

        keywords_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": keywords_prompt}],
            temperature=0.6,
            max_tokens=500
        )
        
        keywords = keywords_response.choices[0].message.content.strip()
        
        # Generate meta description
        meta_prompt = f"""Write a compelling SEO meta description (150-160 characters) for a blog post about: {topic}

Make it engaging and include relevant keywords. Return only the meta description."""

        meta_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": meta_prompt}],
            temperature=0.7,
            max_tokens=200
        )
        
        meta_description = meta_response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'titles': titles,
            'content': blog_content,
            'keywords': keywords,
            'meta_description': meta_description
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Check if API key is set
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️  WARNING: GROQ_API_KEY environment variable not set!")
        print("Please set it before running: export GROQ_API_KEY='your-api-key-here'")
    
    app.run(debug=True, port=5000)