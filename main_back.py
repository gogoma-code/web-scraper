from extractors.indeed import extract_indeed_jobs
from file import save_to_file

keyword = input("what do you want to search for?")
jobs = extract_indeed_jobs(keyword)

save_to_file(keyword, jobs)