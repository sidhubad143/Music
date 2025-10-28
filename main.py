# main.py
from flask import Flask, render_template, request, jsonify
import requests
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

API_URL = "http://47.129.201.23:2020/try"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip()
    streamtype = request.form.get('streamtype', 'audio')  # Default to audio
    vid = "true" if streamtype.lower() == "video" else "false"
    
    if not query:
        return render_template('search.html', error="Please enter a search query.", query=query, streamtype=streamtype)
    
    try:
        params = {"query": query, "vid": vid}
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            return render_template('search.html', error=data["error"], query=query, streamtype=streamtype)
        
        link = data.get("link")
        if not link:
            return render_template('search.html', error="No link found for the query.", query=query, streamtype=streamtype)
        
        # Assume 'link' is a direct playable URL (e.g., mp3/mp4). If it's a Telegram link, you may need to handle download/streaming separately.
        # For demo, we'll use it directly in audio/video tag.
        title = f"Playing: {query}"  # Placeholder title; enhance with API if it returns title
        
        return render_template('search.html', link=link, title=title, query=query, streamtype=streamtype)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        logging.error(error_msg)
        return render_template('search.html', error=error_msg, query=query, streamtype=streamtype)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5050)
