# kalles_restaurant
# Project goals
The goal of this project is to build a functional and user-friendly Restaurant Booking System that allows visitors to make reservations online and helps restaurant staff manage those bookings efficiently.

This project will be built using HTML, CSS, JavaScript (frontend), Python + Django (backend), and PostgreSQL as the database. The map functionality will be implemented using an external API.

### External user goals 
* Book one or more guests for a specific date and time.
* Receive confirmation that their reservation has been successfully submitted.
* View where the restaurant is located via an interactive map.
* Preview the menu and access contact details before booking.

### Site Owner Goals
* Receive and manage online booking requests directly through the admin.py 
* Prevent double bookings and ensure each time slot has appropriate table availability.
* Reduce manual handling of reservations by automating the booking process.

# Data model 
This model represents a restaurant booking. Each booking has a unique ID (primary key) and stores essential information such as the full name of the person making the booking, the date and time of the reservation, and the number of guests included. This structure allows the restaurant to keep track of individual bookings in an organized and efficient way.
### Booking.model

| Fieldname |  Data type | Description |
|:-----|:--------:|:------:|
| **id**  | PK | Unique identifier for each booking  |
| **full_name**   |  CharField (max_length=200)  |  Name of the person making the booking  |
| **date**   | DateField | Date of the booking |
| **time**   | TimeField | Time of the booking |
| **guests**   | PositiveIntegerField | Number of guests included in the booking |



# Wiremframes
![alt](./readme-images/desktop-wireframe.png)
![alt](./readme-images/mobile-wireframe.png)