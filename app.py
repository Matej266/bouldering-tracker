import streamlit as st
from progress import hardest_send, attempts_by_grade, total_climbs, total_sessions, progress_over_time, sends_per_grade
from sessions import get_sessions, log_session
from locations import get_locations
from climbs import log_climb, get_climbs
from grades import get_grades
import pandas as pd

if 'active_session_id' not in st.session_state:
    st.session_state.active_session_id = None
if 'show_climb_form' not in st.session_state:
    st.session_state.show_climb_form = False

st.title("Bouldering Tracker")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Progress", "Grades","Log", "Add Climbs"])

with tab1:
    st.subheader("Overview")
    st.subheader("Personal Bests")
    
    col1, col2, col3, = st.columns(3)
    with col1:
        st.metric("Hardest Send", hardest_send() or "N/A")
    with col2:
        st.metric("Total Climbs Sent", total_climbs())
    with col3:
        st.metric("Total Sessions", total_sessions())
        
    st.subheader("Recent Sessions")
    sessions = get_sessions()
    df = pd.DataFrame(sessions, columns=['id', 'location_name', 'date', 'duration_min', 'feel', 'notes'])
    st.dataframe(df)

with tab2:
    st.subheader("Progress over Time")
    data = progress_over_time()
    df = pd.DataFrame(data, columns=['date', 'best_sort_order', 'best_grade'])
    st.line_chart(df.set_index("date")['best_sort_order'])
    

with tab3:
    st.subheader("Attempts per Grades")
    data = attempts_by_grade()
    df = pd.DataFrame(data, columns=['label', 'total_attempts', 'total_sends'])
    st.dataframe(df)
    st.subheader("Sends per Grade")
    data = sends_per_grade()
    dt = pd.DataFrame(data, columns=['label', 'total_sends'])
    st.bar_chart(dt.set_index("label"))
    
with tab4:
    if not st.session_state.show_climb_form:
        st.subheader("Log a Session")
        
        locations = get_locations()
        location_names = [loc['name'] for loc in locations]
        location_ids = [loc['id'] for loc in locations]
        
        selected_location = st.selectbox("Location", location_names)
        location_id = location_ids[location_names.index(selected_location)]
        
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, step=5)
        feel = st.slider("How did you feel?", min_value=1, max_value=5, value=3)
        notes = st.text_input("Notes (optional)")
        
        if st.button("Log Session"):
            session_id = log_session(location_id, duration, feel, notes or None)
            st.session_state.active_session_id = session_id
            st.session_state.show_climb_form = True
            st.rerun()
    
    else:
        st.subheader(f"Log Climbs — Session #{st.session_state.active_session_id}")
        st.info("Your session is saved. Now log your climbs below.")
        
        grades = get_grades()
        grade_labels = [g['label'] for g in grades]
        grade_ids = [g['id'] for g in grades]
        
        selected_grade = st.selectbox("Grade", grade_labels)
        grade_id = grade_ids[grade_labels.index(selected_grade)]
        
        tries = st.number_input("Number of tries", min_value=1, max_value=100, step=1)
        sent = st.checkbox("Sent?")
        climb_notes = st.text_input("Notes (optional)", key="climb_notes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Log Climb"):
                log_climb(
                    st.session_state.active_session_id,
                    grade_id,
                    tries,
                    1 if sent else 0,
                    climb_notes or None
                )
                st.success("Climb logged!")
        
        with col2:
            if st.button("Finish Session"):
                st.session_state.active_session_id = None
                st.session_state.show_climb_form = False
                st.rerun()
                
with tab5:
    st.subheader("Add Climbs to a Session")
    
    sessions = get_sessions()
    
    if not sessions:
        st.info("No sessions logged yet. Log a session first.")
    else:
        session_labels = [f"#{s['id']} — {s['date']} — {s['location_name']}" for s in sessions]
        session_ids = [s['id'] for s in sessions]
        
        selected_session = st.selectbox("Select Session", session_labels)
        session_id = session_ids[session_labels.index(selected_session)]
        
        st.divider()
        
        existing_climbs = get_climbs(session_id)
        if existing_climbs:
            st.subheader("Climbs already logged this session")
            df = pd.DataFrame(existing_climbs, columns=['id', 'grade_label', 'tries', 'sent', 'notes'])
            df['sent'] = df['sent'].apply(lambda x: 'Yes' if x else 'No')
            st.dataframe(df)
        else:
            st.info("No climbs logged for this session yet.")
        
        st.divider()
        st.subheader("Log a new climb")
        
        grades = get_grades()
        grade_labels = [g['label'] for g in grades]
        grade_ids = [g['id'] for g in grades]
        
        selected_grade = st.selectbox("Grade", grade_labels, key="add_grade")
        grade_id = grade_ids[grade_labels.index(selected_grade)]
        
        tries = st.number_input("Number of tries", min_value=1, max_value=100, step=1, key="add_tries")
        sent = st.checkbox("Sent?", key="add_sent")
        notes = st.text_input("Notes (optional)", key="add_notes")
        
        if st.button("Log Climb"):
            log_climb(session_id, grade_id, tries, 1 if sent else 0, notes or None)
            st.success("Climb logged!")
            st.rerun()