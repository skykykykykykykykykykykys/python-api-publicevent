"""  API for Direktorat Sarana dan Prasarana ITB
     Ismail Faizal Aziz / 18217024
"""

#Scrapy Spider
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher


#HTTP Server & JSON
import http.server
from http.server import HTTPServer,SimpleHTTPRequestHandler
import base64
import cgi
import json

#URL Parser
from urllib.parse import urlparse

# Overwrite previous crawled data
#If not, previous data will make jsonDecodeError
fo = open("scraper_output.json", "w")
fo.write( "")
fo.close()

#Class Spider
class spider_scraper(scrapy.Spider):
     name = 'scraper_jadwal'
     index = 0
     custom_settings={ 'FEED_URI': "scraper_output.json",
                         'FEED_FORMAT': 'json'}

     def start_requests(self):
          url = "https://ditsp.itb.ac.id/sarana-dan-prasarana/status-peminjaman/"
          yield scrapy.Request(url=url, callback=self.parse)


     def parse(self, response):
          event_title = response.css("span.event-title::text")
          event_detail = response.xpath("//span[@class='calnk']/a/span/text()")
          for row in response.css("td.day-with-date"):
               event_tanggal = str(self.index + 1) + " " + response.css("td.calendar-month::text").get()
               yield {
                    "tanggal"     : event_tanggal,
                    "nama_fasil"   : event_title[self.index].get(),
                    "penggunaan"  : event_detail[self.index].get()
               }
               self.index = self.index + 1


#Fungsi spider_results akan melakukan proses crawling dengan class Spider yang telah dibuat dan menyimpan output dalam satu variabel
def spider_results():
     results = []

     def crawler_results(signal,sender,item,response,spider):
          results.append(item)
     dispatcher.connect(crawler_results, signal=signals.item_scraped)

     process = CrawlerProcess(get_project_settings())
     process.crawl(spider_scraper)
     process.start()

     return results

dataInfo = spider_results()

#load file hasil scraper
with open("scraper_output.json","r") as jadwal:
     data = json.load(jadwal)

#Class HTTP Request Handler
class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
     def do_GET(self):
          parsed_url = urlparse(self.path)
          path = parsed_url.path
          query = parsed_url.query
          if path == '/jadwal' :
               if query == '' :
                    #jika tanpa query, diberikan keseluruhan jadwal di bulan tersebut
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
               else :
                    #request handling dengan query tanggal
                    #keluaran = tanggal beserta nama peminjam dan peruntukkan fasilitas
                    param = query.split('=')[0]
                    if param == 'tanggal':
                         self.send_response(200)
                         self.send_header("Content-type", "application/json")
                         self.end_headers()
                         tanggal = int(query.split('=')[1])
                         data_tanggal= data[tanggal-1]['tanggal']
                         data_nama= data[tanggal-1]['nama_fasil']
                         data_used= data[tanggal-1]['penggunaan']
                         data_custom = "Tanggal : " + data_tanggal + "\nNama Peminjam dan Fasilitas yang digunakan " + data_nama + "\nPeruntukkan Fasilitas : " + data_used
                         self.wfile.write(json.dumps(data_custom).encode())
                    else :
                         #param gk ada
                         self.send_response(404)
                         self.send_header("Content-type", "text/html")
                         self.end_headers() 
          else :
               self.send_response(404)
               self.send_header("Content-type", "text/html")
               self.end_headers()

port = 8080
with HTTPServer(("",port), HTTPRequestHandler) as httpd:
     print("serving at port ",port)
     httpd.serve_forever()