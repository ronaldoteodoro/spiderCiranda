#author - Ronaldo Teodoro | Capi Etherial
import scrapy

def extrairPropriedade(propriedade):
	dados = propriedade.css('::text').extract()[1:]
	return [dado.strip() for dado in dados]

class CirandaSpider(scrapy.Spider):
	name = "cirandaTema"
	start_urls = ['https://www.cirandacultural.com.br/temas']

	def parse(self, response):
		for item in response.css('center a ::attr(href)'):
			link = item.extract()
			tema = link.replace("https://www.cirandacultural.com.br/products/vitrine/temas-",'')
			link = "https://www.cirandacultural.com.br" + link
			tema = tema.replace('-',' ')
			yield response.follow(link,meta={'tema':tema} , callback=self.parseLinks)

	def parseLinks(self, response):
		for item in response.xpath('//figcaption//a'):
			tema = response.meta['tema']
			url = item.xpath('@href').extract()
			url = "https://www.cirandacultural.com.br" + "".join(url)
			yield response.follow(url,meta={'tema':tema} , callback=self.parseDadosLivro)
		tema = response.meta['tema']
		next_pages = response.css('.navigation a::attr(href)').extract()
		if next_pages:
			for next_page in next_pages:
				tema = response.meta['tema']
				yield response.follow(next_page,meta={'tema':tema} ,callback=self.parseLinks)

	def parseDadosLivro(self,response):
		ficha = response.css('.ficha-tecnica li')
		propriedades = [extrairPropriedade(propriedade) for propriedade in ficha]
		item = { "url": response.url, "tema": response.meta['tema'] }
		item.update(dict(propriedades))
		yield item