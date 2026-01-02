from flask import Flask, render_template, request
from predict import analyze
import database
from datetime import date

database.create_tables()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chat():
    reply = ""

    if request.method == "POST":
        msg = request.form["message"]

        sentiment, issue, urgency, reply = analyze(msg)

        today = date.today().isoformat()

        conn = database.connect()
        c = conn.cursor()
        c.execute(
            "INSERT INTO chats(message, sentiment, issue, urgency, date) VALUES(?,?,?,?,?)",
            (msg, sentiment, issue, urgency, today)
        )
        conn.commit()
        conn.close()

    return render_template("chat.html", reply=reply)

@app.route("/dashboard")
def dashboard():
    conn = database.connect()
    c = conn.cursor()

    c.execute("SELECT sentiment, COUNT(*) FROM chats GROUP BY sentiment")
    sentiment_data = c.fetchall()

    c.execute("SELECT issue, COUNT(*) FROM chats GROUP BY issue")
    issue_data = c.fetchall()

    c.execute("SELECT urgency, COUNT(*) FROM chats GROUP BY urgency")
    urgency_data = c.fetchall()

    c.execute("SELECT date, COUNT(*) FROM chats GROUP BY date")
    trend_data = c.fetchall()

    c.execute("SELECT COUNT(*) FROM chats")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM chats WHERE sentiment='positive'")
    positive = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM chats WHERE sentiment='negative'")
    negative = c.fetchone()[0]

    satisfaction = round((positive / total) * 100, 2) if total > 0 else 0

    c.execute("SELECT message FROM chats")
    texts = [row[0] for row in c.fetchall()]

    from collections import Counter
    words = " ".join(texts).lower().split()
    stopwords = ["the","is","to","and","a","of","my","i","it","for","in","on"]
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    top_keywords = Counter(keywords).most_common(5)

    conn.close()

    return render_template(
        "dashboard.html",
        sentiment_data=sentiment_data,
        issue_data=issue_data,
        urgency_data=urgency_data,
        trend_data=trend_data,
        total=total,
        positive=positive,
        negative=negative,
        satisfaction=satisfaction,
        top_keywords=top_keywords
    )

@app.route("/download")
def download():
    import pandas as pd
    conn = database.connect()
    df = pd.read_sql("SELECT * FROM chats", conn)
    conn.close()

    df.to_csv("customer_report.csv", index=False)
    return "Report downloaded successfully. Check customer_report.csv in your project folder."

app.run(debug=True)
