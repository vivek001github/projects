from flask import Flask, request, redirect, render_template, url_for
import random
import string

app = Flask(__name__)

url_mapping = {}

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Route to display the home page where users can input a URL
@app.route('/')
def home():
    return '''
        <h1>URL Shortener</h1>
        <form action="/shorten" method="post">
            <label for="url">Enter URL:</label>
            <input type="text" id="url" name="url" required>
            <button type="submit">Shorten</button>
        </form>
    '''

# Route to create a shortened URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    
    # Check if the long URL is already shortened
    if long_url in url_mapping.values():
        # Find the existing short code
        short_code = [key for key, value in url_mapping.items() if value == long_url][0]
    else:
        # Generate a unique short code and save it in the dictionary
        short_code = generate_short_code()
        while short_code in url_mapping:
            short_code = generate_short_code()
        url_mapping[short_code] = long_url
    
    short_url = request.host_url + short_code
    return f'Short URL is: <a href="{short_url}">{short_url}</a>'

# Route to redirect the short URL to the original long URL
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
