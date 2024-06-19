from decimal import Decimal
import scrapy
from scrapy.responsetypes import Response
from scrapy.selector import Selector


class BcvSpider(scrapy.Spider):
    name = "BCV"
    # allowed_domains = [
    #     "example.com"
    #     ]
    start_urls = [
        "https://www.bcv.org.ve/tasas-informativas-sistema-bancario",
        ]
    
    
    def parse_selector_to_decimal(self, tasa:Selector) -> Decimal:
        """Convierte los textos de montos de la pagina en Decimales redondeados a 2 decimales
        Elimina los espacios y si está separado los decimales con comas, entonces se reemplaza por puntos

        Args:
            tasa (Selector): Un selector que contenga una tasa o un numero decimal

        Returns:
            Decimal: Lo retorna redondeado y en Decimal type
        """
        return Decimal(tasa.xpath("text()").get().strip().replace(",",".")).quantize(Decimal("0.00"))
    
    def parse_bancos(self,  tabla:list[Selector]):
        # results = []
        cells = tabla.xpath("tbody/tr")
        
        results:dict[str, list[dict[str,str]]] = {}
        
        for cell in cells:
            
            fecha, banco, tasa_compra, tasa_venta = cell.xpath("td")
            
            fecha = fecha.xpath("span/text()").get().strip()
            banco = banco.xpath("text()").get().strip()
            tasa_compra = self.parse_selector_to_decimal(tasa_compra)
            tasa_venta = self.parse_selector_to_decimal(tasa_venta)
            
            if fecha in results:
                results[fecha].append(
                    {
                        "BANCO": banco.upper(), 
                        "COMPRA": tasa_compra,
                        "VENTA": tasa_venta,
                    }
                )
            else:
                results[fecha] = [
                    {
                        "BANCO": banco.upper(), 
                        "COMPRA": tasa_compra,
                        "VENTA": tasa_venta,
                    }
                ]
            
            
            
            
        
        
        return results
    
    def parse_promedio(self, tabla:list[Selector]) -> dict[str, Decimal]:
        
        monedas = {
            "EUR": "/html/body/div[4]/div/div[2]/div/div[2]/div/div/section[1]/div/div[2]/div/div[3]/div/div/div[2]/strong",
            "USD": "/html/body/div[4]/div/div[2]/div/div[2]/div/div/section[1]/div/div[2]/div/div[7]/div/div/div[2]/strong",
        }
        
        results = {
            "EUR": Decimal("0.00"),
            "USD": Decimal("0.00")
        }
        
        selector = tabla[0]
        for key, xpath in monedas.items():
            value = self.parse_selector_to_decimal(selector.xpath(xpath))
            
            results[key] = value
        
        return results

    def parse(self, response:Response):
        tabla_tasa_bancos = response.xpath("/html/body/div[4]/div/div[1]/div/div/div/section/div/div[3]/div/table")
        tabla_promedios = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div/div/section[1]/div/div[2]/div")
        
        promedios = self.parse_promedio(tabla_promedios)
        bancos = self.parse_bancos(tabla_tasa_bancos)
        
        for fecha, tasas in bancos.items():
            yield {"fecha":fecha, "tasas": tasas}
 