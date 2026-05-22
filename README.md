# Selenium WebDriver Portfolio: Linear to POM Refactoring

This repository serves as a portfolio piece demonstrating automated web UI testing using **Python**, **Selenium WebDriver**, and **Pytest**. 

The primary goal of this repository was as a POC to make sure my Pytest automation stack is installed and working. The secondary use case was to demonstrate the benefits of the Page Object Model as a way to make test maintenance easier. 

---


## Architecture Showcase

Every test in this repository has two versions:
1. **`_linear.py`**: A standard, top-to-bottom procedural script. Useful for quick Proof-of-Concepts (POCs), but prone to fragility when UI elements change. I find this method easier to debug any initial issues in getting a POC running.
2. **`_pom.py`**: The exact same test refactored using the **Page Object Model**. This separates the UI element locators (CSS/XPath) from the actual test logic, making the code much easier to maintain.

---

## Test Scope & Environments

This suite runs automated UI interactions against three platforms:

* **Amazon (`test_amazon_search_...`)**: Tests product search functionality, DOM traversal, and scraping results.
* **YouTube (`test_youtube_search_...`)**: Handles complex asynchronous loading, cookie consent banners (region-dependent), search video extraction, and verifies scraped results against the YouTube API.
* **Giant Bomb (`test_giantbomb_frontpage_...`)**: Validates frontpage structural elements, dynamic content loading, and verifies scraped videos against the Giant Bomb API.

## Backend Verification Layer 

I have added a dummy verfiication layer for the **YouTube** and **Giant Bomb** test suites. This layer validates UI scraped data against production API databases. It's designed to allow the tests to run without direct API access. I will need to test this against a site which has some user level API access to see the behaviour when you can query an API directly. At present I have only tested the mock capabilities. 

### Key Architectural Features:
1. **Dynamic Real API / Mock Fallback:**
   * **YouTube Client (`utils/youtube_api.py`):** Automatically queries the official YouTube Data API v3 if a `YOUTUBE_API_KEY` is present in `.env`.
   * **Giant Bomb Client (`utils/giantbomb_api.py`):** Queries the official Giant Bomb API if a `GIANTBOMB_API_KEY` is present in `.env`.
   * If credentials are not set, both clients automatically fall back to pre-seeded mock datasets, allowing the tests to run offline or in generic CI environments without false failures.

2. **Intelligent Matching Engine (`utils/backend_verifier.py`):**
   * **Strict 1-to-1 Matching:** Enforces index tracking to prevent duplicate matching. Once a mock API video title is matched, it is locked, ensuring a true list-to-list comparison.
   * **Stop Word & Punctuation Filtering:** Filters out noise tokens like hyphens `-`, colons `:`, and common English stop words (*the, of, and, a, to, in, with*) so matching is based purely on meaningful keywords.
   * **Fuzzy Similarity Math:** Calculates structural sequence similarity (difflib ratio $\ge 0.5$) and keyword overlap ($\ge 2$ words) to successfully match layout variations.
   * **Unicode Resilience:** Employs a safe-encoding output printer to eliminate potential `UnicodeEncodeError` console crashes in Windows terminals when rendering titles with emojis or custom symbols.

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
git clone https://github.com/Chris-Beeee/SeleniumTests.git
cd SeleniumTests
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

**4. Setup Environment Variables (Optional)**
Copy `.env.example` to `.env` and supply keys to test against real production API backends:
```env
YOUTUBE_API_KEY=your_key_here
GIANTBOMB_API_KEY=your_key_here
```

**5. Run the tests**
```powershell
# Run all tests with verbose output and console prints
pytest -v -s

# Run only the Page Object Model tests
pytest tests/test_*_pom.py -s

# Run only the Linear tests
pytest tests/test_*_linear.py -s
```
