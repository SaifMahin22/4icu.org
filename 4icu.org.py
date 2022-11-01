# ### Fetched University URL + University Name

# In[18]:


import requests
from bs4 import BeautifulSoup


response = requests.get('https://www.4icu.org/us/')
soup = BeautifulSoup(response.text, 'lxml'
all_a_tags = soup.find_all('a')

University_Url = []
for a in all_a_tags:
    if "/reviews/" in a['href']:
        University_Url.append(["https://www.4icu.org"+a['href'], a.text])     
University_Url = University_Url[1:]


# ## Function 

# In[109]:


def All_Information(soup):
    logo_path = "https://www.4icu.org"+soup.find('img', {"itemprop":"logo"})['src']
    university_website = soup.find('a',{"itemprop":"url"})['href']

    country_rank=""
    world_rank=""

    all_a_tags = soup.find_all('a')
    for a in all_a_tags:
        if "country rank" in a.text and country_rank=="":
            country_rank = a.parent.find_next_sibling('td').text

        elif "world rank" in a.text and world_rank=="":
            world_rank = a.parent.find_next_sibling('td').text 

    description = soup.find('p',{"itemprop":"description"}).text
    founding_year = soup.find('span',{"itemprop":"foundingDate"}).text

    street = soup.find('span',{"itemprop":"streetAddress"}).text
    locality = soup.find('span',{"itemprop":"addressLocality"}).text
    postal_code = soup.find('span',{"itemprop":"postalCode"}).text
    region = soup.find('span',{"itemprop":"addressRegion"}).text

    full_address = street+", "+locality+", "+postal_code+", "+region
    full_address = full_address.replace(' ,',",")

    telephone = soup.find('span',{"itemprop":"telephone"}).text.replace('+',"")

    #### Yearly Tution Range #######
    required_table = soup.find('h2', text="Yearly Tuition Range").parent.parent.find('table',{"class":"table text-center"})
    undergrade_students_cost = required_table.tbody.tr.strong.text.split(' US$ ')[0]+" US$"
    post_graduate_cost = required_table.tbody.tr.find_all('strong')[1].text.split(' US$ ')[0]+" US$"

    ##### student Enrollment ###### Academic Stuff 
    std_enrollment = soup.find('em',{"class":"sp student-enrollment"}).find_next_sibling('strong').text
    acdmic_stuff = soup.find('i',{"class":"sp academic-staff"}).find_next_sibling('strong').text
    acdmic_calender = soup.find('i',{"class":"sp academic-calendar"}).find_next_sibling('strong').text
    
    return [logo_path, university_website, country_rank, world_rank, description, founding_year, full_address, telephone, 
           undergrade_students_cost, post_graduate_cost, std_enrollment, acdmic_stuff, acdmic_calender]


# ### Fetching Results from Each University Page

# In[114]:


Records = []

r = requests.Session()
for univeristy_info in University_Url:

    university_url = univeristy_info[0]
    university_name = univeristy_info[1]
    
    ### Getting resonse #########
    response = r.get(university_url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    #### Fetching all required information ########
    information = All_Information(soup)
    
    Records.append([university_name, university_url] + information.copy())
    
    print(f'{university_name} | Country Rank: {information[2]}')


# ## Output ##

# In[116]:


import pandas as pd

df = pd.DataFrame(Records, columns=["University Name","University URL",'logo_path','university_website','country_rank','world_rank','description','founding_year','full_address','telephone','undergrade_students_cost','post_graduate_cost','std_enrollment','acdmic_stuff','acdmic_calender'])
df.to_csv('University Information.csv', index=False, encoding='utf-8')

