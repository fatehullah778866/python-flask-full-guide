# Project 26: Analytics Dashboard 📊

Welcome to Project 26! This app tracks user actions and displays analytics!

## What is This Project? 🤔

**Analytics Dashboard** = An app for tracking and visualizing user actions!

**Think of it like:**
- **Tracking** = Recording actions
- **Analytics** = Statistics and insights
- **Charts** = Visual representation

**Analytics = Understanding user behavior!**

## What You'll Learn 📚

✅ Event tracking
✅ Data aggregation
✅ Statistics calculation
✅ Chart visualization (Chart.js)
✅ Date filtering
✅ API endpoints

## What This App Does 🎯

1. **Track Events** - Record user actions
2. **Display Statistics** - Show analytics
3. **Visualize Data** - Charts and graphs
4. **Filter by Date** - Date range selection
5. **Top Events** - Most common actions
6. **Real-time Tracking** - Track events via API

**Features:**
- 📊 Analytics dashboard
- 📈 Charts and graphs
- 📅 Date filtering
- 🎯 Event tracking
- 📉 Statistics display
- 🔄 Real-time updates

## Step-by-Step Explanation 📖

### Step 1: Event Tracking
```python
def track_event(user_id, event_type, event_data=None):
    event = Event(user_id=user_id, event_type=event_type)
    db.session.add(event)
    db.session.commit()
```
**What this does:**
- Creates event record
- Saves to database
- Tracks user actions

**Simple explanation:**
- Track = Record
- Event = Action!

### Step 2: Data Aggregation
```python
events_by_type = dict(Counter(event_types))
```
**What this does:**
- Counts events by type
- Creates dictionary
- Groups similar events

**Simple explanation:**
- Count = Add up
- Group = Organize!

### Step 3: Chart Visualization
```python
new Chart(ctx, {
    type: 'bar',
    data: chartData
});
```
**What this does:**
- Creates chart
- Displays data visually
- Uses Chart.js library

**Simple explanation:**
- Chart = Visual graph
- Display = Show data!

## Key Concepts 🎓

### 1. Event Tracking

**What are events?**
- User actions
- Recorded in database
- Used for analytics

**Event Structure:**
- User ID
- Event type
- Event data
- Timestamp

### 2. Data Aggregation

**How it works:**
- Collect events
- Group by type/date
- Count occurrences
- Calculate statistics

### 3. Chart Visualization

**What are charts?**
- Visual representation
- Bar charts
- Line charts
- Pie charts

**Chart.js:**
- JavaScript library
- Easy to use
- Responsive charts

## How to Run 🚀

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Register/Login
2. View analytics dashboard
3. Click test buttons to track events
4. See charts update
5. Filter by date range!

## Files in This Project 📁

```
26-analytics-dashboard/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Dashboard with charts
│   ├── login.html      # Login page
│   └── register.html   # Registration page
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test event tracking
2. ✅ View charts
3. ✅ Understand data aggregation
4. ✅ You've completed 26 projects! 🎉

---

**Congratulations! You've completed 26 projects! 🎉**

