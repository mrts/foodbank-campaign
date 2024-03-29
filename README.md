# Foodbank Campaign Management Application

The Foodbank Campaign Management Application is designed to support foodbanks in
organizing and running food collection campaigns in shops efficiently. This
[Django](https://www.djangoproject.com/)-based application facilitates campaign
management, volunteer sign-up, location management and scheduling of volunteer
shifts at shops where the food is collected.

## Features

- **Campaign management**: Allows administrators to create, update and manage campaigns, including setting campaign dates, descriptions and active status.
- **Locations and shift scheduling**: Supports the definition of locations such as shops and scheduling of volunteer shifts, making it easy to manage where and when volunteers can participate in the campaign.
- **Volunteer sign-up**: Through a web interface, volunteers can find campaigns, view available locations and shifts and sign up to participate. The system dynamically updates free places in shifts based on volunteer registrations.

## Prerequisites

- Python 3.8 or higher
- Dependencies listed in `src/requirements.txt`

## Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/mrts/foodbank-campaign.git
   ```
2. Navigate to the project directory:
   ```
   cd foodbank-campaign
   ```
3. Setup _virtualenv_ and install the required Python packages:
   ```
   python -m venv venv
   . venv/bin/activate # or follow your platform convention
   cd src
   pip install -r requirements.txt
   ```
4. Set up the database (assuming you're using the default SQLite for development):
   ```
   python manage.py migrate
   ```
5. Create a superuser account for Django admin:
   ```
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```
7. Open your web browser and go to <http://127.0.0.1:8000> to view the application.

## Usage

- **Admin interface**: Access the Django admin interface at <http://127.0.0.1:8000/haldus> to manage campaigns, locations and shifts.
- **Volunteer sign-up**: Try the volunteer interface at <http://127.0.0.1:8000> where volunteers can view active campaigns and sign up for shifts.

## Contributing

Contributions to the Foodbank Campaign Management Application are most welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add a new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.



