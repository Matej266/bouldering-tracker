from progress import hardest_send, sends_per_session, attempts_by_grade
from sessions import get_session, log_session
from locations import get_locations
from climbs import log_climb, get_climbs

def log_climbs(session_id):
    while True:
        print("\n== Log a New Climb ==")
        print("Select grade:")
        print("1. 5")
        print("2. 6A")
        print("4. 6B")
        print("6. 6C")
        print("...")
        grade_id = int(input("\n -> ").strip())
        tries = int(input("Number of tries: ").strip())
        sent = 1 if input("Sent? (y/n): ").strip().lower() == 'y' else 0
        notes = input("Notes (optional): ").strip() or None
        climb_id = log_climb(session_id, grade_id, tries, sent, notes)
        print("CLimb Logged with ID:", climb_id)
        print("Log another climb for this session? (y/n)")
        if input("\n -> ").strip().lower() != 'y':
            break

def handle_log_session():
    print("\n== Log a New Session ==")
    print("Select location:")
    locations = get_locations()
    for loc in locations:
        print(f"{loc['id']}. {loc['name']}")
    location_id = int(input("\n -> ").strip())
    duration_min = int(input("Duration (minutes): ").strip())
    feel = int(input("Feel (1-5): ").strip())
    notes = input("Notes (optional): ").strip() or None
    session_id = log_session(location_id, duration_min, feel, notes)
    print(f"Session ID: {session_id}")
    print("Now log climbs for this session.")
    log_climbs(session_id)
    
def handle_view_session():
    print("\n== Past Sessions ==")
    sessions = get_session()
    for s in sessions:
        print(f"#{s['id']}| Location: {s['location_name']}| Date: {s['date']}| Duration: {s['duration_min']} min| Feel: {s['feel']}| Notes: {s['notes']}")
    print("\nView climbs for a session? (y/n)")
    if input("\n -> ").strip().lower() == 'y':
        session_id = input("Enter session ID: ").strip()
        climbs = get_climbs(session_id)
        for c in climbs:
            print(f"#{c['id']}| Grade: {c['grade_label']}| Sent: {'Yes' if c['sent'] else 'No'}| Tries: {c['tries']}| Notes: {c['notes']}")
            
def handle_view_progress():
    print("\n== Progress ==")
    print("Hardest Send:", hardest_send())
    print("\nSends per Session:")
    for s in sends_per_session():
        print(f"Session #{s['id']} on {s['date']} at {s['name']}: {s['sends']} sends")
    print("\nAttempts by Grade:")
    for a in attempts_by_grade():
        print(f"Grade {a['label']}: {a['total_attempts']} attempts, {a['total_sends']} sends") 

while True:
    print("\n ==Bouldering Tracker==")
    print("1. Log a new session")
    print("2. Log climbs for a session")
    print("3. View past sessions")
    print("4. View progress")
    print("5. Exit")
    
    choice = input("\n -> ").strip()
    
    if choice == '1':
        handle_log_session()
    elif choice == '2':        
        session_id = int(input("Enter session ID to log climbs for: ").strip())
        log_climbs(session_id)
    elif choice == '3':
        handle_view_session()
    elif choice == '4':
        handle_view_progress()
    elif choice == '5':
        print('exit')
        break
    else:
        print("Invalid option, please try again.")