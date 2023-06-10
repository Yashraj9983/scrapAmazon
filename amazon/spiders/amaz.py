import scrapy


class AmazSpider(scrapy.Spider):
    name = "amaz"
    allowed_domains = ["amazon.in"]
    start_urls = ["file:///C:/Users/Administrator/Documents/scrapy_test/amazon/amazon.html"]
    # file:///C:/Users/Administrator/Documents/scrapy_test/amazon/amazon.html
    # https://www.amazon.in/Amazon-Wireless-Receiver-Optical-Tracking/dp/B09SMYXXM2
    # https://amazon.in/dp/B09SMYXXM2/
    # HEADERS = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #     "Accept-Language": "en-US,en;q=0.5",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Connection": "keep-alive",
    #     "Upgrade-Insecure-Requests": "1",
    #     "Sec-Fetch-Dest": "document",
    #     "Sec-Fetch-Mode": "navigate",
    #     "Sec-Fetch-Site": "none",
    #     "Sec-Fetch-User": "?1",
    #     "Cache-Control": "max-age=0",
    # }

    # def start_requests(self):
    #     for url in self.url_list:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=self.HEADERS)

    def parse(self, response):
        # url=response.url
        asin=response.css("#asin::attr('value')").get()
        title=response.css("span#productTitle::text").get().strip()
        brand= response.css("#bylineInfo::text").get()[7:]
        mrp=response.css(".a-text-price span.a-offscreen::text").get()
        price=response.css(".priceToPay span.a-offscreen::text").get()
        availability=response.css("#availability span::text").get().strip()
        productUrl="www.amazon.in/dp/"+asin
        qnaUrl="www.amazon.in/ask/questions/asin/"+asin
        reviewsUrl="www.amazon.in/product-reviews/"+asin
        questions_answered=response.css("#askATFLink span::text").get().strip().split(" ")[0]
        total_ratings=response.css("#acrCustomerReviewText::text").get().strip().split(" ")[0]
        avg_star_rating=response.css("#acrPopover span a span.a-size-base::text").get().strip()

        # prep=lambda st: "".join([x for x in st if str.isalnum(x)])
        prod_details=[]
        for table in response.css("#prodDetails table"):
            t1={}
            for row in table.css("tr"):
                k=row.css("th::text").get().strip()
                v=row.css("td::text").get().encode("ascii",errors="ignore").decode().strip()
                if v=="":
                    v=row.css("td #acrPopover a span::text").get()
                if v=="" or v==None:
                    v=row.css("td span span::text").get()[:-1] 
                    # v+=row.css("td a::text").get()+")"   
                if v!=None:
                    v=v.strip()
                t1[k]=v
            if len(t1)>0:    
                prod_details.append(t1)    

        yield {
            "productUrl":productUrl,
            "asin":asin,
            "title":title,
            "brand":brand,
            "mrp":mrp,
            "price":price,
            "availability":availability,
            "total_questions_answered":questions_answered,
            "total_ratings":total_ratings,
            "avg_star_rating":avg_star_rating,
            "reviewsUrl":reviewsUrl,
            "qnaUrl":qnaUrl,
            "product_details":prod_details,
        }
