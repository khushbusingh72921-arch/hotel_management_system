# app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------------------
# Page config + Pastel CSS
# ---------------------------
st.set_page_config(page_title="Hotel Management", layout="wide", page_icon="🏨")

st.markdown(
    """
    <style>
    body { background-color: #F7FAFC; }
    .card { padding: 18px; border-radius: 12px; background: #FFFFFF; box-shadow: 0 6px 18px rgba(0,0,0,0.06); }
    .metric { padding: 14px; border-radius: 10px; text-align: center; }
    .m1 { background: #EAF8F0; }   /* pastel green */
    .m2 { background: #FFF7E8; }   /* pastel orange */
    .m3 { background: #E9F4FF; }   /* pastel blue */
    .header { font-weight:700; font-size:22px; margin-bottom:6px; }
    .small { color:#666; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Sidebar (menu)
# ---------------------------
st.sidebar.title("🏨 Hotel Management")
menu = st.sidebar.radio("Go to", ["Dashboard", "Bookings", "Rooms", "Customers", "Staff"])

# ---------------------------
# Simple sample data (for dashboard)
# ---------------------------
def random_chart_data():
    return pd.DataFrame({
        "Bookings": np.abs(np.random.randn(20).cumsum()) + 5,
        "Revenue": (np.abs(np.random.randn(20).cumsum()) * 120).astype(int)
    })

# ---------------------------
# DASHBOARD
# ---------------------------
if menu == "Dashboard":
    st.title("📊 Dashboard Overview")
    # KPIs
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric m1"><div class="header">Occupancy</div><div style="font-size:28px;">78%</div><div class="small">Today</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric m2"><div class="header">Total Revenue</div><div style="font-size:28px;">$12,450</div><div class="small">This month</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric m3"><div class="header">Upcoming Check-ins</div><div style="font-size:28px;">14</div><div class="small">Next 24 hrs</div></div>', unsafe_allow_html=True)

    st.markdown("<br/>")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Booking Trend")
    st.line_chart(random_chart_data())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br/>")
    r1, r2 = st.columns([2, 1])
    with r1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Recent Bookings")
        df_recent = pd.DataFrame([
            {"Booking ID": 1001, "Guest": "Aisha", "Room": 204, "Status": "Checked-in"},
            {"Booking ID": 1002, "Guest": "Rahul", "Room": 110, "Status": "Booked"},
            {"Booking ID": 1003, "Guest": "Lina", "Room": 305, "Status": "Checked-out"},
        ])
        st.table(df_recent)
        st.markdown("</div>", unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Quick Actions")
        st.button("New Booking")
        st.button("Add Room")
        st.button("Export CSV")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# BOOKINGS (fully working)
# ---------------------------
elif menu == "Bookings":
    st.title("📝 Bookings")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # initialize storage
    if "bookings" not in st.session_state:
        st.session_state.bookings = []

    st.subheader("Add New Booking")

    # Use a Streamlit form so submit is explicit and works reliably
    with st.form("booking_form", clear_on_submit=False):
        guest = st.text_input("Guest Name")
        check_in = st.date_input("Check-in Date")
        check_out = st.date_input("Check-out Date")
        room_type = st.selectbox("Room Type", ["Single", "Double", "Deluxe", "Suite"])
        notes = st.text_area("Notes (optional)", height=80)
        submit_booking = st.form_submit_button("Add Booking")

    if submit_booking:
        # very basic validation
        if not guest:
            st.error("Please enter guest name.")
        elif check_out < check_in:
            st.error("Check-out date must be the same or after check-in date.")
        else:
            new_booking = {
                "Guest": guest,
                "Check-in": check_in.isoformat(),
                "Check-out": check_out.isoformat(),
                "Room Type": room_type,
                "Notes": notes,
                "Created At": datetime.now().isoformat(timespec="seconds"),
                "Status": "Confirmed"
            }
            st.session_state.bookings.append(new_booking)
            st.success("✅ Booking added successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br/>")
    st.subheader("All Bookings")

    if len(st.session_state.bookings) == 0:
        st.info("No bookings yet. Add one using the form above.")
    else:
        # show bookings table
        df = pd.DataFrame(st.session_state.bookings)
        st.dataframe(df)

        # provide simple actions for selected booking
        st.markdown("---")
        st.write("Manage bookings:")
        sel_index = st.number_input("Booking index (0..N-1) to operate on", min_value=0, max_value=max(0, len(st.session_state.bookings)-1), value=0, step=1)
        action = st.selectbox("Action", ["None", "Delete", "Mark as Checked-in", "Mark as Checked-out"])
        if st.button("Apply"):
            if action == "Delete":
                deleted = st.session_state.bookings.pop(sel_index)
                st.success(f"Deleted booking for {deleted['Guest']}")
            elif action == "Mark as Checked-in":
                st.session_state.bookings[sel_index]["Status"] = "Checked-in"
                st.success("Status updated.")
            elif action == "Mark as Checked-out":
                st.session_state.bookings[sel_index]["Status"] = "Checked-out"
                st.success("Status updated.")
            st.experimental_rerun()

# ---------------------------
# ROOMS
# ---------------------------
elif menu == "Rooms":
    st.title("🛏 Room Management")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    rooms = pd.DataFrame({
        "Room No": [101, 102, 103, 201, 202],
        "Type": ["Single", "Double", "Suite", "Double", "Deluxe"],
        "Status": ["Available", "Occupied", "Available", "Maintenance", "Available"]
    })
    st.table(rooms)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# CUSTOMERS
# ---------------------------
elif menu == "Customers":
    st.title("👤 Customers")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.table(pd.DataFrame([
        {"Name": "Aisha", "Phone": "9876543210"},
        {"Name": "Rahul", "Phone": "9123456780"}
    ]))
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# STAFF
# ---------------------------
elif menu == "Staff":
    st.title("🧑‍💼 Staff")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.table(pd.DataFrame([
        {"Name": "Alex", "Role": "Manager"},
        {"Name": "Nina", "Role": "Receptionist"}
    ]))
    st.markdown("</div>", unsafe_allow_html=True)
