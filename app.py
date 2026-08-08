
import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="FAQ Assistant Pro",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

FAQ_DATA = [
    ("What is your return policy?", "You can return eligible products within 30 days of delivery. The item should be unused and in its original condition."),
    ("How can I track my order?", "Open your Orders page and select the order you want to track. The latest shipping status and tracking details will be displayed there."),
    ("How do I cancel my order?", "You can cancel an order before it is shipped by opening the order details and selecting Cancel Order."),
    ("How can I reset my password?", "Select Forgot Password on the login page, enter your registered email address, and follow the reset link."),
    ("How do I create an account?", "Click Sign Up, enter your basic details and email address, create a password, and complete the verification step."),
    ("What payment methods are accepted?", "Common payment methods include credit cards, debit cards, UPI and online banking. Available options can vary by region."),
    ("How long does delivery take?", "Standard delivery usually takes 3 to 7 business days, depending on the destination and product."),
    ("Can I change my delivery address?", "If the order has not shipped, contact support as soon as possible to request an address change."),
    ("How can I contact customer support?", "You can contact customer support through the Help or Contact Us section."),
    ("Is my personal information secure?", "Use a strong password and keep your account credentials private. Applications should protect personal data using appropriate security controls."),
    ("Can I get a refund?", "Refunds are issued for eligible returned or cancelled orders according to the refund policy. Processing time can depend on the payment method."),
    ("How long does a refund take?", "After a refund is approved, it can take several business days to appear in your original payment account."),
    ("Do you offer cash on delivery?", "Cash on delivery may be available for selected products and locations. Availability is shown during checkout."),
    ("Can I change my payment method after ordering?", "Payment methods generally cannot be changed after an order is placed. If the order is still cancellable, you can cancel and place a new order."),
    ("What should I do if my order arrives damaged?", "Take photos of the damaged package or product and contact customer support as soon as possible with your order details."),
    ("What should I do if I receive the wrong product?", "Contact customer support with your order number and photos of the received product. Support can guide you through replacement or return options."),
    ("Can I exchange a product?", "Eligible products can be exchanged according to the exchange policy. The product should normally be unused and in its original condition."),
    ("Do I need an account to place an order?", "Some services allow guest checkout, while others require an account. Creating an account makes order tracking and support easier."),
    ("How do I update my profile information?", "Open your account or profile settings, edit the required information, and save the changes."),
    ("How do I change my password?", "Open Account Settings, choose Security or Change Password, enter the required information, and save the new password."),
    ("Why is my payment failing?", "Check your payment details, available balance, bank restrictions, and internet connection. If the problem continues, try another supported payment method."),
    ("Why has my order not shipped yet?", "Orders can take additional processing time because of stock availability, verification, weekends, or holidays. Check your order status for the latest update."),
    ("What does order processing mean?", "Order processing means your order has been received and is being prepared before shipment."),
    ("Can I cancel an order after it has shipped?", "Usually an order cannot be cancelled after shipment. You may need to receive it and use the applicable return process."),
    ("How do I find my order number?", "Your order number is normally shown in the order confirmation email and in the Orders section of your account."),
    ("What countries do you deliver to?", "Delivery availability depends on the service and product. Enter your address during checkout to check whether delivery is available."),
    ("Are there additional delivery charges?", "Delivery charges depend on the destination, order value, delivery method, and applicable promotions."),
    ("How can I report a problem with an order?", "Open the order details and contact support using the Help or Contact Us option. Include your order number and a short description of the problem."),
    ("What is an FAQ chatbot?", "An FAQ chatbot matches a user's question with the most relevant frequently asked question and returns its predefined answer."),
    ("How does this chatbot find an answer?", "This application converts FAQ questions into TF-IDF vectors and uses cosine similarity to find the most similar FAQ."),
    ("What is TF-IDF?", "TF-IDF is a text representation technique that gives importance to words based on how frequently they appear in a document compared with the whole collection."),
    ("What is cosine similarity?", "Cosine similarity measures how similar two text vectors are by comparing the angle between them. A higher value generally means greater similarity."),
    ("Does this chatbot use artificial intelligence?", "It uses a natural language processing technique for text similarity. It is a lightweight retrieval-based chatbot rather than a generative AI model."),
    ("Can I add my own FAQs?", "Yes. Replace or extend the FAQ_DATA list in app.py with your own questions and answers."),
    ("Does the chatbot require an API key?", "No. This version runs locally using Python and scikit-learn and does not require a paid translation or AI API key."),
]

THEMES = {
    "Ocean Blue": {
        "bg": "#eef6ff", "card": "#ffffff", "text": "#10233f", "muted": "#5c6f89",
        "primary": "#2563eb", "secondary": "#0ea5e9", "border": "#d6e4f5",
        "input": "#ffffff", "answer": "#f8fbff"
    },
    "Midnight Purple": {
        "bg": "#0b1020", "card": "#141b2d", "text": "#f5f7ff", "muted": "#aab4ca",
        "primary": "#8b5cf6", "secondary": "#6366f1", "border": "#2c3753",
        "input": "#0f172a", "answer": "#18223a"
    },
    "Emerald": {
        "bg": "#effcf7", "card": "#ffffff", "text": "#10382c", "muted": "#5c756d",
        "primary": "#059669", "secondary": "#10b981", "border": "#cceee2",
        "input": "#ffffff", "answer": "#f5fffb"
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "Ocean Blue"

with st.sidebar:
    st.markdown("## 🎨 Appearance")
    selected_theme = st.selectbox(
        "Choose a theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
    )
    st.session_state.theme = selected_theme

theme = THEMES[st.session_state.theme]

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {theme["bg"]};
        color: {theme["text"]};
    }}
    [data-testid="stHeader"] {{
        background: transparent;
    }}
    [data-testid="stSidebar"] {{
        background: {theme["card"]};
        border-right: 1px solid {theme["border"]};
    }}
    [data-testid="stSidebar"] * {{
        color: {theme["text"]} !important;
    }}
    .block-container {{
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}
    .hero {{
        padding: 30px 32px;
        border-radius: 24px;
        background: linear-gradient(135deg, {theme["primary"]}, {theme["secondary"]});
        color: white;
        box-shadow: 0 18px 45px rgba(37, 99, 235, .18);
        margin-bottom: 24px;
    }}
    .hero h1 {{
        color: white !important;
        font-size: 42px;
        margin: 0 0 8px 0;
        font-weight: 800;
    }}
    .hero p {{
        color: rgba(255,255,255,.92) !important;
        margin: 0;
        font-size: 16px;
    }}
    .section-title {{
        color: {theme["text"]} !important;
        font-size: 20px;
        font-weight: 800;
        margin: 18px 0 8px;
    }}
    label, [data-testid="stWidgetLabel"] p {{
        color: {theme["text"]} !important;
        font-weight: 700 !important;
    }}
    input, textarea {{
        color: {theme["text"]} !important;
        background: {theme["input"]} !important;
        -webkit-text-fill-color: {theme["text"]} !important;
        border-color: {theme["border"]} !important;
        caret-color: {theme["primary"]} !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: {theme["muted"]} !important;
        opacity: 1 !important;
    }}
    [data-baseweb="select"] > div {{
        background: {theme["input"]} !important;
        color: {theme["text"]} !important;
        border-color: {theme["border"]} !important;
    }}
    [data-baseweb="select"] * {{
        color: {theme["text"]} !important;
    }}
    [role="option"] {{
        color: {theme["text"]} !important;
        background: {theme["input"]} !important;
    }}
    .answer-box {{
        padding: 22px;
        border-radius: 18px;
        background: {theme["answer"]};
        border: 1px solid {theme["border"]};
        color: {theme["text"]} !important;
        font-size: 17px;
        line-height: 1.7;
        box-shadow: 0 12px 30px rgba(15, 23, 42, .07);
    }}
    .match-box {{
        margin-top: 12px;
        padding: 12px 15px;
        border-radius: 12px;
        background: {theme["card"]};
        border: 1px solid {theme["border"]};
        color: {theme["muted"]} !important;
        font-size: 13px;
    }}
    .stButton > button {{
        border-radius: 12px !important;
        min-height: 44px !important;
        font-weight: 700 !important;
        border: 1px solid {theme["border"]} !important;
        color: {theme["text"]} !important;
        background: {theme["card"]} !important;
    }}
    .stButton > button:hover {{
        border-color: {theme["primary"]} !important;
        color: {theme["primary"]} !important;
    }}
    [data-testid="stForm"] {{
        background: {theme["card"]};
        border: 1px solid {theme["border"]};
        border-radius: 20px;
        padding: 22px;
    }}
    .info {{
        color: {theme["muted"]};
        font-size: 13px;
        line-height: 1.6;
    }}
    h2, h3, p, li {{
        color: {theme["text"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def build_engine():
    questions = [q for q, _ in FAQ_DATA]
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    matrix = vectorizer.fit_transform(questions)
    return vectorizer, matrix

vectorizer, faq_matrix = build_engine()

def clean_text(text):
    return re.sub(r"\s+", " ", text.lower().strip())

def find_answer(query):
    query_vector = vectorizer.transform([clean_text(query)])
    scores = cosine_similarity(query_vector, faq_matrix)[0]
    index = scores.argmax()
    return FAQ_DATA[index][1], float(scores[index]), FAQ_DATA[index][0]

st.markdown(
    """
    <div class="hero">
        <h1>💬 FAQ Assistant Pro</h1>
        <p>Smart FAQ matching powered by NLP, TF-IDF and cosine similarity.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([2.2, 1])

with left:
    st.markdown('<div class="section-title">Ask your question</div>', unsafe_allow_html=True)
    question = st.text_input(
        "Question",
        value=st.session_state.get("question", ""),
        placeholder="Example: How can I track my order?",
        label_visibility="collapsed",
    )

    c1, c2, c3 = st.columns([1.4, 1, 1])
    with c1:
        ask = st.button("🔎 Find Best Answer", type="primary", use_container_width=True)
    with c2:
        clear = st.button("🗑️ Clear", use_container_width=True)
    with c3:
        random_q = st.button("✨ Example", use_container_width=True)

    if random_q:
        st.session_state["question"] = FAQ_DATA[0][0]
        st.rerun()

    if clear:
        st.session_state["question"] = ""
        st.rerun()

    if ask:
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            answer, score, matched = find_answer(question)
            st.markdown('<div class="section-title">🤖 Chatbot Response</div>', unsafe_allow_html=True)

            if score >= 0.15:
                st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="match-box">🎯 Best matching FAQ: <b>{matched}</b></div>',
                    unsafe_allow_html=True,
                )
                st.write("")
                st.progress(min(score, 1.0), text=f"Similarity confidence: {score:.2f}")
            else:
                st.info("I couldn't find a confident match. Try rephrasing your question or add that FAQ to the dataset.")

with right:
    st.markdown('<div class="section-title">📚 Quick Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="info">Click any question to place it in the search box.</div>', unsafe_allow_html=True)
    for i, (q, _) in enumerate(FAQ_DATA[:12]):
        if st.button(q, key=f"faq_{i}", use_container_width=True):
            st.session_state["question"] = q
            st.rerun()

st.divider()
st.caption(f"Task 2 • {len(FAQ_DATA)} FAQs • TF-IDF + Cosine Similarity • Streamlit")
