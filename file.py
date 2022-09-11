def save_to_file(file_name, by, jobs):
    file = open(f"{file_name}.csv", "w")
    
    #file.write("Position,Company,Location,Link\n")
    if by == "all":
        file.write("Company,Position,Location,Time&Salary,Tag,Link\n")
        for job in jobs:
            if type(job['location']) is list:
                location = ':'.join(job['location'])
            else:
                location = job['location']
            
            if 'salary' in job:
                salary = " & " + job['salary']
            else:
                salary = ""
            
            if 'tag' in job:
                tag = ':'.join(job['tag'])
            else:
                tag = ""
            
            file.write(f"{job['company']},{job['position']},{location},{job['time']}{salary},{tag},{job['link']}\n")
    elif by == "remoteok":
        file.write("Company,Position,Location,Time&Salary,Tag,Link\n")
        for job in jobs:
            file.write(f"{job['company']},{job['position']},{':'.join(job['location'])},{job['time']} & {job['salary']},{':'.join(job['tag'])},{job['link']}\n")
    elif by == "wwk":
        file.write("Company,Position,Location,Time,Link\n")
        for job in jobs:
            file.write(f"{job['company']},{job['position']},{job['location']},{job['time']},{job['link']}\n")

    file.close()
