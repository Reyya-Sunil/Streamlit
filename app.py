import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, timedelta

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="VORTEX | Gym Operating System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Executive SaaS UI Styling (Obsidian & Emerald) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        letter-spacing: -0.011em;
    }

    /* Core Canvas */
    .stApp {
        background-color: #090b10 !important;
        color: #e2e8f0;
    }

    /* Top Header Bar */
    header[data-testid="stHeader"] {
        background: rgba(9, 11, 16, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid #1a202c !important;
    }

    /* Sleek Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #06070a !important;
        border-right: 1px solid #161b26 !important;
    }
    
    /* Metrics / KPI Strip */
    .metric-container {
        background: #0f131c;
        border: 1px solid #1c2433;
        border-radius: 12px;
        padding: 20px 22px;
        position: relative;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-container:hover {
        border-color: #2d3748;
        background: #121722;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
    }
    .metric-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
    }
    .metric-num {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        line-height: 1;
        color: #ffffff;
    }
    .metric-meta {
        font-size: 0.78rem;
        font-weight: 500;
        color: #94a3b8;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Card Panels */
    .surface-panel {
        background: #0f131c;
        border: 1px solid #1c2433;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 24px;
    }
    .surface-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #f8fafc;
        margin: 0 0 6px 0;
    }
    .surface-desc {
        font-size: 0.82rem;
        color: #64748b;
        margin: 0 0 18px 0;
    }

    /* Status Pills */
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
    }
    .pill-active {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .pill-warning {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.25);
    }
    .pill-danger {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }

    /* Professional Button Overrides */
    div.stButton > button:first-child {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.4rem !important;
        transition: all 0.15s ease-in-out !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8 !important;
        border-color: #60a5fa !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
    }

    /* Form Fields */
    div[data-baseweb="input"] {
        background-color: #0a0d14 !important;
        border: 1px solid #1e2638 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #0a0d14 !important;
        border: 1px solid #1e2638 !important;
        border-radius: 8px !important;
    }

    /* Custom Radio Navigation Styling */
    div[data-testid="stRadio"] > div {
        gap: 6px;
    }
    div[data-testid="stRadio"] label {
        background: #0d111a;
        padding: 10px 14px;
        border-radius: 8px;
        border: 1px solid #1a2232;
        width: 100%;
        transition: 0.15s ease;
    }
    div[data-testid="stRadio"] label:hover {
        background: #141a27;
        border-color: #2d3b55;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Database Layer ---
DB_NAME = "vortex_gym.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            plan_name TEXT NOT NULL,
            join_date DATE NOT NULL,
            expiry_date DATE NOT NULL,
            amount_paid REAL NOT NULL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_member(name, phone, email, plan, join_dt, exp_dt, amount, notes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO members (full_name, phone, email, plan_name, join_date, expiry_date, amount_paid, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, email, plan, join_dt, exp_dt, amount, notes))
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM members ORDER BY id DESC", conn)
    conn.close()
    if not df.empty:
        df["join_date"] = pd.to_datetime(df["join_date"]).dt.date
        df["expiry_date"] = pd.to_datetime(df["expiry_date"]).dt.date
    return df

def renew_membership(m_id, new_exp, add_fee):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE members 
        SET expiry_date = ?, amount_paid = amount_paid + ? 
        WHERE id = ?
    """, (new_exp, add_fee, m_id))
    conn.commit()
    conn.close()

def delete_member(m_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM members WHERE id = ?", (m_id,))
    conn.commit()
    conn.close()

init_db()
today = date.today()
df = load_data()

# Dynamic Status Computation
if not df.empty:
    df["days_left"] = (df["expiry_date"] - today).apply(lambda d: d.days)
    def calculate_status(days):
        if days < 0:
            return "Expired"
        elif 0 <= days <= 7:
            return "Expiring Soon"
        return "Active"
    df["status"] = df["days_left"].apply(calculate_status)
else:
    df["days_left"] = []
    df["status"] = []

# Expiry Notification Radar
expired_count = len(df[df["status"] == "Expired"]) if not df.empty else 0
expiring_soon_count = len(df[df["status"] == "Expiring Soon"]) if not df.empty else 0

if "toast_dispatched" not in st.session_state:
    if expired_count > 0:
        st.toast(f"Critical: {expired_count} subscription(s) overdue.", icon="🔴")
    if expiring_soon_count > 0:
        st.toast(f"Renewal Radar: {expiring_soon_count} client(s) due within 7 days.", icon="🟡")
    st.session_state.toast_dispatched = True

# --- 4. Sidebar Controls ---
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 24px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: #2563eb; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; color: #fff;">⚡</div>
                <div>
                    <h3 style="margin: 0; font-size: 1.15rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">VORTEX OS</h3>
                    <div style="font-size: 0.72rem; color: #64748b; font-weight: 500;">GYM OPERATIONS ENGINE</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #475569; letter-spacing: 0.08em; margin-bottom: 8px;'>System Navigation</p>", unsafe_allow_html=True)
    nav_selection = st.radio(
        "Navigation",
        ["Executive Dashboard", "Client Intake", "Member Directory", "Subscription Renewals"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: #0d111a; border: 1px solid #1a2232; border-radius: 10px; padding: 14px;">
            <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Node Health</div>
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;">
                <span style="height: 8px; width: 8px; background-color: #10b981; border-radius: 50%; display: inline-block;"></span>
                <span style="font-size: 0.8rem; font-weight: 600; color: #cbd5e1;">Live • Cloud Node</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. View: Executive Dashboard ---
if nav_selection == "Executive Dashboard":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 1.85rem; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: -0.03em;">Command Center</h1>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.88rem;">Key performance indicators, live headcount, and subscription lifecycle metrics.</p>
        </div>
    """, unsafe_allow_html=True)

    # High-Density KPI Cards
    total_m = len(df)
    active_m = len(df[df["status"] == "Active"]) if not df.empty else 0
    total_rev = df['amount_paid'].sum() if not df.empty else 0.0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-header">
                    <span class="metric-title">Active Capacity</span>
                    <span style="color: #10b981; font-size: 0.85rem;">●</span>
                </div>
                <div class="metric-num" style="color: #10b981;">{active_m}</div>
                <div class="metric-meta"><span>Current active accounts</span></div>
            </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-header">
                    <span class="metric-title">Action Required (7D)</span>
                    <span style="color: #f59e0b; font-size: 0.85rem;">⏳</span>
                </div>
                <div class="metric-num" style="color: #f59e0b;">{expiring_soon_count}</div>
                <div class="metric-meta"><span>Upcoming expirations</span></div>
            </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-header">
                    <span class="metric-title">Overdue Members</span>
                    <span style="color: #ef4444; font-size: 0.85rem;">✕</span>
                </div>
                <div class="metric-num" style="color: #ef4444;">{expired_count}</div>
                <div class="metric-meta"><span>Subscription lapsed</span></div>
            </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-header">
                    <span class="metric-title">Collected Revenue</span>
                    <span style="color: #3b82f6; font-size: 0.85rem;">₹</span>
                </div>
                <div class="metric-num" style="color: #f8fafc;">₹{total_rev:,.0f}</div>
                <div class="metric-meta"><span>From {total_m} enrolled accounts</span></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # Focus Lists
    col_urgent_a, col_urgent_b = st.columns(2)
    with col_urgent_a:
        st.markdown("""
            <div class="surface-panel">
                <div class="surface-title" style="color: #f87171;">⚠️ Lapsed Subscriptions</div>
                <div class="surface-desc">Members whose pass has expired. Prompt renewal required.</div>
            </div>
        """, unsafe_allow_html=True)
        expired_table = df[df["status"] == "Expired"] if not df.empty else pd.DataFrame()
        if expired_table.empty:
            st.info("No expired subscriptions currently.")
        else:
            st.dataframe(
                expired_table[["id", "full_name", "phone", "plan_name", "expiry_date", "days_left"]],
                use_container_width=True,
                hide_index=True
            )

    with col_urgent_b:
        st.markdown("""
            <div class="surface-panel">
                <div class="surface-title" style="color: #fbbf24;">⚡ Expiry Radar (Next 7 Days)</div>
                <div class="surface-desc">Subscriptions reaching maturity shortly.</div>
            </div>
        """, unsafe_allow_html=True)
        expiring_table = df[df["status"] == "Expiring Soon"] if not df.empty else pd.DataFrame()
        if expiring_table.empty:
            st.info("Zero members expiring within the next 7 days.")
        else:
            st.dataframe(
                expiring_table[["id", "full_name", "phone", "plan_name", "expiry_date", "days_left"]],
                use_container_width=True,
                hide_index=True
            )

# --- 6. View: Client Intake (Register Member) ---
elif nav_selection == "Client Intake":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 1.85rem; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: -0.03em;">Member Onboarding</h1>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.88rem;">Enroll a new customer, set membership duration, and record payment.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="surface-panel">', unsafe_allow_html=True)
        with st.form("client_intake_form", clear_on_submit=True):
            r1, r2 = st.columns(2)
            with r1:
                name = st.text_input("Full Name", placeholder="Rahul Varma")
                phone = st.text_input("Phone Number", placeholder="9876543210")
                email = st.text_input("Email Address", placeholder="rahul@example.com")
            with r2:
                plan = st.selectbox(
                    "Membership Tier",
                    ["Standard (1 Month / 30 Days)", "Quarterly (3 Months / 90 Days)", "Semi-Annual (6 Months / 180 Days)", "Annual (12 Months / 365 Days)"]
                )
                start_date = st.date_input("Commencement Date", value=today)

                tier_days = {
                    "Standard (1 Month / 30 Days)": 30,
                    "Quarterly (3 Months / 90 Days)": 90,
                    "Semi-Annual (6 Months / 180 Days)": 180,
                    "Annual (12 Months / 365 Days)": 365
                }
                calc_expiry = start_date + timedelta(days=tier_days[plan])
                expiry_date = st.date_input("Maturity / Expiration Date", value=calc_expiry)

            r3, r4 = st.columns(2)
            with r3:
                fee = st.number_input("Fee Settled (₹)", min_value=0.0, step=100.0, value=2500.0)
            with r4:
                notes = st.text_input("Clinical / Personal Fitness Goals", placeholder="Hypertrophy / Post-rehab shoulder caution")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Complete Intake & Authorize Access")

            if submit:
                if not name.strip() or not phone.strip():
                    st.error("Validation Error: Full Name and Contact Number are mandatory fields.")
                elif expiry_date <= start_date:
                    st.error("Validation Error: Expiry date must chronologically succeed the join date.")
                else:
                    add_member(name.strip(), phone.strip(), email.strip(), plan, start_date, expiry_date, fee, notes)
                    st.success(f"Customer {name} initialized. Access valid through {expiry_date}.")
                    st.session_state.toast_dispatched = False
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. View: Member Directory ---
elif nav_selection == "Member Directory":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 1.85rem; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: -0.03em;">Directory & Roster</h1>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.88rem;">Filter records, review status badges, and purge invalid entries.</p>
        </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No member records located. Use Client Intake to register customers.")
    else:
        # Search & Filter controls
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            query = st.text_input("Search Registry", placeholder="Search by name, contact...")
        with f2:
            status_f = st.selectbox("Status Filter", ["All", "Active", "Expiring Soon", "Expired"])
        with f3:
            plan_f = st.selectbox("Tier Filter", ["All"] + sorted(list(df["plan_name"].unique())))

        view_records = df.copy()

        if query:
            view_records = view_records[
                view_records["full_name"].str.contains(query, case=False, na=False) |
                view_records["phone"].str.contains(query, case=False, na=False)
            ]
        if status_f != "All":
            view_records = view_records[view_records["status"] == status_f]
        if plan_f != "All":
            view_records = view_records[view_records["plan_name"] == plan_f]

        st.caption(f"Showing {len(view_records)} entries")

        # Enterprise Table View
        st.dataframe(
            view_records[[
                "id", "full_name", "phone", "plan_name", 
                "join_date", "expiry_date", "days_left", "status", "amount_paid"
            ]],
            use_container_width=True,
            hide_index=True
        )

        with st.expander("Administrative Purge"):
            del_id = st.number_input("Specify Member ID to remove", min_value=1, step=1)
            if st.button("Purge Entry"):
                delete_member(del_id)
                st.warning(f"Record #{del_id} removed permanently.")
                st.rerun()

# --- 8. View: Subscription Renewals ---
elif nav_selection == "Subscription Renewals":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 1.85rem; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: -0.03em;">Subscription Extensions</h1>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.88rem;">Extend expiring memberships, update fee collections, and re-arm passes.</p>
        </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No members available.")
    else:
        member_lookup = {f"#{row['id']} — {row['full_name']} ({row['phone']})": row['id'] for _, row in df.iterrows()}
        selected_key = st.selectbox("Select Target Account", list(member_lookup.keys()))
        t_id = member_lookup[selected_key]
        target = df[df["id"] == t_id].iloc[0]

        # Account Details Badge strip
        pill_cls = "pill-active" if target["status"] == "Active" else ("pill-warning" if target["status"] == "Expiring Soon" else "pill-danger")
        
        st.markdown(f"""
            <div class="surface-panel" style="margin-top: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="margin: 0; color: #fff;">{target['full_name']}</h3>
                        <p style="margin: 4px 0 12px 0; color: #64748b; font-size: 0.85rem;">Contact: {target['phone']} | Active Plan: {target['plan_name']}</p>
                        <span class="pill {pill_cls}">{target['status']}</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.76rem; color: #64748b; text-transform: uppercase;">Current Maturity</div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 700; color: #cbd5e1;">{target['expiry_date']}</div>
                        <div style="font-size: 0.78rem; color: #94a3b8;">({target['days_left']} days relative)</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("renewal_processing"):
            rn1, rn2 = st.columns(2)
            with rn1:
                extension_block = st.selectbox(
                    "Cycle Extension",
                    ["30 Days (Standard 1 Month)", "90 Days (Quarterly)", "180 Days (Semi-Annual)", "365 Days (Full Year)"]
                )
                renewal_payment = st.number_input("Renewal Payment Received (₹)", min_value=0.0, step=100.0, value=2000.0)

            with rn2:
                # If already expired, base the extension from today; otherwise stack on top of existing maturity
                pivot_date = max(today, target["expiry_date"])
                ext_days = int(extension_block.split()[0])
                computed_new_maturity = pivot_date + timedelta(days=ext_days)
                final_expiry = st.date_input("Adjusted Expiry Date", value=computed_new_maturity)

            confirm_btn = st.form_submit_button("Commit Renewal & Extend Pass")
            if confirm_btn:
                renew_membership(t_id, final_expiry, renewal_payment)
                st.success(f"Account for {target['full_name']} extended until {final_expiry}!")
                st.session_state.toast_dispatched = False
                st.rerun()