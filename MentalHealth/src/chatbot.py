# chatbot.py - Rule-based backend with mood check, quiz selection, quiz evaluation

questions_mood = [
    "On a scale of 1-10, how would you rate your mood today?",
    "What emotion describes how you feel today in one word?",
    "Did you feel stressed or relaxed today?",
    "Did you have enough energy to do your usual tasks today?",
    "Did anything make you feel grateful today?"
]

questions_stress = [
    "In the last week, how often have you felt unable to control important things in your life? (Never/Sometimes/Often/Very Often)",
    "How often have you felt nervous or stressed?",
    "How often have you felt confident about your ability to handle personal problems?",
    "How often have you felt that things were going your way?",
    "How often have you found you could not cope with all the things you had to do?",
    "How often have you been able to control irritations in your life?",
    "How often have you felt that difficulties were piling up so high that you could not overcome them?",
    "How often have you felt upset because of something that happened unexpectedly?",
    "How often have you felt anger or frustration during the past week?",
    "How often have you felt overwhelmed by your responsibilities?"
]

questions_anxiety = [
    "Feeling nervous, anxious, or on edge?",
    "Not being able to stop or control worrying?",
    "Worrying too much about different things?",
    "Trouble relaxing?",
    "Being so restless that it’s hard to sit still?",
    "Becoming easily annoyed or irritable?",
    "Feeling afraid as if something awful might happen?",
    "Experiencing physical symptoms like sweating, trembling, or a racing heart?",
    "Avoiding situations due to fear or anxiety?",
    "Having difficulty concentrating because of worrying?"
]

questions_depression = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself or that you are a failure?",
    "Trouble concentrating on things?",
    "Moving or speaking slowly or being fidgety/restless?",
    "Thoughts that you would be better off dead or hurting yourself?",
    "Feeling worthless or excessive guilt?"
]

suggestions_mood = {
    "positive": "It's great that you're feeling good! Keep maintaining your self-care routines and stay connected with your goals.",
    "neutral": "It's okay to have neutral days. Consider taking a short walk, doing a breathing exercise, or journaling your thoughts.",
    "negative": "It seems you might be having a tough time. Consider deep breathing, reaching out to a friend, or taking a short mindfulness break. Remember, it's okay to seek support."
}

user_sessions = {}

def get_chatbot_response(user_input, session_id="default"):
    session = user_sessions.get(session_id, {"mode": "mood", "index": 0, "responses": []})

    def evaluate_mood(responses):
        combined = " ".join(responses).lower()
        if any(w in combined for w in ["happy", "good", "great", "relaxed", "calm", "8", "9", "10"]):
            return "positive"
        elif any(w in combined for w in ["okay", "fine", "neutral", "5", "6", "7"]):
            return "neutral"
        else:
            return "negative"

    def quiz_scoring(responses):
        score = 0
        for r in responses:
            r = r.lower()
            if "never" in r:
                score += 0
            elif "sometimes" in r:
                score += 1
            elif "often" in r:
                score += 2
            elif "very often" in r:
                score += 3
            elif "no" in r:
                score += 0
            elif "somewhat" in r:
                score += 1
            elif "yes" in r:
                score += 2
            else:
                score += 1
        return score

    # Mood Check Phase
    if session["mode"] == "mood":
        if session["index"] < len(questions_mood):
            session["responses"].append(user_input)
            question = questions_mood[session["index"]]
            session["index"] += 1
            user_sessions[session_id] = session
            return question
        else:
            mood = evaluate_mood(session["responses"])
            advice = suggestions_mood[mood]
            session["mode"] = "quiz_select"
            session["index"] = 0
            session["responses"] = []
            user_sessions[session_id] = session
            return f"Based on your responses, your mood seems {mood}. Here is a suggestion for you: {advice}\n\nWould you like to take a quiz?\nType 'stress', 'anxiety', 'depression', or 'no'."

    # Quiz Selection Phase
    if session["mode"] == "quiz_select":
        choice = user_input.strip().lower()
        if choice == "stress":
            session["mode"] = "stress"
            session["index"] = 0
            session["responses"] = []
            user_sessions[session_id] = session
            return questions_stress[0]
        elif choice == "anxiety":
            session["mode"] = "anxiety"
            session["index"] = 0
            session["responses"] = []
            user_sessions[session_id] = session
            return questions_anxiety[0]
        elif choice == "depression":
            session["mode"] = "depression"
            session["index"] = 0
            session["responses"] = []
            user_sessions[session_id] = session
            return questions_depression[0]
        elif choice == "no":
            user_sessions[session_id] = {"mode": "done"}
            return "Thank you for checking in with me today. Take care! 🌻"
        else:
            return "Please type 'stress', 'anxiety', 'depression', or 'no' to proceed."

    # Quiz Phases
    if session["mode"] in ["stress", "anxiety", "depression"]:
        quiz_map = {
            "stress": questions_stress,
            "anxiety": questions_anxiety,
            "depression": questions_depression
        }
        session["responses"].append(user_input)
        if session["index"] < len(quiz_map[session["mode"]]):
            question = quiz_map[session["mode"]][session["index"]]
            session["index"] += 1
            user_sessions[session_id] = session
            return question
        else:
            score = quiz_scoring(session["responses"])
            if score <= 10:
                level = "low"
            elif score <= 20:
                level = "moderate"
            else:
                level = "high"
            result = f"Your {session['mode']} level appears to be {level}. Remember this is not a diagnosis, but it may help you reflect on your wellbeing."
            session["mode"] = "quiz_select"
            session["index"] = 0
            session["responses"] = []
            user_sessions[session_id] = session
            return f"{result}\n\nWould you like to take another quiz? Type 'stress', 'anxiety', 'depression', or 'no'."

    # Done
    if session["mode"] == "done":
        return "We have completed today's check-in. Have a peaceful day! 🌼"

    # Default fallback
    return "Something went wrong, please refresh and try again."

