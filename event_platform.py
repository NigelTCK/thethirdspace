# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 19:26:46 2025

@author: Admin
"""
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import random
import calendar
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from streamlit_chat import message
import pytz
import urllib
from icalendar import Calendar, Event

# ============================== DATA STRUCTURES ==============================
categories = {
    "Hobbies": ["Reading", "Board games", "Pottery-making", "Painting"],
    "Food": ["Hawker Fare", "Coffee/Cafe Experiences", "Bars", "Restaurants & Fine Dining"],
    "Physical Activities": ["Gymming/Crossfit", "Outdoor Sports", "Indoor Sports", "Combat Sports"],
    "Nature": ["Hiking", "Bird-watching", "Scenic walks", "Stargazing"]
}

events = {
    "Event A": ["Reading", "Scenic walks"],
    "Event B": ["Board games", "Indoor Sports"],
    "Event C": ["Pottery-making"],
    "Event D": ["Painting", "Coffee/Cafe Experiences"],
    "Event E": ["Hawker Fare"],
    "Event F": ["Bars", "Restaurants & Fine Dining"],
    "Event G": ["Gymming/Crossfit"],
    "Event H": ["Outdoor Sports", "Hiking"],
    "Event I": ["Combat Sports"],
    "Event J": ["Bird-watching"],
    "Event K": ["Stargazing"],
    "Event L": ["Indoor Sports"],
    "Event M": ["Coffee/Cafe Experiences", "Scenic walks"],
    "Event N": ["Restaurants & Fine Dining"],
    "Event O": ["Hiking", "Stargazing"],
    "Event P": ["Board games", "Bars"]
}

event_details = {
    "Event A": {
        "date": datetime(2025, 6, 15, 18, 0),  # June 15, 2025 6:00 PM
        "duration": 2,
        "description": "Guided reading session followed by scenic nature walk"
    },
    "Event B": {
        "date": datetime(2025, 6, 20, 14, 30),  # June 20, 2:30 PM
        "duration": 3,
        "description": "Board games championship with indoor sports activities"
    },
    "Event C": {
        "date": datetime(2025, 6, 25, 10, 0),  # June 25, 10:00 AM
        "duration": 2.5,
        "description": "Beginner-friendly pottery making workshop"
    },
    "Event D": {
        "date": datetime(2025, 6, 28, 15, 0),  # June 28, 3:00 PM
        "duration": 3,
        "description": "Art jamming session with café experience"
    },
    "Event E": {
        "date": datetime(2025, 7, 2, 11, 30),  # July 2, 11:30 AM
        "duration": 2,
        "description": "Hawker food tasting tour with local specialties"
    },
    "Event F": {
        "date": datetime(2025, 7, 5, 19, 0),  # July 5, 7:00 PM
        "duration": 4,
        "description": "Premium bar-hopping and fine dining experience"
    },
    "Event G": {
        "date": datetime(2025, 7, 8, 7, 0),  # July 8, 7:00 AM
        "duration": 1.5,
        "description": "High-intensity crossfit bootcamp session"
    },
    "Event H": {
        "date": datetime(2025, 7, 12, 8, 0),  # July 12, 8:00 AM
        "duration": 4,
        "description": "Outdoor sports day with coastal hiking"
    },
    "Event I": {
        "date": datetime(2025, 7, 15, 18, 30),  # July 15, 6:30 PM
        "duration": 2,
        "description": "Introduction to mixed martial arts workshop"
    },
    "Event J": {
        "date": datetime(2025, 7, 18, 6, 30),  # July 18, 6:30 AM
        "duration": 3,
        "description": "Morning bird-watching expedition with guides"
    },
    "Event K": {
        "date": datetime(2025, 7, 22, 20, 0),  # July 22, 8:00 PM
        "duration": 2,
        "description": "Night sky observation with telescope access"
    },
    "Event L": {
        "date": datetime(2025, 7, 25, 13, 0),  # July 25, 1:00 PM
        "duration": 3,
        "description": "Indoor sports tournament (badminton & table tennis)"
    },
    "Event M": {
        "date": datetime(2025, 7, 29, 9, 0),  # July 29, 9:00 AM
        "duration": 3.5,
        "description": "Botanical garden walk with specialty coffee tasting"
    },
    "Event N": {
        "date": datetime(2025, 8, 1, 19, 30),  # August 1, 7:30 PM
        "duration": 3,
        "description": "Michelin-starred fine dining experience"
    },
    "Event O": {
        "date": datetime(2025, 8, 5, 16, 0),  # August 5, 4:00 PM
        "duration": 5,
        "description": "Sunset hiking followed by night stargazing"
    },
    "Event P": {
        "date": datetime(2025, 8, 8, 20, 0),  # August 8, 8:00 PM
        "duration": 4,
        "description": "Board game night with craft beer specials"
    }
}

addresses = {
    "Event A": "Bukit Timah Nature Reserve, Singapore",
    "Event B": "*SCAPE, 2 Orchard Link, Singapore",
    "Event C": "Goodman Arts Centre, 90 Goodman Road, Singapore",
    "Event D": "National Gallery Singapore, 1 St Andrew's Rd, Singapore",
    "Event E": "Maxwell Food Centre, 1 Kadayanallur St, Singapore",
    "Event F": "Clarke Quay, 3 River Valley Rd, Singapore",
    "Event G": "ActiveSG Gym, 100 Jurong East St 13, Singapore",
    "Event H": "East Coast Park, East Coast Park Service Rd, Singapore",
    "Event I": "Evolve MMA, 26 China St, Singapore",
    "Event J": "Sungei Buloh Wetland Reserve, 301 Neo Tiew Cres, Singapore",
    "Event K": "Science Centre Observatory, 15 Science Centre Rd, Singapore",
    "Event L": "Our Tampines Hub, 1 Tampines Walk, Singapore",
    "Event M": "HortPark, 33 Hyderabad Rd, Singapore",
    "Event N": "Odette, 1 St Andrew's Rd, Singapore",
    "Event O": "Pulau Ubin, Singapore",
    "Event P": "Settlers Cafe, 31 North Bridge Rd, Singapore"
}

vendors = {
    "Food": [
        {"name": "Halal Catering Co.", "type": "Halal", "menu": ["Menu A: $20/pax", "Menu B: $25/pax"], "contact": "tel: 9123 4567, email: halal@catering.com"},
        {"name": "Delicious Bites", "type": "Halal", "menu": ["Menu A: $18/pax", "Menu B: $22/pax"], "contact": "tel: 8234 5678, email: delicious@bites.com"},
        {"name": "Gourmet Feast", "type": "Non-Halal", "menu": ["Menu A: $30/pax", "Menu B: $35/pax"], "contact": "tel: 7345 6789, email: gourmet@feast.com"},
        {"name": "Tasty Treats", "type": "Non-Halal", "menu": ["Menu A: $25/pax", "Menu B: $28/pax"], "contact": "tel: 6456 7890, email: tasty@treats.com"},
        {"name": "Nasi Lemak Specialists", "type": "Halal", "menu": ["Set A: $15/pax", "Set B: $20/pax"], "contact": "tel: 6123 1234, email: nasi@lemak.com"},
        {"name": "Dim Sum Masters", "type": "Non-Halal", "menu": ["Premium Set: $35/pax", "Standard Set: $25/pax"], "contact": "tel: 6234 5678, email: dimsum@masters.com"}
    ],
    "Event Organizing": [
        {"name": "Lighting Pros", "service": "Lighting and Fixtures", "price": "$500-$700/event", "contact": "tel: 9123 1234, email: lighting@pros.com"},
        {"name": "Furniture Rentals", "service": "Rentable Furniture", "price": "$300-$500/event", "contact": "tel: 8234 2345, email: furniture@rentals.com"},
        {"name": "Sound Solutions", "service": "Microphones and Sound Equipment", "price": "$200-$400/event", "contact": "tel: 7345 3456, email: sound@solutions.com"},
        {"name": "Event Staffing", "service": "Emcees/Personnel", "price": "$50-$100/person/day", "contact": "tel: 6456 4567, email: staffing@event.com"},
        {"name": "Stage Designers SG", "service": "Stage Setup", "price": "$800-$1200/event", "contact": "tel: 6567 8901, email: stage@design.com"},
        {"name": "AV Experts", "service": "Projection & Screens", "price": "$400-$600/event", "contact": "tel: 6678 9012, email: av@experts.com"}
    ],
    "Event Spaces": [
        {"name": "Marina Bay Sands", "location": "10 Bayfront Ave, Singapore", "price": "$5000-$7000/day", "contact": "tel: 9123 5678, email: events@mbs.com"},
        {"name": "Singapore Expo", "location": "1 Expo Dr, Singapore", "price": "$3000-$5000/day", "contact": "tel: 8234 6789, email: events@expo.com"},
        {"name": "The Fullerton Hotel", "location": "1 Fullerton Square, Singapore", "price": "$4000-$6000/day", "contact": "tel: 7345 7890, email: events@fullerton.com"},
        {"name": "Gardens by the Bay", "location": "18 Marina Gardens Dr, Singapore", "price": "$3500-$5500/day", "contact": "tel: 6456 8901, email: events@gardens.com"},
        {"name": "Raffles City", "location": "252 North Bridge Rd", "price": "$4500-$6500/day", "contact": "tel: 6789 0123, email: events@raffles.com"},
        {"name": "Chijmes Hall", "location": "30 Victoria St", "price": "$3000-$5000/day", "contact": "tel: 6890 1234, email: events@chijmes.com"}
    ]
}

# ============================== CORE FUNCTIONS ==============================
def generate_calendar_view(available_dates, vendor_name=""):
    """Create calendar grid with unique widget keys"""
    months = ["June 2025", "July 2025", "August 2025"]
    selected_month = st.selectbox(
        "Select Month:",
        months,
        key=f"month_selector_{vendor_name}"  # Unique key per vendor
    )
    
    month_num = datetime.strptime(selected_month, "%B %Y").month
    cal = calendar.monthcalendar(2025, month_num)
    
    df = pd.DataFrame(cal, columns=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    df = df.replace(0, "")
    
    available_days = [datetime.strptime(d, "%Y-%m-%d").day for d in available_dates 
                     if datetime.strptime(d, "%Y-%m-%d").month == month_num]
    
    def highlight_days(day):
        return "background-color: #90EE90" if day in available_days else ""
    
    st.dataframe(df.style.map(highlight_days))  # Use .map() instead of .applymap()

def generate_mock_calendar():
    """Generate random availability dates for vendors"""
    start_date = datetime.today()
    forced_date = (start_date + timedelta(days=7)).strftime("%Y-%m-%d")  # Remove extra parenthesis
    
    calendar_data = {}
    for vendor_type in vendors:
        calendar_data[vendor_type] = {}
        for vendor in vendors[vendor_type]:
            # Assign dates for ALL vendors (including special ones)
            dates = [forced_date] + [
                (start_date + timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
                for _ in range(4)
            ] if vendor["name"] in ["Delicious Bites", "Marina Bay Sands", "Event Staffing"] else [
                (start_date + timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
                for _ in range(5)
            ]
            calendar_data[vendor_type][vendor["name"]] = dates
    return calendar_data

def generate_ics(event_name):
    """Generate ICS file content for a given event"""
    cal = Calendar()
    event = Event()
    details = event_details[event_name]
    
    event.add('summary', event_name)
    event.add('description', details["description"])
    event.add('dtstart', details["date"])
    event.add('dtend', details["date"] + timedelta(hours=details["duration"]))
    event.add('location', addresses[event_name])
    
    cal.add_component(event)
    return cal.to_ical()

def create_google_calendar_url(event_name):
    """Generate Google Calendar URL"""
    details = event_details[event_name]
    start = details["date"].strftime("%Y%m%dT%H%M%SZ")
    end = (details["date"] + timedelta(hours=details["duration"])).strftime("%Y%m%dT%H%M%SZ")
    
    params = {
        'action': "TEMPLATE",
        'text': event_name,
        'dates': f"{start}/{end}",
        'details': details["description"],
        'location': addresses[event_name]
    }
    return f"https://www.google.com/calendar/render?{urllib.parse.urlencode(params)}"

def create_outlook_calendar_url(event_name):
    """Generate Outlook Calendar URL"""
    details = event_details[event_name]
    start = details["date"].strftime("%Y-%m-%dT%H:%M:%S")
    end = (details["date"] + timedelta(hours=details["duration"])).strftime("%Y-%m-%dT%H:%M:%S")
    
    params = {
        'path': '/calendar/action/compose',
        'rru': 'addevent',
        'startdt': start,
        'enddt': end,
        'subject': event_name,
        'location': addresses[event_name],
        'body': details["description"]
    }
    return f"https://outlook.live.com/calendar/0/deeplink/compose?{urllib.parse.urlencode(params)}"

       
# ============================== EVENTORGANIZER COMPONENTS ==============================
def vendor_management():
    st.title("Vendor Hub 🛠️")
    vendor_type = st.selectbox("Select Vendor Category:", list(vendors.keys()))
    
    if vendor_type:
        st.header(f"{vendor_type} Partners")
        calendar_data = generate_mock_calendar()
        
        for vendor in vendors[vendor_type]:
            with st.expander(f"**{vendor['name']}**", expanded=False):  # Collapsed by default
                cols = st.columns([2, 3])
                with cols[0]:
                    if "menu" in vendor: 
                        st.write("**Menus**")
                        for menu in vendor["menu"]:
                            st.write(f"🍱 {menu}")
                    st.write(f"📞 {vendor['contact']}")
                
                with cols[1]:
                    dates = calendar_data[vendor_type][vendor['name']]
                    generate_calendar_view(dates, vendor['name'])  # Unique key via vendor name
def event_templates():
    st.title("Event Blueprints 📋")
    templates = {
        "Corporate Dinner": {
            "required_vendors": {
                "Food": "Halal Catering Co.",
                "Event Spaces": "Marina Bay Sands",
                "Event Organizing": "Event Staffing"  
            },
            "description": "Formal dinner with part-time event staff and premium catering with Halal options"
        },
        "Tech Conference": {
            "required_vendors": {
                "Food": "Gourmet Feast",
                "Event Organizing": "AV Experts",
                "Event Spaces": "Singapore Expo"
            },
            "description": "Marketing Event with AV setup and premium catering"
        },
        "Wedding Banquet": {
            "required_vendors": {
                "Food": "Dim Sum Masters",
                "Event Organizing": "Stage Designers SG",
                "Event Spaces": "Chijmes Hall"
            },
            "description": "Private intimate event with custom-made decorations and Dim Sum buffet"
        }
    }
    
    selected_template = st.selectbox("Choose Event Template:", list(templates.keys()))
    
    if selected_template:
        st.subheader(templates[selected_template]["description"])
        calendar_data = generate_mock_calendar()
        required = templates[selected_template]["required_vendors"]
        
        st.markdown("---")
        st.subheader("Vendor Details & Availability")
        
        for category, vendor_name in required.items():
            # Find vendor details
            vendor = next((v for v in vendors[category] if v["name"] == vendor_name), None)
            if not vendor:
                continue
                
            with st.expander(f"**{vendor_name}** ({category})", expanded=True):
                cols = st.columns([2, 3])
                with cols[0]:
                    st.write("#### Contact Information")
                    st.write(vendor["contact"])
                    if "menu" in vendor:
                        st.write("#### Menu Options")
                        for menu in vendor["menu"]:
                            st.write(f"- {menu}")
                
                with cols[1]:
                    st.write("#### Availability Calendar")
                    dates = calendar_data[category][vendor_name]
                    generate_calendar_view(dates, f"{vendor_name}_template")
                    
# ============================== EVENTGOER COMPONENTS ==============================
def get_main_categories():
    return list(categories.keys()) + ["None of the above"]

def get_user_preferences(selected_main):
    preferences = set()
    for category in selected_main:
        if category == "None of the above":
            continue
        suboptions = categories[category] + ["None of the above"]
        selected_sub = st.multiselect(f"Preferences for {category}:", suboptions)
        if "None of the above" in selected_sub:
            st.info(f"No preferences selected for {category}.")
            continue
        preferences.update(selected_sub)
    return preferences

def recommend_events(preferences):
    return [event for event, tags in events.items() if all(tag in preferences for tag in tags)]

def registered_events():
    st.title("My Schedule 🗓️")
    events = {
        "Soon Event": {
            "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "location": "Marina Bay Sands",
            "alert": True
        },
        "Later Event": {
            "date": (datetime.now() + timedelta(days=35)).strftime("%Y-%m-%d"),
            "location": "Singapore Expo",
            "alert": False
        }
    }
    
    for name, details in events.items():
        container = st.container()
        if details["alert"]:
            container.error(f"🚨 **{name}** - {details['date']}")
        else:
            container.info(f"📅 {name} - {details['date']}")
        st.write(f"📍 {details['location']}")
        st.write("---")

def event_recommender():
    st.title("Event Finder 🔍")
    # Step 1: Main Category Selection
    st.header("Step 1: Choose Main Categories")
    main_options = get_main_categories()
    selected_main = st.multiselect("Select categories:", main_options)
    
    if not selected_main:
        st.warning("Please select at least one category.")
        return
    
    if all(opt == "None of the above" for opt in selected_main):
        st.info("Sorry, we'll look into refreshing the choices of events we offer!")
        return
    
    # Step 2: Sub-Option Selection
    st.header("Step 2: Choose Sub-options")
    preferences = get_user_preferences(selected_main)
    
    if not preferences:
        st.warning("No sub-options selected. Adjust your choices.")
        return
    
    # Step 3: Event Recommendations
    recommended = recommend_events(preferences)
    if not recommended:
        st.warning("No matching events found.")
        return
    
    # Step 4: Event Selection with "None" Option
    st.header("Step 3: Explore Events")
    event_options = recommended + ["None"]
    selected_events = st.multiselect("Select events to view addresses (or choose 'None'):", event_options)
    
    if "None" in selected_events:
        st.info("Sorry, we'll look into refreshing the choices of events we offer!")
    elif selected_events:
        st.header("Addresses 📍")
        for event in selected_events:
            if event != "None":
                st.markdown(f"**{event}**: {addresses[event]}")
        
        # Sign-up Form
        st.markdown("---")
        with st.form("signup_form"):
            st.subheader("Event Sign-Up")
            email = st.text_input("Email Address")
            name = st.text_input("Full Name")
            submitted = st.form_submit_button("Confirm Registration")
            
            if submitted:
                if email and name:
                    st.session_state.signed_up_events = selected_events
                    st.session_state.show_calendar_options = True
                    st.success("🎉 Registration Successful!")
                else:
                    st.warning("Please fill in all fields")

        # Calendar Options
        if st.session_state.get('show_calendar_options', False):
            st.markdown("---")
            st.subheader("Add to Calendar 📅")
            
            for event in st.session_state.signed_up_events:
                if event == "None":
                    continue
                
                st.markdown(f"**{event}**")
                cols = st.columns([1,1,2])
                st.markdown("""
                <style>
                img[alt="Google"], img[alt="Outlook"] {
                    width: 48px;
                    height: 48px;
                }
                </style>
                """, unsafe_allow_html=True)
                
                with cols[0]:
                    # Google Calendar
                    google_url = create_google_calendar_url(event)
                    st.markdown(f"[![Google](https://img.icons8.com/color/48/000000/google-calendar.png)]({google_url})", 
                                unsafe_allow_html=True)
                
                with cols[1]:
                    # Outlook Calendar
                    outlook_url = create_outlook_calendar_url(event)
                    st.markdown(f"[![Outlook](https://upload.wikimedia.org/wikipedia/commons/d/df/Microsoft_Office_Outlook_%282018%E2%80%93present%29.svg)]({outlook_url})", 
                                unsafe_allow_html=True)
                
                with cols[2]:
                    # ICS Download
                    ics_file = generate_ics(event)
                    st.download_button(
                        label="Download .ics File",
                        data=ics_file,
                        file_name=f"{event.replace(' ', '_')}.ics",
                        mime="text/calendar"
                    )
                
                st.markdown("---")
                
# ============================== EVENT ANALYTICS STRUCTURE ==============================
# Mock Event Analytics Data
event_analytics = {
    "Event 1": {
        "Revenue from Ticket Sales": 5000,
        "Volume of Sales": 100,
        "Expenses of Rent": 2000,
        "Other Revenue Sources": 500,
        "Duration": "2025-03-01 to 2025-03-03",
        "Status": "Concluded"
    },
    "Event 2": {
        "Revenue from Ticket Sales": 3000,
        "Volume of Sales": 75,
        "Expenses of Rent": 1500,
        "Other Revenue Sources": 300,
        "Duration": "2025-03-10 to 2025-03-12",
        "Status": "Ongoing"
    }
}

def event_analytics_tab():
    st.title("Event Analytics 📊")
    
    # Expanded mock data
    event_analytics = {
        "Annual Tech Summit": {
            "Revenue": {
                "Ticket Sales": 15000,
                "Sponsorships": 25000,
                "Merchandise": 4500,
                "Other": 3200
            },
            "Expenses": {
                "Venue Rental": 8000,
                "Staffing": 4500,
                "Marketing": 6200,
                "Vendors": 11500
            },
            "Attendance": 850,
            "Duration": "2025-03-01 to 2025-03-03",
            "Status": "Concluded"
        },
        "Startup Networking Night": {
            "Revenue": {
                "Ticket Sales": 8000,
                "Sponsorships": 15000,
                "Merchandise": 2200,
                "Other": 1500
            },
            "Expenses": {
                "Venue Rental": 5000,
                "Staffing": 2800,
                "Marketing": 3500,
                "Vendors": 7500
            },
            "Attendance": 420,
            "Duration": "2025-03-10 to 2025-03-12",
            "Status": "Ongoing"
        }
    }
    
    selected_event = st.selectbox("Select Event:", list(event_analytics.keys()))
    
    if selected_event:
        data = event_analytics[selected_event]
        
        # Key Metrics
        total_revenue = sum(data["Revenue"].values())
        total_expenses = sum(data["Expenses"].values())
        net_profit = total_revenue - total_expenses
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:,}")
        col2.metric("Total Expenses", f"${total_expenses:,}")
        col3.metric("Net Profit", f"${net_profit:,}", delta_color="inverse")
        
        # Charts
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Revenue Pie Chart
        revenue_labels = list(data["Revenue"].keys())
        revenue_values = list(data["Revenue"].values())
        ax1.pie(revenue_values, labels=revenue_labels, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Revenue Breakdown')
        
        # Expenses Bar Chart
        expense_categories = list(data["Expenses"].keys())
        expense_values = list(data["Expenses"].values())
        ax2.bar(expense_categories, expense_values)
        ax2.set_title('Expense Distribution')
        ax2.tick_params(axis='x', rotation=45)
        
        st.pyplot(fig)
        
        # Additional Metrics
        st.write(f"**Attendance:** {data['Attendance']} participants")
        st.write(f"**Event Duration:** {data['Duration']}")
        st.write(f"**Status:** {data['Status']}")

# ============================== CHATBOT COMPONENTS ==============================
chat_responses = {
    "hello": "Hi there! How can I help with your event planning today? 😊",
    "help": "I can assist with:\n- Finding vendors\n- Suggesting event ideas\n- Explaining features\nJust ask!",
    "vendors": "Check the [Vendor Hub](#vendor-hub) for:\n🍽️ Food caterers\n🎪 Event spaces\n💡 Planning services",
    "categories": "We offer events in:\n🎨 Hobbies\n🍔 Food\n🏋️ Physical Activities\n🌳 Nature",
    "prices": "Check the prices shown in the [Vendor Hub](#vendor-hub), or call the vendors via their hotline if you have any other queries.",
    "thanks": "You're welcome! Let me know if you need anything else.",
    
    # New responses 
    "events": "Take a look at our Vendor List for our list of vendors, our Event Templates for a ready-made event solution, and our Event Analytics to see the performance of your current and previous events!",
    "calendar": "Click on the drop-down option under each vendor in the Vendor Hub to see their availabilities!",
    "analytics": "Event organizers can view performance metrics in the Event Analytics dashboard.",
    "templates": "Planning an event? Check our ready-made Event Blueprints for quick setup!",
    "food": "We have multiple food vendors including Halal options! Browse them in the Vendor Hub under the Food category.",
    "spaces": "Looking for event spaces? We partner with venues like Marina Bay Sands and Singapore Expo. See all options in the Vendor Hub.",
    "contact": "Need to reach out to specific vendors? Their contact information is available under the drop-down option in the Vendor Hub.",
    "operator": "Please hold while we connect you with a live operator.",
    "default": "I'm still learning! For detailed info, check the other tabs or ask about:\n- Event categories\n- Vendor types\n- Ticket prices. If a live operator is needed, type in 'operator'."
}


def get_bot_response(user_input):
    user_input = user_input.lower()
    
    # Check for greetings
    if any(greeting in user_input for greeting in ["hi", "hello", "hey"]):
        return chat_responses["hello"]
    
    # Check for keywords in user input
    keywords = {
        "help": ["help", "assist", "support"],
        "vendors": ["vendor", "supplier", "caterer", "service provider"],
        "categories": ["category", "type", "kind", "classification"],
        "prices": ["price", "cost", "fee", "expensive", "cheap"],
        "events": ["event", "activity", "happening", "show"],
        "schedule": ["schedule", "my events", "registered", "signed up"],
        "calendar": ["calendar", "add to calendar", "google calendar", "outlook"],
        "analytics": ["analytics", "statistics", "performance", "metrics"],
        "templates": ["template", "blueprint", "preset", "ready-made"],
        "food": ["food", "catering", "meal", "eat", "halal"],
        "spaces": ["space", "venue", "location", "place"],
        "register": ["register", "sign up", "join", "attend"],
        "contact": ["contact", "call", "email", "reach"],
        "recommend": ["recommend", "suggest", "propose", "find me"],
        "operator": ["operator"]
    }
    
    # Check for matches in keywords
    for response_key, trigger_words in keywords.items():
        if any(word in user_input for word in trigger_words):
            return chat_responses[response_key]
    
    # Check for thanks
    if any(word in user_input for word in ["thank", "thanks", "appreciate"]):
        return chat_responses["thanks"]
    
    # Default response if no matches
    return chat_responses["default"]

# ============================== CHATBOT COMPONENTS ==============================
def chat_assistant():
    st.title("Your Event Buddy 🤖")
    
    # Custom CSS for dark text box and message visibility
    st.markdown("""
    <style>
        .stTextInput input {
            background-color: #2D2D2D !important;
            color: white !important;
        }
        /* Fix bot message visibility */
        div[data-testid="stMarkdownContainer"] > div {
            color: #333333 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for i, (sender, msg) in enumerate(st.session_state.chat_history):
            if sender == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 5px;">
                    <div style="background: #0078FF; color: white; padding: 10px; border-radius: 15px; max-width: 70%;">
                        {msg}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 5px;">
                    <div style="background: #F0F2F6; color: #333333; padding: 10px; border-radius: 15px; max-width: 70%;">
                        {msg}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Input box at bottom
    with st.form("chat_input", clear_on_submit=True):
        user_input = st.text_input("Type your message:", key="chat_input_field", value="", placeholder="Ask me about events, vendors, or planning...")
        submitted = st.form_submit_button("Send")
    
    if submitted and user_input:
        st.session_state.chat_history.append(("user", user_input))
        bot_response = get_bot_response(user_input)
        st.session_state.chat_history.append(("bot", bot_response))
        st.rerun()

# ============================== UPDATED MAIN APP STRUCTURE ==============================
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose Mode:", ["Event Explorer", "Organizer Portal", "Chat Assistant"])
    
    if app_mode == "Event Explorer":
        event_recommender()
        st.sidebar.header("My Events")
        registered_events()
        
    elif app_mode == "Organizer Portal":
        st.sidebar.header("Organizer Tools")
        tool = st.sidebar.radio("Select Tool:", 
                              ["Vendor Network", "Event Templates", "Performance Analytics"])
        
        if tool == "Vendor Network":
            vendor_management()
        elif tool == "Event Templates":
            event_templates()
        elif tool == "Performance Analytics":
            event_analytics_tab()
    
    elif app_mode == "Chat Assistant":
        chat_assistant()

if __name__ == "__main__":
    main()
