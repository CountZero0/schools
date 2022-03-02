import scrapy
from scrapy import Request


class SchoolSpider(scrapy.Spider):
    name = 'school'
    allowed_domains = ['swansea.gov.uk']
    start_urls = ['https://www.swansea.gov.uk/schoolcontactdetails']
                   #Gettin all category urls.
    def parse(self, response):
        for category_url in response.css('h2.item__title a::attr(href)').extract():
            yield response.follow(response.urljoin(category_url), callback=self.parse_school_links)
                   #Getting all needed urls inside category and entering the next page if needed.
    def parse_school_links(self, response):
        for school_url in response.css('h2.item__title a::attr(href)').extract():
            yield response.follow(response.urljoin(school_url), callback=self.parse_school)

        next_page = response.css('.paging__item--current+ .paging__item .paging__link::attr(href)').get()
        if next_page:
            yield Request(next_page, callback=self.parse_school_links)
                    #Collecting all needed data inside school page.
    def parse_school(self, response):
        school = response.css('dl.contact')
        yield {
            'school_title': school.css('dd.contact__value--name::text').get(),
            'head_teacher': school.css('dd.contact__value--job::text').get().strip(),
            'phoennumber': school.css('dd.contact__value--tel a::attr(href)').get()[4:],
            'e-mail': school.css('dd.contact__value--email a::attr(href)').get()[7:],
            'category': school.xpath('//div[3]/div/ol/li[5]/a/text()').get()
        }
