from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disabled-dev-shm-usage")

browser = webdriver.Chrome(options=options)

def get_page_count(keyword):
    #url = f"https://remoteok.com/remote-{term}-jobs"
    #res = requests.get(url, headers={"User-Agent": "Kimchi"})
    #soup = BeautifulSoup(res.text, "html.parser")
    
    browser.get(f"https://kr.indeed.com/jobs?q={keyword}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.select_one('nav[role=navigation]')
    if pagination == None or len(pagination) == 0:
        return 1

    pages_list = pagination.select('ul.pagination-list')

    if pages_list == None or len(pages_list) == 0:
        pages = pagination.select('div')
    else:
        pages = pagination.select('li')

    if pages is None:
        return 1
    else:
        count = len(pages)
        if count >= 5:
            return 5
        else:
            return count

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []

    for page in range(pages):
        print("find by page", page+1)
        print(f"request url: https://kr.indeed.com/jobs?q={keyword}&start={page*10}")

        browser.get(f"https://kr.indeed.com/jobs?q={keyword}&start={page*10}")
        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_list = soup.find('ul', class_="jobsearch-ResultsList")

        if job_list is not None:
            jobs = job_list.find_all('li', recursive=False)

            for job in jobs:
                zone = job.find('div', class_="mosaic-zone")
                if zone is None:
                    h2 = job.find('h2', class_="jobTitle")
                    anchor = job.select_one('h2 a')
                    title = anchor['aria-label']
                    link = anchor['href']
                    company = job.find('span', class_="companyName")
                    location = job.find('div', class_="companyLocation")

                    # ',' replace to ' ' for csv
                    job_data = {
                        'link': f"https://www.indeed.com{link.replace(',', '‚')}",
                        'company': company.string.replace(',', '‚'),
                        'location': location.string.replace(',', '‚'),
                        'position': title.replace(',', '‚')
                    }

                    results.append(job_data)

    return results