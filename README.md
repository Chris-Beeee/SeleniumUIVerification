# Selenium WebDriver Portfolio: TMDB Test Suite

This repository serves as a portfolio piece demonstrating automated web UI testing using **Python**, **Selenium WebDriver**, and **Pytest**. 

The primary goal of this repository is to use the Page Object Model examples but with a live API verifying the results against the data fro the front end of the site, as opposed to the examples given in my portfolio which only verify the results against a mock backend. 

[themoviedb.org](https://www.themoviedb.org) was chosen because it has a free API that can be used for non-commercial projects, unlike more well known sites like IMDB, which only licences its API commercially. 

These tests have been designed to work whether you have 1) a login with the site or 2) have applied for and been given an API key or not. Though obviously the tests are primarily designed for a user who has both. 
* [Login or create an account](https://www.themoviedb.org/login)
* [API details (account required)](https://www.themoviedb.org/settings/api)

---

## Test Scope & Environments

This suite runs automated UI interactions against **The Movie Database (TMDB)** (`test_tmdb_...`):

* **Category Verification**: Scrapes movie titles across different categories (Now Playing, Popular, Upcoming, Top Rated) and dynamically compares them to TMDB's backend API to ensure the front-end displays correct data.
* **Authentication**: Tests the login functionality. First, it authenticates the API token to ensure backend access, then drives Selenium to log into the UI.
* **Basic Movie Discovery (`tests/test_tmdb_discover_pom.py`)**: Tests movie filtering utilizing primary filters: **Genre**, **Keyword** (with autocomplete selection), and **Date Range**, verifying UI results against the production API.
* **Advanced Multi-Filter Discovery (`tests/test_tmdb_discover_complex.py`)**: Tests highly complex, dynamic queries utilizing **all** advanced filters: **Certification**, **User Score**, **Minimum User Votes**, **Language**, **Runtime**, **Availabilities**, and **Show me**. Omitted filters are dynamically bypassed. Kendo UI sliders and dropdowns are driven robustly via programmatically injected jQuery scripts.

## Backend Verification Layer

To make these tests robust, they include a backend verification layer that validates UI scraped data against production API responses. 

### Key Architectural Features:
1. **Dynamic Real API / Mock Fallback:**
   * **TMDB Client (`utils/tmdb_api.py`):** Queries the official TMDB API if a `TMDB_API_READ_ACCESS_TOKEN` is present in `.env`. 
   * If credentials are not set (or if you use the `--mock-api` flag), it falls back to pre-seeded mock datasets, allowing the tests to run offline or in CI environments without false failures.
   * **Regional UI Accuracy:** When real credentials are provided, the category tests will explicitly log in to TMDB before scraping. This ensures the UI results apply the correct regional account settings (e.g., UK region) to perfectly match the API localization.

2. **Intelligent Matching Engine (`utils/backend_verifier.py`):**
   * **Fuzzy Similarity Math:** Calculates structural sequence similarity to successfully match slight layout or naming variations between the UI and API.
   * **Stop Word & Punctuation Filtering:** Filters out noise tokens so matching is based purely on meaningful keywords.

---

## Technology Stack
* **Language:** Python 3.x
* **Browser Automation:** Selenium WebDriver 4.x
* **Testing Framework:** Pytest
* **Reporting:** Pytest-HTML
* **HTTP Client:** Requests

---

## How to Run Locally

**1. Clone the repository and navigate to the directory**
```powershell
git clone https://github.com/Chris-Beeee/SeleniumUIVerification.git
cd SeleniumUIVerification
```

**2. Create and activate a virtual environment**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**
```powershell
pip install -r requirements.txt
```

**4. Setup Environment Variables**
Copy `.env.example` to `.env` and supply your TMDB credentials. This allows the API verification and login tests to pass successfully:
```env
TMDB_USERNAME=your_username
TMDB_PASSWORD=your_password
TMDB_API_READ_ACCESS_TOKEN=your_read_access_token
```

**5. Run the tests**

**Run normally (uses your credentials to log in and test real API data):**
```powershell
pytest -v -s
```

**Run in Mock/Offline Mode (ignores credentials, skips login tests, uses offline mock data):**
```powershell
pytest -v -s --mock-api
```

**Run only the POM category and basic discover tests:**
```powershell
pytest tests/test_tmdb_*_pom.py -v -s
```

**Run the advanced multi-filter discover tests:**
```powershell
pytest tests/test_tmdb_discover_complex.py -v -s
```

**Run everything and generate a timestamped HTML report (saved inside the `reports/` folder):**
```powershell
pytest --html=report.html
```
