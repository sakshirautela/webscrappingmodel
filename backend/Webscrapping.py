from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)
CORS(app)

@app.route('/api/data/<path:url>', methods=['GET'])
def get_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        possible_selectors = [
            ('div', {'class': 'article-content'}),
            ('div', {'id': 'articleContent'}),
            ('div', {'class': 'text'}),
            ('div', {'class': 'content'}),
            ('div', {'class': 'entry-content'}),
            ('div', {'class': 'article--viewer_content'}),
            ('main', {}),
            ('section', {}),
            ('article', {})
        ]

        content_div = None
        for tag, attrs in possible_selectors:
            content_div = soup.find(tag, attrs) if attrs else soup.find(tag)
            if content_div:
                break

        if content_div:
            paragraphs = [
                p.get_text(strip=True) 
                for p in content_div.find_all('p') 
                if p.get_text(strip=True)
            ]
            return jsonify({"content": paragraphs})
        else:
            print("\n--- DEBUG: Could not find matching content ---")
            print(soup.prettify()[:2000]) 
            print("--- END DEBUG ---\n")
            return jsonify({"error": "Content not found"}), 404

    finally:
        driver.quit()


if __name__ == '__main__':
    app.run(debug=True)
