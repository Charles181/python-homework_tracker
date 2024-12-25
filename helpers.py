import requests
from bs4 import BeautifulSoup
import json

# Function to login to Moodle
def login_to_moodle(username, password, login_url, session):
    # Payload for login (form data)
    login_payload = {
        'username': username,
        'password': password,
    }
    
    # Perform login
    response = session.post(login_url, data=login_payload)
    
    if response.status_code == 200:
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False

# Function to extract homework/assignments from calendar
def get_assignments(calendar_url, session, headers):
    response = session.get(calendar_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve calendar")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    calendar_table = soup.find('table', class_='calendarmonth')

    # Initialize list to store assignments
    assignments = []
    month = soup.find('h2', class_='current').text.strip()
    # Loop through each 'td' day element in the calendar table
    for day_cell in calendar_table.find_all('td', class_='clickable'):
        # Get the day number from the 'a' tag (if present)
        day_number = day_cell.find('a', class_='day').text if day_cell.find('a', class_='day') else day_cell.text.strip()

        # Get all the assignment events for that day
        events = day_cell.find_all('li', class_='calendar_event_course')

        # Process each event (assignment)
        for event in events:
            assignment = {}
            
            # Extract the assignment title from the 'a' tag
            assignment_link = event.find('a', {'data-action': 'view-event'})
            assignment_name = assignment_link.text.strip()
            assignment_url = assignment_link['href']
            
            # Extract the due date (same as day number)
            due_date = day_number

            # Add assignment details to the dictionary
            assignment['name'] = assignment_name
            assignment['url'] = assignment_url
            assignment['fecha_de_entrega'] = due_date
            
            # Extract course information (if available)
            course_name = None
            course_select = soup.find('select', id='course')
            if course_select:
                selected_option = course_select.find('option', selected=True)
                if selected_option:
                    course_name = selected_option.text.strip()

            assignment['course'] = course_name
            
            # Add the assignment to the list
            assignments.append(assignment)

    return assignments

def save_file(data, file):
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)
        

# Function encapsulation
def fetch_and_save_assignments(username, password, login_url, calendar_url, headers, output_file='assignments.json'):
    with requests.Session() as session:
        # Step 1: Login to Moodle
        if login_to_moodle(username, password, login_url, session):
            # Step 2: Fetch assignments
            assignments = get_assignments(calendar_url, session, headers)
            
            # Step 3: Save assignments to a file
            save_file(assignments, output_file)
            return assignments
        else:
            return None
