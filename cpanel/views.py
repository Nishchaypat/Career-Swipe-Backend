import sys
sys.path.append(r"C:\Users\npatel237\OneDrive - Georgia State University\CareerSwipe\cpanel")
from config import config
from config import cred as creds
from libraries import *

load_dotenv()
API=os.getenv("API")

class UploadFileForm(forms.Form):
    file = forms.FileField()

def file_ext(file_path,user_id):

   def to_markdown(text):
      text = text.replace('•', '  *')
      return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
   
   def read_pdf_from_url(url):
    response = requests.get(url)
   
   def pdf(file_path):
      #print("came to pdf method!!!")
      response = urllib.request.urlopen(file_path)
      pdf_content = response.read()


      with tempfile.NamedTemporaryFile(delete=False) as temp_file:

         temp_file.write(pdf_content)
         temp_file.seek(0)
         temp_file_path = temp_file.name

         pdf_reader = PyPDF2.PdfReader(temp_file)
         text = ""
         page = pdf_reader.pages[0]  
         page_text = page.extract_text()
         text += page_text
      response.close()
      return text

   def wdocx(file_url):
      response = requests.get(file_url)
      with tempfile.NamedTemporaryFile(delete=False) as temp_file:
         temp_file.write(response.content)
         temp_file_path = temp_file.name
      
         #print("1")
         try:
            doc = docx.Document(temp_file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
         except:
            #print("EXE")
            text = ""
            text = textract.process(temp_file_path, encoding='utf-8')
         #print("2")
         
      os.remove(temp_file_path)
      return text
   
   def txt(url):
      try:

         response = urllib.request.urlopen(url)
         content = response.read()
         text = content.decode('utf-8')
         response.close()
         
         return text
      except urllib.error.URLError as e:
         #print(f"Error: {e}")
         return None
   

   def resume_data(file_content, user_id):
      
      model = genai.GenerativeModel('gemini-pro') 
      genai.configure(api_key=API)
      chat = model.start_chat()  
      
      chat.send_message(file_content)  
      final = ''

      questions=['Your task is to extract the required data from the resume: Give the data of the following in a single json format: "Personal_Info" : Name, Email, Phone Number, and Location. "Education"  : University, GPA, Major and Minor. "Skills" : Such as 8 "programming skills", 5 "technological skills", 5 "behavioural skills". "Work_Experience": Position, Company, Location, Dates, Small "Summary" of that role. "Extracurricular_Activities": "Avtivity", "Role". "Links" Just give the https: links links present in this text. "Suggestions": Suggest 5 roles for this candidate. "Score" : Based on the candidates major, GPA, skills, experience give score out of 100. "Improvement_Suggestions" : List 3 things that this candidate do to improve the resume. "Projects": List 3 projects candidate can make to improve their skills.']
      for question in questions:
         response = chat.send_message(question)
         answer = response.text.replace('python', '').replace('```', '').replace('candidate_info = {', '').replace('json', '')
         final += answer
      global final_json
      final_json = json.loads(final)
      return final_json

   def file_read(file_path):
      if file_path.endswith('.txt') or '.txt' in file_path:
         return txt(file_path)
      elif file_path.endswith('.docx') or '.docx' in file_path:
         #print('its a word document')
         return wdocx(file_path)
      elif file_path.endswith('.pdf') or '.pdf' in file_path:
         return pdf(file_path)
      else:
         return 'Upload only PDF, DOCX, TXT. Try Again'

   #print('Made it')
   file_content=file_read(file_path)
   #print("PDF file reading done")
   data=resume_data(file_content,user_id)
   #print("getting text done")
   return data

def filter_candidate(requirements):
   model = genai.GenerativeModel('gemini-pro') 
   genai.configure(api_key=API)
   chat = model.start_chat()  
   cred = credentials.Certificate(creds)
   DB_URL="https://careerswipe-c08a4-default-rtdb.firebaseio.com/"
   ids=[]
   users=db.reference("/student")
   for u in users.get():
      gp=db.reference(f"/student/{u}/Education/GPA")
      g=gp.get()

      univ_stu=db.reference(f"/student/{u}/Education/University").get()

      program=[db.reference(f"/student/{u}/Education/Major").get(),db.reference(f"/student/{u}/Education/Minor").get()]

      try:
         if float(g)>=float(requirements['gpa']) and univ_stu==requirements['university'] and requirements['major'] in program :
            ids.append(u)
         else:
            pass
      except:
         pass
   print(ids)
   chat = model.start_chat()
   for x in ids:
      students=db.reference(f"/student/{x}")
      all_skills=db.reference(f"/student/{x}/Skills")
      all_exp=db.reference(f"/student/{x}/Work Experience")                         
      chat.send_message(f"Here are the skills and experience of student with ID: {x}: Skills: {all_skills.get()} and experience is {all_exp.get()}")

   response=chat.send_message(f"Here are my requirements in a dictionary format, can you return only student IDS in json format(sorted from best match to least match) in a list format only who best fit my requirements? {requirements}, please do not give any explanation or reasoning. Return only the id")
   results=response.text.replace("```", "")
   results=results.replace("json","")
   try:
      results= eval(results)
   except:
      import re
      regex = r'\[.*?\]'
      results = re.findall(regex, results)
      results= list(results)
   
   filtered_students={}
   final=[]
   x=0
   for i in results:
      data=get_data_rec(i)
      filtered_students[x]=data
      x+=1
   final.append(filtered_students)
   final.append(ids)
   return final


#######################################################################################################################################



firebase=pyrebase.initialize_app(config)
autho=firebase.auth()
database=firebase.database()
storage=firebase.storage()

global user

try:
   cred = credentials.Certificate(creds)
   firebase_admin.initialize_app(cred, {"databaseURL": config['databaseURL']})
except:
   print("Wrong CREDENTIALS!!!!!!!!!!!!!")

def info(request):
   return render(request,'info.html')


def firstspage(request):
   return render(request,'firstspage.html')

def signin(request):
   return render(request,'signin.html')

def Rsignin(request):
   return render(request,'Rsignin.html')

def signup(request):
   return render(request,'signup.html')

def Rsignup(request):
   return render(request,'Rsignup.html')

def postsignin(request):
      global user
      email=request.POST.get('email')
      password=request.POST.get('password')
      try:
         user=autho.sign_in_with_email_and_password(email,password)
         ##print(user['idToken']) 
         sessionId=user['idToken']
         request.session=str(sessionId)
      except:
         message="Invalid"
         return render(request,'signin.html',{"message":message})
      data_file=get_data(user['localId'])
      return render(request,'uploadsuccess.html',{'file':data_file})

def get_data(id):
   filtered_students={}
   ref = db.reference(f'/student/{id}')
   data=ref.get()
   filtered_students[0]=data
   return filtered_students

def get_data_rec(id):
   ref = db.reference(f'/student/{id}')
   data=ref.get()
   return data


def postRsignin(request):
      global user
      email=request.POST.get('email')
      password=request.POST.get('password')
      try:
         user=autho.sign_in_with_email_and_password(email,password)
         sessionId=user['idToken']
         request.session=str(sessionId)
      except:
         message="Invalid"
         return render(request,'Rsignin.html',{"message":message})
      return render(request,"search.html",{'e':email})


def logout(request):
   auth.logout(request)
   return render(request,('firstspage.html'))

def postsignup(request):
   name=request.POST.get('name')
   email=request.POST.get('email')
   password=request.POST.get('password')
   confirmpassword=request.POST.get('confirmpassword')
   if confirmpassword!=password:
      message="Password didnt match"
      return render(request,'signup.html',{"message":message})
   try:
      if email.endswith('.edu') and 'student' in email:
         user=autho.create_user_with_email_and_password(email,password)
         autho.send_email_verification(user['idToken'])
      else:
         message="Use only Student Email Address"
         return render(request,'signup.html',{"message":message})
   except:
      message="Unable to Login Try again"
      return render(request,'signup.html',{"message":message})
   try:
      user=autho.sign_in_with_email_and_password(email,password)
      sessionId=user['idToken']
      request.session=str(sessionId)
   except:
      message="Invalid"
      return render(request,'signup.html',{"message":message})
   return render(request,"welcome.html",{'e':email})


def postRsignup(request):
   name=request.POST.get('company_name')
   email=request.POST.get('hr_email')
   password=request.POST.get('password')
   confirmpassword=request.POST.get('confirmpassword')
   if confirmpassword!=password:
      message="Password didnt match"
      return render(request,'Rsignup.html',{"message":message})
   try:
      if email.endswith('.edu') and 'student' not in email:
         user=autho.create_user_with_email_and_password(email,password)
         autho.send_email_verification(user['idToken'])
      else:
         message="Use only Student Email Address"
         return render(request,'Rsignup.html',{"message":message})
   except:
      message="Unable to Login Try again"
      return render(request,'Rsignup.html',{"message":message})
   user_id=user['localId']
   data={'name':name,'status':'1'}
   database.child('recruiter').child(user_id).child('details').set(data)
   message='Check the link, sent to the email entered above, so we can confirm your email address'
   return render(request,'Rsignin.html',{"message":message})


def uploadfile(request):
   user=autho.current_user
   form=UploadFileForm(request.POST,request.FILES)
   if form.is_valid():
      user_id=user['localId']
      my_resume=request.FILES['file']
      other=request.FILES.getlist('other-file')
      my_resume_name=my_resume.name
      my_resume_name=user_id+my_resume_name
      storage.child(my_resume_name).put(my_resume)
      try:
         download_url = storage.child(my_resume_name).get_url(None)
         #print(download_url)
      except:
          return render(request,'welcome.html',{"message":'Retry upload'})
      #url='gs://careerswipe-c08a4.appspot.com/'+my_resume_name
      #web_path=(r'https://firebasestorage.googleapis.com/v0/b/careerswipe-c08a4.appspot.com/o/'+my_resume_name)
      data_file=file_ext(download_url,user_id)
      ref = db.reference(f'/student/{user_id}')
      ref.set(data_file)
      ref.child(str('Resume')).set(download_url)
      data_file=get_data(user_id)
      list_url=[]
      for i in other:
         print(i.name)
         storage.child(user_id+i.name).put(i)
         download_url = storage.child(user_id+i.name).get_url(None)
         list_url.append(download_url)
      ref.child(str('Other')).set(list_url)
      return render(request,'uploadsuccess.html',{'file':data_file})
   else:
      form=UploadFileForm()
      message='form not valid'
      return render(request,'welcome.html',{'form':form, 'message':message})

def reupload(request):
   global user
   user=autho.current_user
   sessionId=user['idToken']
   request.session=str(sessionId)
   return render(request,"welcome.html",{'e':user['email']})

def forgotpassword(request):
   return render(request,'forgotpassword.html')

def Rforgotpassword(request):
   return render(request,'Rforgotpassword.html')

def postforgotpassword(request):
   email=request.POST.get('email')
   autho.send_password_reset_email(email)
   return render(request,'signin.html')

def postRforgotpassword(request):

   email=request.POST.get('email')
   autho.send_password_reset_email(email)

   return render(request,'Rsignin.html')


def results(request):
   return render(request,'results.html')


def favourite(request):
   return render(request,'favourite.html')

def search(request):
   return render(request,'search.html')


def postfilter(request):
   if request.method == 'POST':
        skills = request.POST.getlist('skills[]') 
        gpa = request.POST.get('GPA')
        university = request.POST.get('uni')
        major = request.POST.get('major')
        experience = request.POST.get('exp')
        role=request.POST.get('role')
   
   filters={'role':role, 'skills':skills, 'gpa':gpa, 'university':university, 'major': major, 'experience':experience}
   data_file=None
   data_file=filter_candidate(filters)
   if not data_file[1]:
      return render(request,'results.html',{'file':'', 'ids':''})   
   #print('before',data_file[0])
   for i in data_file[0]:
      if data_file[0][i]==None:
         del data_file[0][i]
   #print(data_file[0])
   return render(request,'results.html',{'file':data_file[0], 'ids':data_file[1]})


@require_POST
def add_to_favorites(request):
   global user
   user = autho.current_user
   sessionId = user['idToken']
   request.session['idToken'] = str(sessionId)
   recruiter_id = user['localId']
   
   ref = db.reference(f'/recruiter/{recruiter_id}/students')
   
   student_id = request.POST.get('userId')
   #print("Received student ID:", student_id)
   existing_students = ref.get() or {}
   #print(existing_students)
   if student_id in existing_students:
      return JsonResponse({'status': 'Duplicate: Student already added'})
   next_index = len(existing_students)
   ref.update({student_id:'1'})
   return JsonResponse({'status': 'Added', 'index': next_index})

def favStudent(request):
   global user
   user = autho.current_user
   sessionId = user['idToken']
   request.session['idToken'] = str(sessionId)
   recruiter_id = user['localId']
   ref = db.reference(f'/recruiter/{recruiter_id}/students')
   existing_students = ref.get()
   filtered_students={}
   x=0
   res = []
   #print(existing_students)
   if type(existing_students)==dict:
      for val in existing_students:
         if val != None :
            res.append(val)
   # if type(existing_students)==list:
   #    for i in existing_students:
   #       if i != None :
   #          res.append(i)
   #print('hu',res)
   for i in res:
      if i is not None:
         data=get_data_rec(i)
         filtered_students[x]=data
         x+=1
   data_file=[]
   data_file.append(filtered_students)
   return render(request,'favourite.html',{'file':data_file[0],'ids':res})
   
   
@require_POST
def remove_from_favorites(request):
   global user
   user = autho.current_user
   sessionId = user['idToken']
   request.session['idToken'] = str(sessionId)
   recruiter_id = user['localId']
   ref = db.reference(f'/recruiter/{recruiter_id}/students')
   existing_students = ref.get() or {}
   
   student_id = request.POST.get('userId')
   key_to_remove = None
   #print('rem',existing_students)
   if type(existing_students)==dict:
      if type(existing_students)==dict:
         for val in existing_students:
            if val==student_id:
               key_to_remove=val
   # if type(existing_students)==list:
   #    for i in (existing_students):
   #       if i == student_id:
   #          key_to_remove = str(i)
   #          break
   #print(type(key_to_remove))
   if key_to_remove is None:
      return JsonResponse({'status': 'Not Found: Student ID not in favorites'}, status=404)
   if type(key_to_remove)==str:
      ref.child(key_to_remove).delete() 
   return JsonResponse({'status': 'Removed', 'studentId': student_id})