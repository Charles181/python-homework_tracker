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
            assignment['due_date'] = due_date
            
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

    # Output the assignments
    print(month)
    for assignment in assignments:
        print(f"Assignment: {assignment['name']}")
        print(f"Due Date: {assignment['due_date']}")
        print(f"Course: {assignment['course']}")
        print(f"URL: {assignment['url']}\n")
    
    return assignments

def save_file(data, file):
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)
        

# Main script
if __name__ == "__main__":
    # Moodle credentials and URLs
    username = '2240400'
    password = 'WKOX1013411'
    login_url = 'https://aula.uane.mx/login/index.php'
    calendar_url = 'https://aula.uane.mx/calendar/view.php?view=month'
    
    # Replicating the headers from Developer Tools
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'es-US,es;q=0.9,es-419;q=0.8,en;q=0.7',
        'referer': 'https://aula.uane.mx/my/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }
    
    with requests.Session() as session:
        # Login to Moodle
        if login_to_moodle(username, password, login_url, session):
            # Get the assignments from the calendar
            assignments = get_assignments(calendar_url, session, headers)
            
            # Output the assignments as JSON
            save_file(assignments, 'data.json')
            print(json.dumps(assignments, indent=4))
