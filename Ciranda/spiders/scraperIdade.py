#author - Ronaldo Teodoro | Capi Etherial
import scrapy

def extrairPropriedade(propriedade):
	dados = propriedade.css('::text').extract()[1:]
	return [dado.strip() for dado in dados]

class CirandaSpider(scrapy.Spider):
	name = "cirandaIdades"
	start_urls = ['https://www.cirandacultural.com.br/idade']

	def parse(self, response):
		for item in response.css('center a ::attr(href)'):
			link = item.extract()
			idade = link.replace("/products/vitrine/selos-indicativos-",'')
			if (idade[:7] == 'leitora'):
				link = "https://www.cirandacultural.com.br" + link
				idade = idade.replace('leitora---','')
				yield response.follow(link,meta={'idade':idade} , callback=self.parseLinks)

	def parseLinks(self, response):
		for item in response.xpath('//figcaption//a'):
			idade = response.meta['idade']
			url = item.xpath('@href').extract()
			url = "https://www.cirandacultural.com.br" + "".join(url)
			yield response.follow(url,meta={'idade':idade} , callback=self.parseDadosLivro)
		idade = response.meta['idade']
		next_pages = response.css('.navigation a::attr(href)').extract()
		if next_pages:
			for next_page in next_pages:
				idade = response.meta['idade']
				yield response.follow(next_page,meta={'idade':idade} ,callback=self.parseLinks)

	def parseDadosLivro(self,response):
		ficha = response.css('.ficha-tecnica li')
		propriedades = [extrairPropriedade(propriedade) for propriedade in ficha]
		item = { "url": response.url, "idade": response.meta['idade'] }
		item.update(dict(propriedades))
		yield item