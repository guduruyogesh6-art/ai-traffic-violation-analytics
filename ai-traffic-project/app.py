import time
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

from ai_engine import TrafficAI

ai = TrafficAI()

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Traffic Analyzer",
    page_icon="🚦",
    layout="wide"
)

# ---------------- LANGUAGE SELECTOR ---------------- #
language = st.sidebar.selectbox(
    "🌐 Select Language",
    ["English", "Telugu", "Hindi"]
)

# ---------------- TRANSLATIONS ---------------- #
translations = {
    "English": {
        "title": "🚦 AI-Powered Traffic Analyzer",
        "subtitle": "Real-Time Traffic Monitoring & Violation System",
        "navigation": "Navigation",

        "dashboard": "Dashboard",
        "add_vehicle": "Add Vehicle",
        "add_violation": "Add Violation",
        "view_data": "View Data",
        "live_ai_detection": "Live AI Detection",

        "vehicles": "Vehicles",
        "violations": "Violations",
        "fines": "Fines",

        "violation_breakdown": "Violation Breakdown",
        "traffic_status": "Traffic Status",
        "ai_insights": "AI Insights",

        "vehicle_records": "Vehicle Records",
        "violation_records": "Violation Records",

        "select_vehicle": "Select Vehicle Type",
        "vehicle_number": "Vehicle Number",
        "violation_type": "Violation Type",
        "fine_amount": "Fine Amount",

        "save_violation": "Save Violation",
        "violation_saved": "Violation Recorded Successfully!",

        "smooth": "🟢 Smooth Traffic Flow",
        "medium": "🟡 Medium Traffic",
        "heavy": "🔴 Heavy Traffic",
        "normal": "Traffic behavior is normal 👍",

        "start_detection": "Start AI Detection",
        "live_title": "Live AI Traffic Detection"
    },

    "Telugu": {
        "title": "🚦 AI ఆధారిత ట్రాఫిక్ విశ్లేషకుడు",
        "subtitle": "రియల్-టైమ్ ట్రాఫిక్ మానిటరింగ్ & ఉల్లంఘన వ్యవస్థ",
        "navigation": "నావిగేషన్",

        "dashboard": "డాష్‌బోర్డ్",
        "add_vehicle": "వాహనం జోడించు",
        "add_violation": "ఉల్లంఘన జోడించు",
        "view_data": "డేటా చూడండి",
        "live_ai_detection": "లైవ్ AI గుర్తింపు",

        "vehicles": "వాహనాలు",
        "violations": "ఉల్లంఘనలు",
        "fines": "జరిమానాలు",

        "violation_breakdown": "ఉల్లంఘనల విభజన",
        "traffic_status": "ట్రాఫిక్ స్థితి",
        "ai_insights": "AI సూచనలు",

        "vehicle_records": "వాహన రికార్డులు",
        "violation_records": "ఉల్లంఘన రికార్డులు",

        "select_vehicle": "వాహన రకం ఎంచుకోండి",
        "vehicle_number": "వాహన నంబర్",
        "violation_type": "ఉల్లంఘన రకం",
        "fine_amount": "జరిమానా మొత్తం",

        "save_violation": "ఉల్లంఘన సేవ్ చేయండి",
        "violation_saved": "ఉల్లంఘన విజయవంతంగా నమోదు చేయబడింది!",

        "smooth": "🟢 సాఫీ ట్రాఫిక్ ప్రవాహం",
        "medium": "🟡 మధ్యస్థ ట్రాఫిక్",
        "heavy": "🔴 భారీ ట్రాఫిక్",
        "normal": "ట్రాఫిక్ ప్రవర్తన సాధారణంగా ఉంది 👍",

        "start_detection": "డిటెక్షన్ ప్రారంభించండి",
        "live_title": "లైవ్ AI ట్రాఫిక్ గుర్తింపు"
    },

    "Hindi": {
        "title": "🚦 AI ट्रैफिक विश्लेषक",
        "subtitle": "रीयल-टाइम ट्रैफिक मॉनिटरिंग और उल्लंघन सिस्टम",
        "navigation": "नेविगेशन",

        "dashboard": "डैशबोर्ड",
        "add_vehicle": "वाहन जोड़ें",
        "add_violation": "उल्लंघन जोड़ें",
        "view_data": "डेटा देखें",
        "live_ai_detection": "लाइव AI डिटेक्शन",

        "vehicles": "वाहन",
        "violations": "उल्लंघन",
        "fines": "जुर्माना",

        "violation_breakdown": "उल्लंघन विवरण",
        "traffic_status": "ट्रैफिक स्थिति",
        "ai_insights": "AI इनसाइट्स",

        "vehicle_records": "वाहन रिकॉर्ड",
        "violation_records": "उल्लंघन रिकॉर्ड",

        "select_vehicle": "वाहन प्रकार चुनें",
        "vehicle_number": "वाहन नंबर",
        "violation_type": "उल्लंघन प्रकार",
        "fine_amount": "जुर्माना राशि",

        "save_violation": "उल्लंघन सेव करें",
        "violation_saved": "उल्लंघन सफलतापूर्वक दर्ज किया गया!",

        "smooth": "🟢 साफ ट्रैफिक प्रवाह",
        "medium": "🟡 मध्यम ट्रैफिक",
        "heavy": "🔴 भारी ट्रैफिक",
        "normal": "ट्रैफिक व्यवहार सामान्य है 👍",

        "start_detection": "AI डिटेक्शन शुरू करें",
        "live_title": "लाइव AI ट्रैफिक डिटेक्शन"
    }
}

t = translations[language]

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("traffic.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_type TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_no TEXT,
    violation_type TEXT,
    fine_amount INTEGER
)
""")

conn.commit()

# ---------------- HEADER ---------------- #
st.title(t["title"])
st.markdown(t["subtitle"])

# ---------------- SIDEBAR ---------------- #
menu = st.sidebar.radio(
    t["navigation"],
    [
        t["dashboard"],
        t["add_vehicle"],
        t["add_violation"],
        t["view_data"],
        t["live_ai_detection"]
    ]
)

# ---------------- DASHBOARD ---------------- #
if menu == t["dashboard"]:

    vehicle_count = cursor.execute(
        "SELECT COUNT(*) FROM vehicles"
    ).fetchone()[0]

    violation_count = cursor.execute(
        "SELECT COUNT(*) FROM violations"
    ).fetchone()[0]

    total_fines = cursor.execute(
        "SELECT COALESCE(SUM(fine_amount),0) FROM violations"
    ).fetchone()[0]

    # Local AI Inferencing
    traffic_prediction = ai.predict_traffic(
        vehicle_count,
        violation_count
    )

    risk_prediction = ai.risk_level(
        violation_count
    )

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(f"🚗 {t['vehicles']}", vehicle_count)
    col2.metric(f"🚨 {t['violations']}", violation_count)
    col3.metric(f"💰 {t['fines']}", f"₹{total_fines}")

    # AI Predictions
    st.subheader("🤖 Local AI Prediction")

    st.info(f"Traffic Prediction: {traffic_prediction}")
    st.info(f"Risk Level: {risk_prediction}")

    # Violation Chart
    st.subheader(t["violation_breakdown"])

    vio_df = pd.read_sql_query("""
        SELECT violation_type, COUNT(*) as count
        FROM violations
        GROUP BY violation_type
    """, conn)

    if not vio_df.empty:
        fig = px.pie(
            vio_df,
            names="violation_type",
            values="count"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Traffic Status
    st.subheader(t["traffic_status"])

    if vehicle_count < 20:
        st.success(t["smooth"])
    elif vehicle_count < 50:
        st.warning(t["medium"])
    else:
        st.error(t["heavy"])

    # AI Insights
    st.subheader(t["ai_insights"])

    if violation_count > 10:
        st.error("🚨 High violation zone detected")
    elif violation_count > 5:
        st.warning("⚠️ Monitor area closely")
    else:
        st.success(t["normal"])

# ---------------- ADD VEHICLE ---------------- #
elif menu == t["add_vehicle"]:

    st.subheader(t["add_vehicle"])

    vehicle_type = st.selectbox(t["select_vehicle"], ["Car", "Bike", "Bus", "Truck"])

    if st.button("Add Vehicle"):
        cursor.execute("INSERT INTO vehicles(vehicle_type) VALUES(?)", (vehicle_type,))
        conn.commit()
        st.success("Vehicle Added Successfully!")

# ---------------- ADD VIOLATION ---------------- #
elif menu == t["add_violation"]:

    st.subheader(t["add_violation"])

    vehicle_no = st.text_input(t["vehicle_number"])

    violation_type = st.selectbox(
        t["violation_type"],
        ["Signal Jumping", "Over Speeding", "Wrong Side", "No Helmet", "No Seatbelt"]
    )

    fine_map = {
        "Signal Jumping": 1000,
        "Over Speeding": 1500,
        "Wrong Side": 2000,
        "No Helmet": 500,
        "No Seatbelt": 500
    }

    fine = fine_map[violation_type]

    st.info(f"{t['fine_amount']}: ₹{fine}")

    if st.button(t["save_violation"]):

        cursor.execute("""
            INSERT INTO violations(vehicle_no, violation_type, fine_amount)
            VALUES (?, ?, ?)
        """, (vehicle_no, violation_type, fine))

        conn.commit()
        st.success(t["violation_saved"])

# ---------------- VIEW DATA ---------------- #
elif menu == t["view_data"]:

    st.subheader(t["vehicle_records"])
    vehicles = pd.read_sql_query("SELECT * FROM vehicles", conn)
    st.dataframe(vehicles, use_container_width=True)

    st.subheader(t["violation_records"])
    violations = pd.read_sql_query("SELECT * FROM violations", conn)
    st.dataframe(violations, use_container_width=True)

# ---------------- LIVE AI ---------------- #
elif menu == t["live_ai_detection"]:

    st.title("🚦 Real-Time CCTV AI Detection")

    st.warning("Use browser camera (works in cloud)")

    img = st.camera_input("Capture Vehicle Image")

    if img is not None:
        st.image(img)

        st.success("AI Analysis Running...")

        st.info("Vehicles detected: 2 (demo)")
        st.info("No violation detected (demo)")
