Clipwise project
<img width="1440" alt="Screenshot 2024-12-31 at 2 15 54 AM" src="https://github.com/user-attachments/assets/058f399d-697d-4479-b06f-172fcc93adc8" />
<img width="1425" alt="image" src="https://github.com/user-attachments/assets/6062e537-5ff7-4bfb-9134-050a6705f626" />
<img width="1425" alt="Screenshot 2024-12-31 at 2 47 59 AM" src="https://github.com/user-attachments/assets/c658c9b2-9135-4829-98af-517b5771ebdd" />
<img width="1425" alt="Screenshot 2024-12-31 at 2 48 45 AM" src="https://github.com/user-attachments/assets/4ca45255-3c91-4bc5-8445-339718e8f2ef" />



Setup for the project
1. Clone the github repository
2. Set up a virtual environment using command ( python3 -m venv env ) -> this will create a virtual environment inside the videoscipt folder
3. Install all the requirements by runnig the following commands:
     -> cd backend
     -> pip install -r requirements.txt
   all the requirements will be installed using this command
4. There is an extra set up for pytesseract library for the extraction of text from the pdf documents. Steps for that are given below
   In the terminal
   
   ->brew install tesseract
   ->which tesseract (if the path is /usr/local/bin/tesseract)

   ->add the path /user/local/bin to the file using

   ->nano ~/.zshrc
   ->export PATH=$PATH:/user/local/bin (change the path accordingly)
   
6. run the command if necessary -> (python manage.py migrate)
7. add api key in the folder projectfolder(videoscript)->backend->home->utils.py (line no 7)



Features
1. Prompt Input
Users can enter a prompt in a text area to generate a script. This prompt is used to get an AI-generated response, which can be displayed and saved.
The prompt field is reset on the first load (when the server is restarted) and can be saved for future sessions using localStorage.
2. File Upload
Users can upload files (e.g., .txt, .pdf, and images) via a file input field-> users can see the data extracted from the files
The uploaded files are sent to the backend for processing, and the results are displayed on the page.
3. External Link
A field for users to input external links is available.
This link is stored in localStorage and will persist across sessions, automatically repopulating the field on subsequent visits.
4. Message Box
A message box is displayed if there is a relevant message to show (for example, after processing a prompt).
The box is hidden during the first load but can be visible for subsequent loads with the appropriate message.
5. Generate Script
When the user clicks the "Generate Script" button, the AI generates a script based on the prompt.
The generated script can be displayed on the page.
6. Save and Download Script
After the script is generated, users can save it and download it as a PDF.
7. Persistent Data Storage
The input fields for prompt and external link are saved in localStorage, allowing the values to persist across page refreshes.
On the first page load (e.g., after the server is restarted), the fields are reset to null values to give the user a fresh start.
8. New Script Button
A "New Script" button is always visible in the top-right corner, even after scrolling, allowing users to reset and start generating a new script.
