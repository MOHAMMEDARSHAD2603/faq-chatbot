FAQ Chatbot Assistant
This is a Flask‑based FAQ chatbot project. It allows users to browse FAQs by category, ask questions, get instant answers, and give feedback. It also has a modern UI with dark mode, a help button, and a welcome message. The project is deployed on Render.

Features
* Category‑based FAQ filtering (Booking, Orders, Payments, Cancellation, Delivery, Facilities, Offers, General)
* Feedback buttons (Yes/No) with logging to a feedback file
* Dark mode toggle and light mode option
* Help button for quick access to all FAQs
* Typing indicator to make responses feel realistic
* Reset/Home button to return to the category view
* Welcome message when users open the chatbot
* Dataset of 100 FAQs stored in faqs.json
* Fully deployed on Render

Tech Stack
* Frontend: HTML, CSS, JavaScript
* Backend: Python (Flask)
* Data: JSON (faqs.json)
* Deployment: Render

Project Structure
* app.py → Flask backend
* faqs.json → FAQ dataset
* templates/chatbot.html → Frontend UI
* static/ → CSS/JS assets (if any)
* feedback_log.txt → Stores user feedback
* requirements.txt → Python dependencies
* README.md → Documentation

Installation (Local Setup)
* Clone the repository.
* Install dependencies using pip install -r requirements.txt.
* Run the app with python app.py.
* Open http://127.0.0.1:5000 in your browser.

Deployment
The chatbot is deployed on Render.
Live demo link:"https://faq-chatbot-5lf5.onrender.com/"

Usage
* Select a category to view FAQs.
* Click a question to see the answer.
* Submit feedback (Yes/No).
* Toggle dark mode or use help/home buttons.

Future Improvements
* Add analytics to track FAQ usage and feedback stats.
* Connect a custom domain for a professional link.
* Add multilingual support.
* Expand the FAQ dataset with user feedback.

Credits
* Built by Mohammed Arshad.R
* CodeAlpha Project, 2025



