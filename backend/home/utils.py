import requests
from bs4 import BeautifulSoup
import os
import openai
import requests
from bs4 import BeautifulSoup
xaiapikey=" "
def fetch_link_metadata_and_content(external_link):
    # Default return values
    result = {
        'title': "",
        'description': "",
        'content': ""
    }

    # Check if the external link starts with http or https
    if not (external_link.startswith('http://') or external_link.startswith('https://')):
        return result  # Return empty strings if the URL is not valid

    try:
        # Fetch the page with a timeout of 10 seconds
        response = requests.get(external_link, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract metadata
        result['title'] = soup.title.string if soup.title else ""
        
        # Look for the meta description tag
        description = soup.find('meta', attrs={'name': 'description'})
        result['description'] = description['content'] if description else ""

        # Extract meaningful content (e.g., first 3 paragraphs)
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        result['content'] = " ".join(paragraphs[:3])  # Limit to the first 3 paragraphs

    except requests.exceptions.RequestException:
        # In case of any error (like a bad URL, no response, etc.), return empty values
        pass

    return result


def api_response(prompt,title,desc,content):
    XAI_API_KEY = xaiapikey
    openai.api_key = XAI_API_KEY
    openai.api_base = "https://api.x.ai/v1"
    client = openai.OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
    )
    user_message = f"Prompt: {prompt}"
    if content:  # Only include content if it's not empty
        user_message += f"\n Additional Content: {content}"
    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
            {"role": "user", "content": user_message },
        ],
    )   
    return completion.choices[0].message.content
