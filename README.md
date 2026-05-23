# Selenium WebDriver Portfolio: TMDB Test Suite

This repository serves as a portfolio piece demonstrating automated web UI testing using **Python**, **Selenium WebDriver**, and **Pytest**. 

The primary goal of this repository is to demonstrate an end-to-end automation stack utilizing the **Page Object Model (POM)** for robust, maintainable tests, specifically targeting **The Movie Database (TMDB)**.

---

## Architecture Showcase

The tests in this repository use the **Page Object Model**. This design pattern separates the UI element locators (CSS/XPath) and page interaction methods from the actual test logic. This makes the codebase significantly easier to read, maintain, and update when the UI changes.

There is also a standard, top-to-bottom procedural script (`test_tmdb_login.py`) for comparison, demonstrating why POM is preferred for complex flows.

---

## Test Scope & Environments

This suite runs automated UI interactions against **The Movie Database (TMDB)** (`test_tmdb_...`):

* **Category Verification**: Scrapes movie titles across different categories (Now Playing, Popular, Upcoming, Top Rated) and dynamically compares them to TMDB's backend API to ensure the front-end displays correct data.
* **Authentication**: Tests the login functionality. First, it authenticates the API token to ensure backend access, then drives Selenium to log into the UI.

## Backend Verification Layer

To make these tests robust, they include a backend verification layer that validates UI scraped data against production API responses. 

### Key Architectural Features:
1. **Dynamic Real API / Mock Fallback:**
   * **TMDB Client (`utils/tmdb_api.py`):** Queries the official TMDB API if a `TMDB_API_READ_ACCESS_TOKEN` is present in `.env`. 
   * If credentials are not set, it can fall back to pre-seeded mock datasets, allowing the tests to run offline or in CI environments without false failures.

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
```powershell
# Run all TMDB POM tests with verbose output
pytest tests/test_tmdb_*_pom.py -v -s

# Run the linear login test
pytest tests/test_tmdb_login.py -v -s

# Run everything and generate an HTML report
pytest --html=report.html
```
