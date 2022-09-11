from bs4 import BeautifulSoup
import re, requests


def extract_remoteok_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"})

    jobs = []

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        jobs_list = soup.find_all('tr', class_="job")
        for job in jobs_list:
            ### get html tags
            logo_info = job.find_all('td', class_="has-logo")
            company_info = job.find_all('td', class_="company_and_position")
            tag_info = job.find_all('td', class_="tags")
            time_info = job.find_all('time')

            ### start extracting data
            company = company_info[0].find("h3", {"itemprop": "name"}).get_text()
            title = company_info[0].find("h2", {"itemprop": "title"}).get_text()

            location = []
            salary = ""
            location_posts = company_info[0].find_all('div', class_="location")
            for location_post in location_posts:
                if location_post.string.find("💰") == -1:
                    location.append(location_post.string)
                else:
                    salary = location_post.string

            tag = []
            for tags in tag_info:
                for tag_post in tags.find_all('h3'):
                    tag.append(tag_post.string.replace('\n', ''))

            time_regex = re.compile(r'(\d+)([a-z])')
            time_group = time_regex.search(str(time_info[0]))
            time = time_group.group()

            ### clean up the values
            result = {
                "company": company,
                "position": title,
                "location": location,
                "salary": salary,
                "tag": tag,
                "time": time
            }
            jobs.append(result)
        
    return jobs

jobs = extract_remoteok_jobs("js")
print(jobs)