import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

# Define the URLs for the concerts
concert_urls = {
    "Concert 1": "https://ipo.pres.global/order/2242",
    "Concert 2": "https://ipo.pres.global/order/2243",
    "Concert 3": "https://ipo.pres.global/order/2244",
}

# Function to check ticket availability using text content analysis
def check_ticket_availability(url):
    try:
        options = webdriver.ChromeOptions()         # instantiate options 
        options.headless = True         # run browser in headless mode 
        options.add_argument("--headless")  # Ensure headless mode is enabled

        # instantiate driver 
        driver = webdriver.Chrome(service=ChromeService( 
            ChromeDriverManager().install()), options=options) 
        driver.get(url) # get the entire website content 

        # select elements by class name 
        elements = driver.find_elements(By.CLASS_NAME, 'error-title') 

        heading = ""
        for title in elements: 
            # select H2s, within element, by tag name 
            #print(title)
            heading = title.find_element(By.TAG_NAME, 'span').text 
            # print H2s 
            #print(type(heading))
        
        if len(heading)>2:
            return False
        else:
            return True
   
    except Exception as e:
        print(f"Error checking availability for {url}: {e}")
        return False
    
    finally:
        driver.quit()
    #driver.quit()
    
    

# Function to send an email
def send_email(concerts):
    from_email = "jerem.tob@gmail.com"
    to_email = "jerem.tob@gmail.com"
    subject = "Tickets Available for Concerts"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = "Tickets are available for the following concerts:\n\n"
    body += "\n".join(concerts)

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, "jemy2402")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main program loop
if __name__ == "__main__":
    while True:
        concerts_available = []
        for concert, url in concert_urls.items():
            is_available = check_ticket_availability(url)
            #print(is_available)
            if is_available:
                concerts_available.append(concert)
                print(f"{concert} tickets are available.")
            else:
                print(f"{concert} tickets are sold out.")

        '''if concerts_available:
            send_email(concerts_available)
        else:
            print("No tickets available at this time.")'''
        
        # Wait for 10 seconds before checking again
        #time.sleep(30)
