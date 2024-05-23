import scrapy


class MercadolivreiphoneSpider(scrapy.Spider):
    name = "mercadolivreIphone"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/iphone"]
    page_count=1
    max_page =15



    def parse(self, response):
        products = response.css('div.ui-search-result__content-wrapper')
        
        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            yield {
                    'brand' : product.css('h2.ui-search-item__title::text').get() if product.css('h2.ui-search-item__title::text').get()!=0 else "Não encontrado",
                    'valor_antigo': prices[0] if len(prices)>0 else None,
                    'Valor_atual': prices[0] if len(prices)==2 else prices[1],
                    'desconto': product.css('span.ui-search-price__discount::text').get() if product.css('span.ui-search-price__discount::text').get()!=0 else None,
                    'avaliacao': product.css('span.ui-search-reviews__rating-number::text').get() if product.css('span.ui-search-reviews__rating-number::text').get()!=0 else None,
                    'Quantidade de avaliação': product.css('span.ui-search-reviews__amount::text').get() if product.css('span.ui-search-reviews__amount::text').get()!=0 else None,
                    'Parcelamento': f"10x {prices[1]}" if len(prices)==2 else f"10x {prices[2]}",
                    'Observacao': product.css('span.ui-search-item__group__element.ui-search-item__variations-text::text').get() if product.css('cspan.ui-search-item__group__element.ui-search-item__variations-text::text').get()!=0 else None
                    }
            print(prices)
            print(len(prices))

        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count +=1
                yield scrapy.Request(url=next_page,callback=self.parse)
        pass
