from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from sys import exit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_LOGIN_ID = "your-Howard--id-here"
USER_LOGIN_PIN = "your-Howard--pin-here"
TERM = "select term"
SUBJECT = "select subject"
COURSE_NUM = "select course number"
SECTION = "course section"
SEARCH_BY = "SEL_CRSE" #Dont change
PATH = "/Users/birajdahal/Desktop/Selenium/chromedriver_mac64/chromedriver" # change it to your file path after downloading chrome driver
CONST_BUTTON= "View Sections" #Dont Change



def make_object(wrapper, tag, tagname):
    try:
        return wait.until(EC.presence_of_element_located((tag, tagname)))
    except:
        print(f"One of your USER_LOGIN_ID: {USER_LOGIN_ID} or USER_LOGIN_PIN: {USER_LOGIN_PIN} is incorrect.")
        exit()

def send_data_to_website(obj, input_command):
    try:
        obj.send_keys(input_command)
    except:
        print("Error")
        exit()

def object_click(obj):
    obj.click()

def select_object(wrapper, tag, tagname):
    return Select(wrapper.find_element(tag,tagname))

def specify_attribute(obj, attr):
    return obj.get_attribute(attr)



driver = webdriver.Chrome(PATH)
try:
    driver.get("https://ssb-prod.ec.howard.edu/PROD/twbkwbis.P_WWWLogin")
except:
    print("Your PATH file is wrong to the ChromeDriver Directory. Please make sure you download it, and put the path in PATH variable above.")
wait = WebDriverWait(driver, 5)

try:
    user_name = make_object(wrapper = driver, tag = "id", tagname = "UserID")
    user_PIN = make_object(wrapper = driver, tag = "id", tagname = "PIN")
 
    send_data_to_website(obj = user_name, input_command=USER_LOGIN_ID) 
    send_data_to_website(obj=user_PIN, input_command = USER_LOGIN_PIN)
    send_data_to_website(obj = user_PIN,input_command = Keys.RETURN)
    
    Student_Servises_button = make_object(wrapper = driver, tag = "id", tagname = "bmenu--P_StuMainMnu___UID1")
    send_data_to_website(obj = Student_Servises_button,input_command = Keys.RETURN)

    Registration_hover = make_object(wrapper = driver, tag = "id", tagname = 'bmenu--P_RegMnu___UID2')
    object_click(obj=Registration_hover)

    
    LookUp = make_object(wrapper = driver, tag = "id", tagname = 'contentItem12')
    object_click(obj=LookUp)
    
    select_term = Select(make_object(wrapper = driver, tag = "name", tagname = 'p_term'))
    try:
        select_term.select_by_visible_text(TERM)
    except:
        print(f"Term you selected {TERM} is in incorrect format or not available. Please Check exactly according to Scroll Down Menu and Enter.")
        exit()

    SubmitButton = make_object(wrapper = driver, tag = "id", tagname = "id____UID6")
    object_click(obj=SubmitButton)
    
    select_subject = Select(make_object(wrapper = driver, tag = "xpath", tagname = '//select[@name="sel_subj"]'))
    try:
        # send_data_to_website(obj = select_subject, input_command=SUBJECT)
        select_subject.select_by_visible_text(SUBJECT)
    except:
        print(f"Subjected you entered {SUBJECT} is not in list. Please be sure to enter it correctly character by character.")
        exit()


    SubmitButton2 = make_object(wrapper = driver, tag = "id", tagname ="id____UID4") 
    object_click(obj=SubmitButton2)

    forms = driver.find_elements("xpath",'//form')  #array

    found = False

    for form in forms:
        inputs = form.find_elements("xpath",'.//input[@type="hidden"]')  #array
        for inp in inputs:
            if specify_attribute(inp, "name") == SEARCH_BY  and specify_attribute(inp, "value")  == COURSE_NUM:
                buttons = form.find_elements("xpath",'.//button') #array
                for button in buttons:
                    if specify_attribute(button, "value") == CONST_BUTTON:
                        object_click(button)
                        found = True
                        break
            if found:
                break
        if found:
            break
    if not found:
        print("Could not find the course number you provided:", COURSE_NUM)


    table = make_object(wrapper = driver, tag = "class name", tagname ="datadisplaytable") 
    rows = table.find_elements("xpath",'.//tr') # array
    
    all_sections_arr = [] 
    for row in rows[2:]:
        each_data = row.find_elements("xpath",'.//td') # array
        temp_arr = []
        for i in each_data:
            temp_arr.append(i.text)
        all_sections_arr.append(temp_arr)
    
    helper_set = set(each[4] for each in all_sections_arr)
    if SECTION not in helper_set:
        print("Could not find the section number you provided:", SECTION)
        exit()
    sec_found = False
    for each in all_sections_arr:
        if each[4] == SECTION and int(each[12]) > 0:
            print("Its Available.")
            exit()
            
    print("Its Not Available.")
    

except Exception as e:
    print(e)
finally:
    driver.quit()