import google.generativeai as genai

genai.configure(api_key="AIzaSyC1hsEEdUYtc33gR5Ml8lpLN_S1DCgGRPI")

def get_chatbot_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        # Add formatting instructions to the prompt
        prompt = f"""Respond in a clear, structured format without markdown. Use bullet points (-) or numbered lists. 
        Avoid symbols like *, **, or #. Question: {user_input}"""
        
        response = model.generate_content(prompt)
        # Remove asterisks and clean up text
        cleaned_response = response.text.replace("*", "").strip()
        return cleaned_response
    except Exception as e:
        return f"Error: {str(e)}"
