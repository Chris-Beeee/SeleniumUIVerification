import os
from datetime import datetime

def pytest_configure(config):
    """
    Hook to dynamically configure the HTML report path with a timestamp.
    Saves the reports into a 'reports' directory.
    """
    if config.pluginmanager.hasplugin('html'):
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Force override the HTML path so it always goes into the reports folder
        config.option.htmlpath = f"reports/report_{timestamp}.html"
        config.option.self_contained_html = True

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Hook to print a master summary at the very end of the console output.
    It reads 'record_property' items saved during the tests.
    """
    terminalreporter.section("MASTER EXECUTION SUMMARY", sep="=", bold=True)
    
    # Iterate through all tests (passed, failed, etc.)
    all_reports = terminalreporter.stats.get('passed', []) + terminalreporter.stats.get('failed', [])
    
    # Sort them to keep output chronological/ordered
    for test_report in sorted(all_reports, key=lambda x: x.nodeid):
        if hasattr(test_report, 'user_properties'):
            # user_properties is a list of tuples: [("api_msg", "[API] ..."), ("ui_msg", "[UI] ..."), ("match_msg", "[VERIFIER] ...")]
            for name, value in test_report.user_properties:
                if name in ("api_msg", "ui_msg", "match_msg"):
                    terminalreporter.write_line(value)

import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--mock-api", action="store_true", default=False, help="Run tests with mock API data"
    )

@pytest.fixture(scope="session")
def is_mock_mode(request):
    return request.config.getoption("--mock-api")
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to explicitly inject our custom execution summaries directly into the HTML report
    and capture screenshots/page source on failure.
    """
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    
    if report.when == "call":
        # Capture debug artifacts on failure
        if report.failed:
            driver = getattr(item, "driver", None)
            if driver:
                import os
                from datetime import datetime
                try:
                    from pytest_html import extras as html_extras
                    os.makedirs("reports/screenshots", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    screenshot_name = f"fail_{timestamp}.png"
                    source_name = f"fail_{timestamp}.html"
                    
                    screenshot_path = os.path.join("reports", "screenshots", screenshot_name)
                    source_path = os.path.join("reports", "screenshots", source_name)
                    
                    driver.save_screenshot(screenshot_path)
                    # Embed screenshot into the report
                    extras.append(html_extras.image(f"screenshots/{screenshot_name}"))
                    
                    # Save page source
                    with open(source_path, "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    # Embed link to page source
                    source_link = f"<div style='margin-top: 10px;'><a href='screenshots/{source_name}' target='_blank'>View DOM Page Source at Failure</a></div>"
                    extras.append(html_extras.html(source_link))
                except Exception as e:
                    print(f"Failed to capture debug artifacts: {e}")

        # Inject execution summaries
        if hasattr(report, 'user_properties'):
            messages = []
            for name, value in report.user_properties:
                if name in ("api_msg", "ui_msg", "match_msg"):
                    messages.append(value)
            
            if messages:
                try:
                    from pytest_html import extras as html_extras
                    summary_text = "\n".join(messages)
                    
                    html_block = (
                        "<div style='background-color: #f1f8ff; padding: 10px; "
                        "border: 1px solid #c8e1ff; border-radius: 5px; margin-bottom: 10px;'>"
                        "<strong>Master Execution Summary:</strong><br>"
                        f"<pre style='margin-top: 5px; margin-bottom: 0px;'>{summary_text}</pre>"
                        "</div>"
                    )
                    extras.append(html_extras.html(html_block))
                except ImportError:
                    pass
        report.extras = extras
