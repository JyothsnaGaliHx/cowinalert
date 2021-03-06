import requests
import json
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
  
# api-endpoint
#URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"#?district_id=265&date=11-05-2021

# params
#pincode = "560076"
district="265"
# insert the start dates of the weeks you want to check vaccine availability for
dates = ["11-05-2021", "12-05-2021", "13-05-2021"]
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# sender's credentials
# you would have turn on 'access for less secure apps' for the sender's google account 
sender_email = 'Jyothsna.gali@gmail.com'
sender_pass = 'Jyo@44574'

# receiver's email
receiver_email = 'praveen.galli@gmail.com'

# re-check after time (in seconds)
recheck_after = 60

while True:
	for date in dates:
		PARAMS = {'district_id':district, 'date':date}
		print(date)
		r = requests.get(url = URL, params = PARAMS, headers = headers)
		print(r)
		data = r.json()
		#print(data)
		for center in data['centers']:
			name = center['name']
			addr = center['address']
			for session in center['sessions']:
				available_capacity = session['available_capacity']
				if available_capacity >0 :
					print(name)
					print(available_capacity)
				min_age_limit = session['min_age_limit']
				vaccine = session['vaccine']
				slot_date = session['date']
				if available_capacity > 0 and min_age_limit == 18 and vaccine == "COVISHIELD" :
					print('[!slot found] Vaccine available @ {0}, {1}'.format(name, addr))
					print('slots: {}, min age: {}, vaccine: {}, date: {}'.format(available_capacity, min_age_limit, vaccine, slot_date))
					mail_content = 'slots: {}, min age: {}, vaccine: {}, date: {}'.format(available_capacity, min_age_limit, vaccine, slot_date)
					message = MIMEMultipart()
					message['From'] = sender_email
					message['To'] = receiver_email
					message['Subject'] =  'Vaccine available @ {0}, {1}'.format(name, addr)
					message.attach(MIMEText(mail_content, 'plain'))
					session = smtplib.SMTP('smtp.gmail.com', 587)
					session.starttls()
					session.login(sender_email, sender_pass)
					text = message.as_string()
					session.sendmail(sender_email, receiver_email, text)
					session.quit()
					print('[info] Email sent')
	print('|', end="", flush=True)
	sleep(recheck_after)