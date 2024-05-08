flights = []


# Define the function to parse the data
def parse_data(data):
    flight = {}
    cabin_info = []
    price_info = []
    for line in data.split('\n'):
        if line.startswith('departure date'):
            flight['departure_date'] = line.split(': ')[1]
        elif line.startswith('out bound flight number'):
            flight['outbound_flight_number'] = line.split(': ')[1]
        elif line.startswith('out bound flight duration'):
            flight['outbound_flight_duration'] = line.split(': ')[1]
        elif line.startswith('departure time'):
            flight['departure_time'] = line.split(': ')[1]
        elif line.startswith('arrival time'):
            flight['arrival_time'] = line.split(': ')[1]
        elif line.startswith('transition'):
            flight['transition'] = line.split(': ')[1]
        elif line.startswith('return date'):
            flight['return_date'] = line.split(': ')[1]
        elif line.startswith('flight number'):
            flight['flight_number'] = line.split(': ')[1]
        elif line.startswith('flight duration'):
            flight['flight_duration'] = line.split(': ')[1]
        elif line.startswith('cabin info'):
            cabin_info.append(line.split(': ')[1])
        elif line.startswith('price info'):
            price_info.append(line.split(': ')[1])
        elif line.strip() == '':
            flight['cabin_info'] = cabin_info
            flight['price_info'] = price_info
            flights.append(flight)
            flight = {}
            cabin_info = []
            price_info = []


# Input data
data = """
departure date: 05/20/2024
out bound flight number: DL389
out bound flight duration: 15h 35m
departure time: 10:10am
arrival time: 1:45pm
transition: Nonstop
return date: 08/13/2024
flight number: DL388
flight duration: 14h 10m
transition: Nonstop
cabin info: Main (K)
price info: 3,771
cabin info: Comfort+® (S)
price info: 3,871
cabin info: Premium Select (P)
price info: 4,650
cabin info: Delta One® Suites (I)
price info: 5,592
"""
"""

"""
# Parse the data
parse_data(data)

# Print the organized flights
for flight in flights:
    print(flight)
