import scrapy

def extrairPropriedade(propriedade):
	dados = propriedade.css('::text').extract()[1:]
	return [dado.strip() for dado in dados]

class CirandaSpider(scrapy.Spider):
	with open("c:\\url.txt", "rt") as f:
		start_urls = [url.strip() for url in f.readlines()]
	name = "cirandaBusca"
	def parse(self,response):
		for item in response.xpath('//figcaption//a'):
			url = item.xpath('@href').extract()
			url = "https://www.cirandacultural.com.br" + "".join(url)
			yield response.follow(url, callback=self.parseDadosLivro)

	def parseDadosLivro(self,response):
		item = { "imageLink" : response.css('.slide-image .imageWrapper a ::attr(href)').extract()}
		ficha = response.css('.ficha-tecnica li')
		propriedades = [extrairPropriedade(propriedade) for propriedade in ficha]
		item.update({ "url": response.url})
		item.update(dict(propriedades))
		yield item