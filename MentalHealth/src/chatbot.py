# chatbot.py (rule-based backend for mood prediction)

questions = [
    "On a scale of 1-10, how would you rate your mood today?",
    "What emotion describes how you feel today in one word?",
    "Did you feel stressed or relaxed today?",
    "Did you have enough energy to do your usual tasks today?",
    "Did anything make you feel grateful today?"
]

suggestions = {
    "positive": "It's great that you're feeling good! Keep maintaining your self-care routines and stay connected with your goals.",
    "neutral": "It's okay to have neutral days. Consider taking a short walk, doing a breathing exercise, or journaling your thoughts.",
    "negative": "It seems you might be having a tough time. Consider deep breathing, reaching out to a friend, or taking a short mindfulness break. Remember, it's okay to seek support."
}

# To maintain conversation state across sessions
user_sessions = {}

def get_chatbot_response(user_input, session_id="default"):
    session = user_sessions.get(session_id, {"index": 0, "responses": []})

    if session["index"] < len(questions):
        session["responses"].append(user_input)
        next_question = questions[session["index"]]
        session["index"] += 1
        user_sessions[session_id] = session
        return next_question
    else:
        combined_response = " ".join(session["responses"]).lower()
        if any(word in combined_response for word in ["happy", "good", "great", "relaxed", "calm", "8", "9", "10"]):
            mood = "positive"
        elif any(word in combined_response for word in ["okay", "fine", "neutral", "5", "6", "7"]):
            mood = "neutral"
        else:
            mood = "negative"

        advice = suggestions[mood]
        user_sessions[session_id] = {"index": 0, "responses": []}
        return f"Based on your responses, your mood seems {mood}. Here is a suggestion for you: {advice}"

