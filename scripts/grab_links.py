import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# run with 
# python grab_links.py /Users/jye/Desktop/scrape_v2/inputs/inputs.csv /Users/jye/Desktop/scrape_v2/outputs/output.csv



def setup_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                                " AppleWebKit/537.36 (KHTML, like Gecko)"
                                " Chrome/85.0.4183.102 Safari/537.36")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def read_job_roles(input_csv):
    try:
        df = pd.read_csv(input_csv)
        if 'job_role' not in df.columns:
            raise ValueError("Input CSV must have a 'job_role' column.")
        job_roles = df['job_role'].dropna().unique().tolist()
        return job_roles
    except Exception as e:
        print(f"Error reading input CSV: {e}")
        return []

def search_indeed(driver, job_role):
    base_url = "https://www.indeed.com.sg"
    search_url = f"{base_url}/jobs?q={job_role.replace(' ', '+')}&l="
    driver.get(search_url)
    
    job_links = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.slider_container'))
        )

        try:
            main_job = driver.find_element(By.CSS_SELECTOR, 'div.fastviewjob')
            main_link = main_job.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if main_link and '/cmp/' not in main_link: 
                job_links.append(main_link)
        except NoSuchElementException:
            print("No main job listing found.")

        job_cards = driver.find_elements(By.CSS_SELECTOR, 'div.slider_container')
        print(f"Found {len(job_cards)} job cards for {job_role}")

        for job_card in job_cards:
            try:
                job_link = job_card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if job_link and '/cmp/' not in job_link: 
                    job_links.append(job_link)
            except NoSuchElementException:
                continue

    except TimeoutException:
        print(f"Timeout: No job postings found for: {job_role}")
    
    except Exception as e:
        print(f"Error searching for {job_role}: {e}")
    
    return job_links


def search_and_collect_all_jobs(driver, job_role):
    """
    This function collects all job links across multiple pages for a given job role.
    """
    collected_links = []
    current_page = 1
    while True:
        print(f"Scraping page {current_page} for job role: {job_role}")
        links_on_page = search_indeed(driver, job_role)
        if not links_on_page:
            break
        collected_links.extend(links_on_page)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
            next_button.click()
            time.sleep(2) 
            current_page += 1
        except NoSuchElementException:
            print(f"No more pages for job role: {job_role}")
            break
    
    return collected_links


def write_output(output_csv, data):
    try:
        print(f"Writing data to CSV: {data}")

        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['job_role', 'link'])
            writer.writerows(data)

        print(f"Data successfully written to {output_csv}")
    except Exception as e:
        print(f"Error writing to output CSV: {e}")



def main(input_csv, output_csv):
    job_roles = read_job_roles(input_csv)
    if not job_roles:
        print("No job roles to process.")
        return

    driver = setup_driver(headless=True)
    results = []

    for job_role in job_roles:
        print(f"Searching for: {job_role}")
        links = search_and_collect_all_jobs(driver, job_role)
        for link in links:
            results.append([job_role, link])
        time.sleep(2)  # delay

    driver.quit()
    write_output(output_csv, results)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search Indeed.com for job roles and retrieve links.")
    parser.add_argument('input_csv', help='/Users/jye/Desktop/scrape_v2/inputs/inputs.csv')
    parser.add_argument('output_csv', help='/Users/jye/Desktop/scrape_v2/outputs')

    args = parser.parse_args()
    main(args.input_csv, args.output_csv)
