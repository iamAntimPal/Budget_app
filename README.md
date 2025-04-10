# Budget Management Application

A lightweight, CSV‑backed budget management application built with Python’s Tkinter library. This application features a secure login and registration system, a menu‐driven interface to navigate through Dashboard, Add Entry, and Reports screens, and a dark/light theme toggle. All data is persisted using CSV files stored in the `data/` folder.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/github/license/antim-1000/ThinkTrack)](https://github.com/antim-1000/ThinkTrack/blob/main/LICENSE)
[![GitHub](https://img.shields.io/github/last-commit/antim-1000/ThinkTrack)](https://github.com/antim-1000/ThinkTrack/commits/main)

## Features

- **User Authentication:**  
  Secure login and registration using password hashing (bcrypt) with credentials stored in CSV.

- **Dashboard:**  
  A sample dashboard displaying a welcome message and a sample pie chart for expense breakdown.

- **Add Entry:**  
  A form that lets users add income or expense entries with fields for type, amount, category, date, and description.

- **Reports:**  
  Export sample budget reports to PDF or Excel using third-party libraries (`fpdf` and `pandas`).

- **Theme Toggle:**  
  Easily switch between light and dark themes with a toggle button.

- **CSV Persistence:**  
  Data is stored in three CSV files under the `data/` folder:
  - `users.csv` – Stores user credentials and preferred currency.
  - `entries.csv` – Stores income/expense entries.
  - `recurring.csv` – Stores recurring transaction details.

## Project Folder Structure

```rb
budget_app/
├── main.py 
|── app/         # Application entry point and main menu logic
│   ├── auth.py          # User authentication logic using CSV persistence
│   └── manager.py       # Business logic for managing entries and recurring transactions
├── data/
│   ├── database.py      # CSV file operations for data persistence
│   └── models.py        # Data models (Entry, RecurringTransaction)
├── ui/
│   ├── components.py    # Reusable UI elements (BaseFrame, LoginForm, MainMenu)
│   ├── dashboard.py     # Dashboard screen (shows welcome message & chart sample)
│   ├── forms.py         # Entry form for adding/editing income/expense entries
│   ├── reports.py       # Reporting interface to export data as PDF or Excel
│   └── styles/
│       ├── light.css    # Light theme style definitions (dummy CSS-like file)
│       └── dark.css     # Dark theme style definitions (dummy CSS-like file)
└── requirements.txt     # List of external dependencies
```

> **Note:** The CSV “database” is created automatically under the `data/` folder when the application is first launched.

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- pip (Python package installer)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/iamAntimPal/Budget_app.git
   cd budget_app
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv env
   source env/bin/activate    # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Application:**

   In the project root directory, run:

   ```bash
   python app/main.py
   ```

2. **On First Run:**

   - The application will automatically create the `data/` folder if it does not exist.
   - Three CSV files (`users.csv`, `entries.csv`, `recurring.csv`) will be created in the `data/` folder with the necessary headers.

3. **Using the Application:**

   - **Login / Registration:**  
     Enter your username and password on the login screen. Use the "Register" button if you are a new user.

   - **Main Menu:**  
     After a successful login, you will see the main menu. From here, you can navigate between:
     - **Dashboard:** View a sample dashboard with a pie chart.
     - **Add Entry:** Open the form to add an income/expense entry.
     - **Reports:** Generate and export a sample report as PDF or Excel.
     - **Logout:** Log out and return to the login screen.
     - **Toggle Theme:** Switch between light and dark themes.

## Dependencies

The application uses several external libraries. Refer to `requirements.txt` for the full list:

- `bcrypt`
- `tkcalendar`
- `matplotlib`
- `fpdf`
- `pandas`
- `openpyxl`
- `schedule`

Install them using:

```bash
pip install -r requirements.txt
```

## Customization

- **CSV Database:**  
  The CSV files are used for data persistence. You can view and modify these directly from the `data/` folder.

- **Theme Files:**  
  The light and dark theme definitions are provided in `ui/styles/light.css` and `ui/styles/dark.css`. Although Tkinter does not directly use CSS, these files serve as a style reference for applying widget styles.

- **Code Extensions:**  
  The code is structured in a modular and class-based format, making it easy to extend functionalities (e.g., additional reporting features or advanced recurring transaction handling).

## Contributing

Feel free to fork this repository and make improvements. Pull requests are welcome!

## License

[MIT License](LICENSE)

## Acknowledgments

This project uses various open-source libraries. Many thanks to their contributors.
