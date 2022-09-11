from flask import Flask, render_template, request, redirect, send_file
from file import save_to_file
from extractors.remoteok import extract_remoteok_jobs
from extractors.wwk import extract_wwk_jobs

app = Flask("jobScrapper")

title = "Job-Search"

all_db = {}
remoteok_db = {}
wwk_db = {}

@app.route("/")
def index():
    return render_template("index.html", title=title)

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect("/")

    if keyword in all_db:
        jobs_remoteok = remoteok_db[keyword]
        jobs_wwk = wwk_db[keyword]
    else:
        jobs_remoteok = extract_remoteok_jobs(keyword)
        jobs_wwk = extract_wwk_jobs(keyword)
        
        all_db[keyword] = jobs_remoteok + jobs_wwk
        remoteok_db[keyword] = jobs_remoteok
        wwk_db[keyword] = jobs_wwk

    return render_template("search.html", title=title, keyword=keyword, jobs_remoteok=jobs_remoteok, jobs_wwk=jobs_wwk)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    by = request.args.get("by")

    if keyword is None:
        return redirect("/")
    if keyword not in all_db:
        return redirect("/search?keyword={keyword}&export=Y")
    
    file_name = f"{keyword}-{by}"
    if by is None or by == "all":
        save_to_file(file_name, by, all_db[keyword])
    elif by == "remoteok":
        save_to_file(file_name, by, remoteok_db[keyword])
    elif by == "wwk":
        save_to_file(file_name, by, wwk_db[keyword])

    return send_file(f"{file_name}.csv", as_attachment=True)

app.run("0.0.0.0")