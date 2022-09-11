import requests
from bs4 import BeautifulSoup

def extract_wwk_jobs(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}&button="
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"})

    jobs = []

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        job_not_fonund = soup.find("div", {"class": "no_results"})
        if job_not_fonund is None:
            job_container = soup.find('div', {'class': "jobs-container"})

            # remove view all ...
            for view_all in job_container.find_all("li", {"class": "view-all"}):
                view_all.decompose()
            
            jobs_list = job_container.find_all("li")
            for job_list in jobs_list:
                ### start extracting data
                logo = job_list.find('div', class_="flag-logo")
                if logo is None:
                    logo = ""
                else:
                    logo = logo['style']
                    logo = logo.replace('background-image:url(', '').replace(')', '')
                
                company_class = job_list.find_all('span', class_="company")
                company = company_class[0].get_text().replace(',', '‚')
                time = company_class[1].get_text().replace(',', '‚')

                position = job_list.find("span", {"class": "title"}).get_text().replace(',', '‚')

                location = job_list.find("span", {"class": "region company"}).get_text().replace(',', '‚')

                hrefs = job_list.find_all("a")
                link = hrefs[1]["href"]
                link = f"https://weworkremotely.com/{link}"

                job = {
                    "logo": logo,
                    "company": company,
                    "position": position,
                    "location": location,
                    "time": time,
                    "link": link
                }
                jobs.append(job)
                
    return jobs

#jobs = extract_wwk_jobs("aspdojapog")
#print(jobs)