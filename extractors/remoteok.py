from bs4 import BeautifulSoup
import re, requests

def extract_remoteok_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"})

    jobs = []

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        jobs_list = soup.find_all('tr', class_="job")
        for job_list in jobs_list:
            ### start extracting data
            img = job_list.find('img', class_="logo")
            logo = None
            if img is None:
                logo = ""
            else:
                logo = img['data-src']

            company = job_list.find('h3', {"itemprop": "name"}).get_text().strip().replace(',', '‚')
            
            title = job_list.find('h2', {"itemprop": "title"}).get_text().strip().replace(',', '‚')

            location = []
            salary = ""
            location_posts = job_list.find_all('div', class_="location")
            for location_post in location_posts:
                if location_post.string.find("💰") == -1:
                    location.append(location_post.string.replace(',', '‚'))
                else:
                    salary = location_post.string.replace(',', '‚')

            tag_info = job_list.find_all('td', class_="tags")
            tag = []
            for tags in tag_info:
                for tag_post in tags.find_all('h3'):
                    tag_post = tag_post.string.strip()
                    tag.append(tag_post)

            time_regex = re.compile(r'(\d+)([a-z])')
            time_group = time_regex.search(str(job_list.find_all('time')[0]))
            time = time_group.group().replace(',', '‚')

            link = job_list.find("a", {"itemprop": "url"})["href"]
            link = f"https://remoteok.com/{link}"

            ### value to list
            job = {
                "logo": logo,
                "company": company,
                "position": title,
                "location": location,
                "salary": salary,
                "tag": tag,
                "time": time,
                "link": link
            }
            jobs.append(job)
    
    return jobs

#jobs = extract_remoteok_jobs("aspdojapog")
#print(jobs)