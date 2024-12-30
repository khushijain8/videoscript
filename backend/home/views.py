import os
import mimetypes
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import json
import json
from django.http import JsonResponse
from home.utils import fetch_link_metadata_and_content
from home.models import Script
from home.utils import api_response
from django.core.paginator import Paginator
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


def index(request, message=None, text=None):
    # Handle file upload and return message and text to the same page
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            # Save the uploaded file
            upload_dir = 'uploads/'
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, uploaded_file.name)

            # Save the file to the server
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Determine file type based on extension or MIME type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            mime_type, _ = mimetypes.guess_type(uploaded_file.name)

            # Handle different file types
            if file_extension == 'txt':
                with open(file_path, 'r') as file:
                    file_text = file.read()
                return render(request, "index.html", {'message': 'Text file uploaded successfully', 'text': file_text})

            elif file_extension == 'pdf' or mime_type == 'application/pdf':
                try:
                    extracted_text = extract_text_from_pdf(file_path)
                    return render(request, "index.html", {'message': 'PDF uploaded and processed successfully', 'text': extracted_text})
                except Exception as e:
                    return render(request, "index.html", {'message': f"Error processing PDF: {str(e)}", 'text': None})

            elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                try:
                    image = Image.open(file_path)
                    ocr_text = pytesseract.image_to_string(image)
                    return render(request, "index.html", {'message': 'Image file uploaded and processed successfully', 'text': ocr_text})
                except Exception as e:
                    return render(request, "index.html", {'message': f"Error processing image: {str(e)}", 'text': None})

            else:
                return render(request, "index.html", {'message': 'Unsupported file type', 'text': None})

        else:
            return render(request, "index.html", {'message': 'No file uploaded', 'text': None})

    # If it's a GET request, just return the empty page
    return render(request, "index.html", {'message': message, 'text': text})


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text += f"\n{text}"
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(image)
            full_text += f"\n{ocr_text}"

    return full_text

  # Import the utility function

def generate_script(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            prompt = data.get('prompt')
            external_link = data.get('external_link')

            # Fetch metadata and content from the external link
            try:
                link_data = fetch_link_metadata_and_content(external_link)
                title = link_data['title']
                description = link_data['description']
                content = link_data['content']
            except ValueError as ve:
                return JsonResponse({'error': str(ve)}, status=400)
            except RuntimeError as re:
                return JsonResponse({'error': str(re)}, status=400)
            # Combine the prompt and extracted content
            generated_script="prompt: "+prompt+"\nresponse by AI: "+api_response(prompt,title,description,content)

            print(generated_script)
            return JsonResponse({'script': generated_script}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def save_script(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data sent from the frontend
            data = json.loads(request.body)
            prompt = data.get('prompt')
            external_link = data.get('externalLink')
            script_content = data.get('script')

            if prompt and script_content:
                # Save the script to the database
                new_script = Script.objects.create(
                    prompt=prompt,
                    external_link=external_link,
                    content=script_content
                )
                return JsonResponse({'success': True, 'script_id': new_script.id})
            else:
                return JsonResponse({'success': False, 'message': 'Missing prompt or script content.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def saved_scripts(request):
    # Fetch all saved scripts
    scripts = Script.objects.all()
    return render(request, 'saved_scripts.html', {'scripts': scripts})