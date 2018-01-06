# -*- coding: utf-8 -*-
from urllib.parse import quote
from urllib.request import urlopen
from flask import Flask, request,render_template, redirect, url_for, send_from_directory
from io import StringIO
from wapy.api import Wapy
import json
import os
import pandas as pd
from pandas.io.common import EmptyDataError
import datetime
import sched, time
import csv
import email
from bs4 import BeautifulSoup
from email.message import EmailMessage

import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("phaophaoespina@gmail.com", "09286916565")

fromaddr = "phaophaoespina@gmail.com"
toaddr = "stormmuhokushikiro@yahoo.com"




print("Email Connected, Proceeding...")









wapy = Wapy('d6n9afa6rtb5t27th5yqqe2m') # Create an instance of Wapy.




app = Flask(__name__)
#-----------------------------------------------------------------------------------------------

#PROBLEM START


#TIMER
def timer():
  timer = 0
  csv_file='C:\Python27\Walmart\sheet.csv'
  print("15 Minutes Have Passed! Updating sheet!...")
  data_df = pd.read_csv(csv_file)
  print("READ")
  for i, row in data_df.iterrows() :
      sku = data_df.iloc[i]['Walmart SKU']
      print (sku)
      if sku is not '':
        update(sku)
        print("Item Updating...")
       
      else:
        break

  print("Update on CSV Complete\n\n\n")
  background()



#UPDATE
def update(sku):

     lookup=str(sku)
     lookup = lookup.replace('.0', '')
     product = wapy.product_lookup(lookup)
     ts = time.time()

     st = datetime.datetime.today().strftime('%Y-%m-%d %I:%M %p')
     print (product.name)



     if product.available_online is 'TRUE':
        instock = 'yes'
     else:
        instock ='no'

     quote_page = product.product_url
     page = urlopen(quote_page)
     soup = BeautifulSoup(page, 'html.parser')
     sold_box = soup.find('a', attrs={'class': 'font-bold prod-SoldShipByMsg'})
     sold = sold_box.text.strip()


     pathto_csv = 'C:\Python27\Walmart\sheet.csv'
     data_df = pd.read_csv(pathto_csv)
     print("CSV READ")




     for i, row in data_df.iterrows() :
        data = data_df.iloc[i]['Walmart SKU']
        print(data)
        data = str(data)
        data = data.replace('.0', '')
        print(lookup)
        if data == lookup:
           old_dataLU = data_df.iloc[i]['Last Update']
           old_dataP = data_df.iloc[i]['Price']
           old_dataQ = data_df.iloc[i]['Quantity']
           old_dataMP = data_df.iloc[i]['Min Price']
           old_dataIN = data_df.iloc[i]['In Stock']
           old_dataSB = data_df.iloc[i]['Sold By']

  
           old_dataLU = str(old_dataLU)
           old_dataP = str(old_dataP)
           old_dataQ = str(old_dataQ)
           old_dataLMP = str(old_dataMP)





           st = str(st)
           print(st)
           data_df['Last Update'] = data_df['Last Update'].replace([old_dataLU], st)
           data_df['Price'] = data_df['Price'].replace([old_dataP], '$'+ str(product.sale_price))
#-----------------
           left_box = soup.find('div', attrs={'class': 'prod-ProductOffer-urgencyMsg'})
           if left_box:
              left = left_box.text.strip()

              stock=left
              data_df['Quantity'] = data_df['Quantity'].replace([old_dataQ], stock)
              if stock != old_dataQ:
                 msg = MIMEMultipart()
                 msg['From'] = fromaddr
                 msg['To'] = toaddr
                 msg['Subject'] = "Walmart Scraper Notification"
                 text = stock + ' for item ' + product.name + ' with SKU ' + lookup + 'check at' + 'https://www.walmart.com/ip/'+lookup
                 text = str(text)
                 msg.set_content(text)
                 server.send_message(msg)
                 print("Changes on" + product.name)
                 print("Email sent!")


           else:
             stock=product.stock
             data_df['Quantity'] = data_df['Quantity'].replace([old_dataQ], stock)
             print("Changes on" + product.name)
             print(stock)


#-----------------
           data_df['Min Price'] = data_df['Min Price'].replace([old_dataMP], '$'+str(product.msrp))
           data_df['In Stock'] = data_df['In Stock'].replace([old_dataIN], instock)
           data_df['Sold By'] = data_df['In Stock'].replace([old_dataSB], str(sold))
           print("Information update complete")
        else:
            print("Update on item Finished\n\n\n\n\n\n")
            break


   

     data_df.to_csv(pathto_csv, index=False)

     
     print(st)








#INTERFACE
@app.route("/background")
def background():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(15, 1, timer)
    s.run()
    return render_template("index.html")



#INTERFACE
@app.route("/")
def home():
    return render_template("index.html")



#-----------------------------------------------------------------------------------------------

#PROBLEM END



#ADD
@app.route("/lookup/", methods=['GET','POST'])
def lookup():

    filename = 'sheet.csv'
    pathto_csv = os.path.join('C:\Python27\Walmart',filename)

    if request.method == 'POST':
       try:
          data_df = pd.read_csv(pathto_csv, delimiter=',', encoding="utf-8-sig" )
          lookup=request.form['lookup']
          product = wapy.product_lookup(lookup)
          ts = time.time()

          st = datetime.datetime.today().strftime('%Y-%m-%d %I:%M %p')
          print (product.name)

          if product.available_online is 'TRUE':
            instock = 'yes'
          else:
            instock ='no'

          quote_page = product.product_url
          page = urlopen(quote_page)
          soup = BeautifulSoup(page, 'html.parser')
          sold_box = soup.find('a', attrs={'class': 'font-bold prod-SoldShipByMsg'})
          sold = sold_box.text.strip()
          left_box = soup.find('div', attrs={'class': 'prod-ProductOffer-urgencyMsg'})
          if left_box:
             left = left_box.text.strip()

 
             stock=left
             fields=[lookup + ',' + '$'+str(product.sale_price) + ',' + instock + ',' + stock + ',' + str(sold) + ',' + st + ',' + '$'+str(product.msrp)]
             with open('C:\Python27\Walmart\sheet.csv', 'a', newline='') as f:
                 writer = csv.writer(f, delimiter=' ', quotechar = ' ')
                 writer.writerow(fields)

          else:
             stock=product.stock
             fields=[lookup + ',' + '$'+str(product.sale_price) + ',' + instock + ',' + stock + ',' + str(sold) + ',' + st + ',' + '$'+str(product.msrp)]
             with open('C:\Python27\Walmart\sheet.csv', 'a', newline='') as f:
               writer = csv.writer(f, delimiter=' ', quotechar = ' ')
               writer.writerow(fields)




       except EmptyDataError:
          pass

       
       return render_template('success.html')

    else:
       return render_template('success.html')
            








