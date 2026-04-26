# Bouldering Tracker

A personal bouldering training tracker built in Python and SQLite, with a terminal CLI for logging sessions and a Streamlit web dashboard for visualising progress over time.

Built as my first real Python project to track my own climbing progress at local gyms in Bratislava and Prague.

---

## Features

- Log bouldering sessions with location, duration, feel rating, and notes
- Log individual climbs per session with grade, tries, sent status, and notes
- View recent sessions and climbs in a clean terminal interface
- Streamlit dashboard with:
  - Personal bests and session statistics
  - Progress over time line chart
  - Attempts and sends broken down by grade
  - Full session and climb editing and deletion

---

## Tech Stack

- **Python**
- **SQLite** — local database
- **Streamlit** — web dashboard
- **Pandas** — data manipulation and DataFrame conversion
- **Plotly** — interactive charts

---

## Project Structure

```
boulder_tracker/
├── app.py          # Streamlit dashboard (viewing and editing data)
├── main.py         # Terminal CLI (logging sessions and climbs)
├── db.py           # Database connection, initialisation, and seeding
├── schema.sql      # SQL schema defining all four tables
├── sessions.py     # Functions for logging and querying sessions
├── climbs.py       # Functions for logging and querying climbs
├── locations.py    # Functions for querying locations
├── grades.py       # Functions for querying grades
└── progress.py     # Statistics and progress query functions
```

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/Matej266/boulder-tracker.git
cd boulder-tracker
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install streamlit pandas plotly
```

**4. Initialise the database**

```bash
python db.py
```

This creates `boulder.db` and seeds the grades table

**5. Run the app**

For the terminal CLI:
```bash
python main.py
```

For the Streamlit dashboard:
```bash
streamlit run app.py
```

---

## Usage

There are two interfaces that work alongside each other:

**Terminal CLI (`main.py`)** — used for data entry. Run this after a session to log what you climbed. The menu walks you through selecting a location, entering session details, and logging individual climbs one by one.

**Streamlit Dashboard (`app.py`)** — used for reviewing and analysing data. Opens in your browser and shows your progress over time, grade breakdowns, and personal bests. Also includes tabs for logging and editing data if you prefer working in the browser.

---

## Database Schema

The database has four tables built around the idea that a climb never exists on its own — it always happened during a session, at a location, and at a specific grade.

| Table | Purpose |
|-------|---------|
| `locations` | Stores gyms and outdoor spots — populated once, referenced by sessions |
| `grades` | Stores the Fontainebleau grade scale with a sort order for correct ranking — populated once, referenced by climbs |
| `sessions` | One row per climbing trip — links to a location |
| `climbs` | One row per boulder problem attempted — links to a session and a grade |

Foreign keys enforce that every climb belongs to a real session and every session belongs to a real location. Grades use a `sort_order` integer column so they can be sorted and compared correctly regardless of their text label.

---

## Possible Future Improvements

- Export session history to CSV
- Grade comparison across different locations (some gyms sandbag grades)
- Streak tracking — consecutive days or weeks with a session logged
- Personal goal setting — set a target grade and track progress toward it
- Session comparison — side by side view of two sessions
- Mobile-friendly interface improvements

---

