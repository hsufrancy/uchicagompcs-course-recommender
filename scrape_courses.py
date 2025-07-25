import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import urllib3
from urllib.parse import urljoin, urlparse
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://mpcs-courses.cs.uchicago.edu/"
quarters = [
    "2025-26/summer", "2025-26/spring", "2025-26/winter", "2025-26/autumn"
]

course_urls = []

for quarter in quarters:
    list_url = f"{base_url}{quarter}/courses"
    print(f"Fetching course list from {list_url}")
    
    try:
        res = requests.get(list_url, verify=False, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Find the table with course listings
        table = soup.find("table", class_="table")
        if table:
            # Find all rows in the table body
            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                
                for row in rows:
                    # Find the second cell (index 1) which contains the course name and link
                    cells = row.find_all("td")
                    if len(cells) >= 2:
                        # Look for the link in the second cell
                        link = cells[1].find("a", href=True)
                        if link:
                            href = link["href"]
                            # Convert to absolute URL
                            full_url = urljoin(base_url, href.lstrip('/'))
                            
                            # Avoid duplicates
                            if full_url not in course_urls:
                                course_urls.append(full_url)
                                print(f"Found course: {full_url}")
        
        # Add small delay to be respectful to the server
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Failed to fetch {list_url}: {e}")

print(f"\nTotal courses found: {len(course_urls)}\n")

# Phase 2: Visit each course URL and extract information
course_data = []

for url in tqdm(course_urls, desc="Scraping course details"):
    try:
        res = requests.get(url, verify=False, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Extract title
        title_elem = soup.find("h1")
        title = title_elem.text.strip() if title_elem else "No title found"
        
        course_info = {"url": url, "title": title}
        
        # Extract course code from URL or title
        url_parts = url.split('/')
        if len(url_parts) > 0:
            course_code = url_parts[-1]  # e.g., "mpcs-50101-1"
            course_info["course_code"] = course_code
        
        # 1. Extract main info table (course details)
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    key = th.text.strip().lower().replace(" ", "_").replace(":", "").replace("-", "_")
                    value = td.get_text(strip=True)
                    course_info[key] = value
        
        # 2. Extract any description paragraphs
        description_parts = []
        # Look for description in various possible containers
        for selector in [".description", ".course-description", "p"]:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if len(text) > 50:  # Only take substantial text blocks
                    description_parts.append(text)
        
        if description_parts:
            course_info["description"] = " | ".join(description_parts[:3])  # Limit to first 3 paragraphs
        
        # 3. Extract syllabus sections
        syllabus_div = soup.find("div", class_="syllabus")
        if syllabus_div:
            h3s = syllabus_div.find_all("h3")
            for h3 in h3s:
                section_title = h3.text.strip().lower().replace(" ", "_").replace(":", "").replace("-", "_")
                next_tag = h3.find_next_sibling()
                
                if next_tag:
                    if next_tag.name == "p":
                        course_info[section_title] = next_tag.get_text(strip=True)
                    elif next_tag.name == "ul":
                        items = [li.get_text(strip=True) for li in next_tag.find_all("li")]
                        course_info[section_title] = " | ".join(items)
                    elif next_tag.name == "div":
                        course_info[section_title] = next_tag.get_text(strip=True)
        
        # 4. Extract any other structured content
        # Look for additional sections that might contain course info
        for heading in soup.find_all(["h2", "h3", "h4"]):
            if heading.text.strip():
                section_name = heading.text.strip().lower().replace(" ", "_").replace(":", "").replace("-", "_")
                # Get content after the heading
                content_parts = []
                next_elem = heading.find_next_sibling()
                while next_elem and next_elem.name not in ["h1", "h2", "h3", "h4"]:
                    if next_elem.name in ["p", "div", "ul"]:
                        text = next_elem.get_text(strip=True)
                        if text:
                            content_parts.append(text)
                    next_elem = next_elem.find_next_sibling()
                
                if content_parts:
                    course_info[section_name] = " | ".join(content_parts)
        
        course_data.append(course_info)
        
        # Add small delay to be respectful to the server
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Save to CSV
if course_data:
    df = pd.DataFrame(course_data)
    df.to_csv("mpcs_courses.csv", index=False)
    print(f"\nScraping complete! Data saved to mpcs_courses.csv")
    print(f"Total courses scraped: {len(course_data)}")
else:
    print("\nNo course data was collected. Please check the URLs and website structure.")