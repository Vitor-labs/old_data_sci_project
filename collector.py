from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

import time
import pandas 

def get_data(keyword, mum, verbose, path, sleep_time=1):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + \
        '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < mum:
        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(sleep_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            prompt = driver.find_element(By.CLASS_NAME , "modal_main")
            prompt.click()
            print("Sign up prompt detected. Clicking to continue.")
            time.sleep(sleep_time)
        except ElementClickInterceptedException:
            print("Sign up prompt not detected.")

        time.sleep(.1)

        try:
            exit = driver.find_element(By.CLASS_NAME , 'SVGInline-svg')
            exit.click()  #clicking to the X.
            print('x CLICKED')
        except NoSuchElementException:
            print('x not found')

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(By.CLASS_NAME , "react-job-listing css-bkasv9 eigr9kq0")
        print(len(job_buttons))
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(mum)))
            if len(jobs) >= mum:
                break

            job_button.click()  # You might
            time.sleep(sleep_time)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, './/div[@class="employerName"]').text
                    location = driver.find_element(By.XPATH, './/div[@class="location"]').text
                    job_title = driver.find_element(By.XPATH, './/div[contains(@class, "title")]').text
                    job_description = driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text

                    collected_successfully = True
                except Exception:
                    time.sleep(sleep_time)

            try:
                salary_estimate = driver.find_element(By.XPATH, './/span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element(By.XPATH, './/span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element(By.XPATH, './/div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    headquarters = driver.find_element(By.XPATH,
                    './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element(By.XPATH,
                        './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH,
                        './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.XPATH,
                        './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(By.XPATH,
                        './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH,
                        './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH,
                        './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH,
                        './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("===================================================")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH ,'.//li[@class="nextButton css-1hq9k8 e13qs2071"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(mum, len(jobs)))
            break

    # This line converts the dictionary object into a pandas DataFrame.
    return pandas.DataFrame(jobs)
