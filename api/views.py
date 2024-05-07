from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_jobs(request):
    # Set up Chrome webdriver
    driver = webdriver.Chrome()

    # Navigate to the specified URL
    url = "https://www.indeed.com/jobs?q=driver+ltv&l=india&from=searchOnHP&vjk=42539aeec5a21679"
    driver.get(url)

    # Wait for the job listings to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "mosaic-provider-jobcards")))

    # Find the <div> element with the specified ID
    job_list_container = driver.find_element(By.ID, "mosaic-provider-jobcards")

    # Find all <a> tags within the <div> element
    job_links = job_list_container.find_elements(By.CLASS_NAME, "jcs-JobTitle")

    # Extract href attribute from each <a> tag and navigate to it
    links = []
    for job_link in job_links:
        href = job_link.get_attribute("href")
        # print("Navigating to:", href)
        links.append(href)

    # Initialize a list to store job data
    job_data_list = []

    # Loop through each job link
    for link in links:
        driver.get(link)

        # Wait for the job title element to load
        job_title_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[1]/h1/span")))

        try:
            company_name_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/span/a")))
            salary = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/div/span"))).text
            company_name = company_name_element.text
            company_link = company_name_element.get_attribute("href")
        except:
            company_name = 'N/A'
            company_link = 'N/A'
            salary = 'N/A'

        location = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div")))

        # Get the page source
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find the job description <div> element
        job_description_div = soup.find("div", {"id": "jobDescriptionText"})

        # Extract the job description text
        job_description_text = job_description_div.text.strip()

        # Extract the job description HTML with tags
        job_description_html = job_description_div.prettify()

        # Extract the job title text
        job_title = job_title_element.text

        # Organize scraped data into a dictionary
        job_data = {
            "job_title": job_title,
            "company_name": company_name,
            "company_link": company_link,
            "location": location.text,
            "salary": salary,
            "job_description_text": job_description_text,
            "job_description_html": job_description_html,
            "job_link": link
        }

        # Append job data to the list
        job_data_list.append(job_data)

    # Quit the driver
    driver.quit()

    # Return scraped data as JsonResponse
    return JsonResponse({"jobs": job_data_list})
