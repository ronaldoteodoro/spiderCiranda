#author - Ronaldo Teodoro | Capi Etherial
import scrapy

def extrairPropriedade(propriedade):
	dados = propriedade.css('::text').extract()[1:]
	return [dado.strip() for dado in dados]

class CirandaSpider(scrapy.Spider):
	name = "cirandaPersonagens"
	start_urls = ['https://www.cirandacultural.com.br/personagens']

	def parse(self, response):
		for item in response.css('center a ::attr(href)'):
			link = item.extract()
			personagens = link.replace("https://www.cirandacultural.com.br/products/vitrine/personagens-",'')
			link = "https://www.cirandacultural.com.br" + link
			personagens = personagens.replace('-',' ')
			yield response.follow(link,meta={'personagens':personagens} , callback=self.parseLinks)

	def parseLinks(self, response):
		for item in response.xpath('//figcaption//a'):
			personagens = response.meta['personagens']
			url = item.xpath('@href').extract()
			url = "https://www.cirandacultural.com.br" + "".join(url)
			yield response.follow(url,meta={'personagens':personagens} , callback=self.parseDadosLivro)
		personagens = response.meta['personagens']
		next_pages = response.css('.navigation a::attr(href)').extract()
		if next_pages:
			for next_page in next_pages:
				personagens = response.meta['personagens']
				yield response.follow(next_page,meta={'personagens':personagens} ,callback=self.parseLinks)

	def parseDadosLivro(self,response):
		ficha = response.css('.ficha-tecnica li')
		propriedades = [extrairPropriedade(propriedade) for propriedade in ficha]
		item = { "url": response.url, "personagens": response.meta['personagens'] }
		item.update(dict(propriedades))
		yield item