import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    # allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/iphone"]
    page_count=1
    max_page =15


    def parse(self, response):
        products = response.css('div.ui-search-result__content-wrapper')
        
        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            yield {
                    'brand' : product.css('h2.ui-search-item__title::text').get(),
                    'valor_antigo': prices[0] if len(prices)>0 else None,
                    'Valor_atual': prices[1] if len(prices)>1 else None,
                    'desconto': product.css('span.ui-search-price__discount::text').get(),
                    'avaliacao': product.css('span.ui-search-reviews__rating-number::text').get(),
                    'Quantidade de avaliação': product.css('span.ui-search-reviews__amount::text').get(),
                    }

        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)')
            if next_page:
                self.page_count +=1
                yield scrapy.Request(url=next_page,callback=self.parse)
            
                       
