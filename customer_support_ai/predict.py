import pickle

sentiment_model = pickle.load(open("models/sentiment.pkl","rb"))
issue_model = pickle.load(open("models/issue.pkl","rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl","rb"))

urgent_words = ["not working","down","failed","error","urgent","slow","disconnect","problem","refund"]
greetings = ["hi", "hello", "hey", "good morning", "good evening"]
thanks_words = ["thanks", "thank you", "thx"]
bye_words = ["bye", "goodbye", "see you"]

def analyze(text):
    text_lower = text.lower()

    # Greeting handling
    if any(g in text_lower for g in greetings):
        return "neutral", "general", "Normal", "Hello! How can I help you today?"

    if any(t in text_lower for t in thanks_words):
        return "positive", "general", "Normal", "You're welcome! I'm glad I could help."

    if any(b in text_lower for b in bye_words):
        return "neutral", "general", "Normal", "Goodbye! Have a great day."

    # ML prediction
    vec = vectorizer.transform([text])
    sentiment = sentiment_model.predict(vec)[0]
    issue = issue_model.predict(vec)[0]

    # Urgency detection
    urgency = "High" if any(w in text_lower for w in urgent_words) else "Normal"

    reply = generate_reply(issue, urgency, text)

    return sentiment, issue, urgency, reply

def generate_reply(issue, urgency, text):
    t = text.lower()

    if issue == "billing":
        if "refund" in t:
            return "Your refund request has been registered. Our billing team will process it shortly."
        if "extra" in t or "charged" in t:
            return "We have noticed an extra charge issue. Our billing department will verify and correct it."
        if "invoice" in t or "bill" in t:
            return "Your billing details are being reviewed. You will receive an updated invoice soon."
        return "Your billing issue is under review."

    if issue == "network":
        if "slow" in t:
            return "We are checking slow internet in your area. Our network team is working on it."
        if "disconnect" in t:
            return "Your connection drop issue has been noted. We are fixing it."
        if "not working" in t or "down" in t:
            return "Your network outage has been marked urgent. Our engineers are resolving it."
        return "We are investigating your network problem."

    if issue == "payment":
        if "failed" in t:
            return "Your payment failure has been detected. Please try again after some time."
        if "debited" in t:
            return "Your amount deduction is being checked. We will update you shortly."
        return "Your payment issue is being processed."

    if urgency == "High":
        return "Your issue has been marked urgent. Our support team will contact you shortly."

    return "Thank you for contacting customer support. We will assist you soon."
