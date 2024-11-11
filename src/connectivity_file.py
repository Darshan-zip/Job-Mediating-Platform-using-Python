import mysql.connector
db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Darshan",
    database="db1"
)
curr=db.cursor()
'''name="adfdarhan"
age="37"
data=(name,age,34332552)
L=[]
query="INSERT INTO project(name,age,no) VALUES(%s,%s,%s)"
#curr.execute(query,data)
db.commit()
curr.execute("select name from project")
for i in curr:
    L.append(i[0])

print(L)
print("Hi")'''

'''s='darhan'
s=(s,)
curr.execute("SELECT COUNT(*) FROM project WHERE name = %s",s)
for i in curr:
    k=i[0]
print(k)'''

'''L=[]
s='darhan'
s=(s,)
curr.execute("select * from project where name like %s",s)
for i in curr:
    L.append(i)
print(L)'''

def jobseeker_insert(L, profile_path):
    print("ENTERED")
    L = tuple(L) + (profile_path,)
    query = """
    INSERT INTO jobseeker(
        name, age, dob, address, educational_qualifications, email, mobno, nationality,
        prev_exp, exp_years, prev_sal, expected_sal, mow, job_style, additional_skills,
        projects, certifications, ref, username, pass, profile_picture_path
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    curr.execute(query, L)
    db.commit()

def recruiter_insert(L, profile_path):
    print("ENTERED")
    L = tuple(L) + (profile_path,)
    query = """
    INSERT INTO recruiter(
        name, dob, address, rec_desig, rec_dept, exp_years, mob_no, email, avail_job_design, qualifications, 
        add_requirements, company_name, basic_pay, certifications, req_exp_years, industrial_sector, mow, 
        job_style, age_constraints, shift, working_hours, overall_description, username, pass, profile_picture_path
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    curr.execute(query, L)
    db.commit()




def get_usernames():
    L=[]
    curr.execute("select username from jobseeker")
    for i in curr:
        L.append(i[0])
    return L
def get_usernames_recruiter():
    L=[]
    curr.execute("select username from recruiter")
    for i in curr:
        L.append(i[0])
    return L

def get_record(s):
    L=[]
    s=(s,)
    curr.execute("select * from jobseeker where username like %s",s)
    for i in curr:
        L=list(i)
    return L
def get_record_recruiter(s):
    L=[]
    s=(s,)
    curr.execute("select * from recruiter where username like %s",s)
    for i in curr:
        L=list(i)
    return L
def check_existence_jobseeker(username):
    s=(username,)
    curr.execute("SELECT COUNT(*) FROM jobseeker WHERE username = %s",s)
    for i in curr:
        return i[0]

def verify_password_jobseeker(username):
    s=(username,)
    curr.execute("SELECT pass FROM jobseeker WHERE username = %s",s)
    for i in curr:
        return i[0]

def verify_password_recruiter(username):
    s=(username,)
    curr.execute("SELECT pass FROM recruiter WHERE username = %s",s)
    for i in curr:
        return i[0]
    
def check_existence_recruiter(username):
    s=(username,)
    curr.execute("SELECT COUNT(*) FROM recruiter WHERE username = %s",s)
    for i in curr:
        return i[0]

def change_password_jobseeker(username,password):
    s=(password,username)
    if check_existence_jobseeker(username)==1:
        curr.execute("update jobseeker set pass=%s where username=%s",s)
        db.commit()
        print("password changed successfully!")


def change_password_recruiter(username,password):
    s=(password,username)
    if check_existence_jobseeker(username)==1:
        curr.execute("update recruiter set pass=%s where username=%s",s)
        db.commit()
        print("password changed successfully!")


def get_reccommended_jobseekers(username):
    if Reccomendation_count(username)==True:
        curr.execute("select username,count from jobseeker where count>=3")
    L=[]
    for i in curr:
        L.append((i[0],i[1]))
    return L

def count_increment(username):
    s=(username,)
    curr.execute("update jobseeker set count=count + 1 where username=%s",s)
    db.commit()
    print("count incremented")

def count_set0():
    curr.execute("update jobseeker set count=0")
    db.commit()
    print("count set to 0")

def Reccomendation_count(username):
    
    usernames=get_usernames()
    rec=get_record_recruiter(username)
    #rec1=[rec[9],rec[12],rec[14],rec[16],rec[17],rec[18]]# without qualifications
    print(rec)
    for i in usernames:
        tempjob=get_record(i)
        if tempjob[11]<=rec[12]:
            count_increment(i)
        if tempjob[4]==rec[9]:
            count_increment(i)
        if tempjob[9]>=rec[14]:
            count_increment(i)
        if tempjob[12]==rec[16]:
            count_increment(i)
        if tempjob[13]==rec[17]:
            count_increment(i)
        if tempjob[1]>=int(rec[18][0:2]) and tempjob[1]<=int(rec[18][3:]):
            count_increment(i)
    return True
        


def search_bar_list(s):
    s=s+'%'
    s=(s,)
    L=[]
    curr.execute("select username,count from jobseeker where username like %s",s)
    for i in curr:
        L.append((i[0],i[1]))
    return L

#---------------

def count_increment_recruiter(username):
    s=(username,)
    curr.execute("update recruiter set count=count + 1 where username=%s",s)
    db.commit()
    print("count incremented")

def count_set0_recruiter():
    curr.execute("update recruiter set count=0")
    db.commit()
    print("count set to 0")

def count_increment_recruiter(username):
    s=(username,)
    curr.execute("update recruiter set count=count + 1 where username=%s",s)
    db.commit()
    print("count incremented")

def Reccomendation_count_recruiters(username):#updating recruiter table count
    
    usernames=get_usernames_recruiter()
    rec=get_record(username)#rec=jobseeker record
    #rec1=[rec[9],rec[12],rec[14],rec[16],rec[17],rec[18]]# without qualifications
    print(rec)
    for i in usernames:
        tempjob=get_record_recruiter(i)#rempjob=REcruiter record
        if tempjob[12]>=rec[11]:
            count_increment_recruiter(i)
        if tempjob[9]==rec[4]:
            count_increment_recruiter(i)
        if tempjob[14]>=rec[9]:
            count_increment_recruiter(i)
        if tempjob[16]==rec[12]:
            count_increment_recruiter(i)
        if tempjob[17]==rec[13]:
            count_increment_recruiter(i)
        if rec[1]>=int(tempjob[18][0:2]) and rec[1]<=int(tempjob[18][3:]):
            count_increment_recruiter(i)
    return True

def get_reccommended_recruiters(username):# getting reccomendations for recruiters
    Reccomendation_count_recruiters(username)
    curr.execute("select username,count from recruiter where count>=3")
    L=[]
    for i in curr:
        L.append((i[0],i[1]))
    return L
def edit_recruiter_profile(username):
    curr.execute("SELECT * FROM recruiter WHERE name=%s", (username,))
    return list(curr.fetchone())

def save_changes_recruiter(username, details):
    query = """
    UPDATE recruiters
    SET name = %s, dob = %s, address_no = %s, street = %s, area = %s, district = %s, city = %s, state = %s, pincode = %s
    WHERE name = %s
    """
    params = (*details, username)
    curr.execute(query, params)
    db.commit()

def search_jobseekers_byfilter(username,salary_range,mow,age,jobstyle):
    L=[]
    sal_lower="0"
    sal_upper="999999999"
    age_lower="18"
    age_upper="99"
    
    print(username,salary_range,mow,age,jobstyle)
    if username==None:
        username=""
        #else add % to the username b4 passing it via function
    if salary_range=="Expected Salary":
        sal_lower="0"
        sal_upper="999999999"
    if mow==None or mow=="Mode of Working":
        mow=""
    if age==None:
        age_lower="18"
        age_upper="99"
    if jobstyle==None:
        jobstyle=""
    if salary_range!=None:
        for i in range(len(salary_range)):
            if salary_range[i]=="-":
                sal_lower=str(salary_range[1:i])
                sal_upper=str(salary_range[i+2:])
    if age!=None:
        for i in range(len(age)):
            if age[i]=="-":
                age_lower=str(age[0:i])
                age_upper=str(age[i+1:])
    
    s="select username,count,profile_picture_path from jobseeker where username like '"+username+"%' and mow like '"+mow+"%' and job_style like '"+jobstyle+"%' and expected_sal<="+sal_upper+" and expected_sal>="+sal_lower+" and age<="+age_upper+" and age>="+age_lower
    print(s)
    curr.execute(s)
    for i in curr:
        L.append((i[0],i[1],i[2]))
    return L


def search_recruiters_byfilter(username,salary_range,mow,working_hours,jobstyle):
    L=[]
    sal_lower="0"
    sal_upper="999999999"
    working_hours_lower="0"
    working_hours_upper="99"
    
    print(username,salary_range,mow,working_hours,jobstyle)
    if username==None:
        username=""
        #else add % to the username b4 passing it via function
    if salary_range=="Expected Salary":
        sal_lower="0"
        sal_upper="999999999"
    if mow==None or mow=="Mode of Working":
        mow=""
    if working_hours==None:
        working_hours_lower="18"
        working_hours_upper="99"
    if jobstyle==None:
        jobstyle=""
    if salary_range!=None:
        for i in range(len(salary_range)):
            if salary_range[i]=="-":
                sal_lower=str(salary_range[1:i])
                sal_upper=str(salary_range[i+2:])
    if working_hours!=None:
        for i in range(len(working_hours)):
            if working_hours[i]=="-":
                working_hours_lower=str(working_hours[0:i])
                working_hours_upper=str(working_hours[i+1:])
    
    s="select username,count,profile_picture_path from recruiter where username like '"+username+"%' and mow like '"+mow+"%' and job_style like '"+jobstyle+"%' and basic_pay<="+sal_upper+" and basic_pay>="+sal_lower+" and working_hours<="+working_hours_upper+" and working_hours>="+working_hours_lower
    print(s)
    curr.execute(s)
    for i in curr:
        L.append((i[0],i[1],i[2]))
    return L

search_jobseekers_byfilter("Darshan",None,None,None,None)