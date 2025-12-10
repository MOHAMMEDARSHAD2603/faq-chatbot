from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from model import FAQMatcher, load_faqs

app = Flask(__name__)
CORS(app)

# Load FAQs from JSON
faqs = load_faqs("faqs.json")
matcher = FAQMatcher(faqs)

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})

@app.route("/ask", methods=["POST"])
def ask():
    """Handle user questions and return best match."""
    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "question required"}), 400

    # best_match returns (question, answer, category, score)
    best_q, best_a, best_cat, score = matcher.best_match(question)

    if score < 0.15:  # threshold tuning
        return jsonify({
            "answer": "❌ Sorry, I only answer questions from our FAQ list. "
                      "👉 Click 'View All FAQs' to see them.",
            "matched_question": None,
            "category": None,
            "score": score
        })

    return jsonify({
        "answer": best_a,
        "matched_question": best_q,
        "category": best_cat,
        "score": score
    })

@app.route("/faqs", methods=["GET"])
def get_faqs():
    """
    Return FAQs.
    - If ?category= is provided → return filtered FAQs.
    - If no category → return all FAQs.
    """
    category = request.args.get("category")
    if category:
        filtered = [faq for faq in faqs if category.lower() in faq["category"].lower()]
        return jsonify(filtered)
    return jsonify(faqs)

@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Collect feedback from chatbot (Yes/No).
    Stores feedback in a simple text file for now.
    """
    data = request.get_json(force=True)
    feedback_value = data.get("feedback")
    answer_text = data.get("answer")

    # Save feedback to a log file
    with open("feedback_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{feedback_value} | {answer_text}\n")

    return jsonify({"status": "saved", "feedback": feedback_value})

@app.route("/chat")
def chat():
    """Serve chatbot frontend."""
    return send_from_directory(".", "chatbot.html")

if __name__ == "__main__":
    # 0.0.0.0 exposes to LAN; change to 127.0.0.1 if you want local only
    app.run(host="0.0.0.0", port=5000)