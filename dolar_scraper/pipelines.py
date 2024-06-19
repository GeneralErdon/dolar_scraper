# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

from dolar_scraper.models import Banco, Tasa, create_table, db_connect
from dolar_scraper.types import TBancoTasa, TDolarItem


class DolarScraperPipeline:
    
    def __init__(self) -> None:
        self.engine = db_connect(os.getenv("DATABASE_URI", "sqlite:///dolar.db"))
        self.Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
    
    def open_spider(self, spider):
        self.session = self.Session()
    
    def close_spider(self, spider):
        """
        This method is called when the spider is closed.
        """
        self.session.close()
    
    def save_model(self, model):
        self.session.add(model)
        self.session.commit()
    
    def process_item(self, item:TDolarItem, spider):
        """Procesa los items provenientes del bcv.py
        el item recibe la siguiente estructura:
        {
            "DD-MM-YYYY": [
                {
                    "BANCO": str,
                    "COMPRA": Decimal
                    "VENTA": Decimal
                }
            ]
        }

        """
        
        fecha = datetime.strptime(
            item["fecha"], "%d-%m-%Y"
        ).date()
        tasas = item["tasas"]
        
        for tasa in tasas:
            
            banco = self.session.query(Banco).filter_by(name = tasa["BANCO"]).first()
            if not banco:
                banco = Banco(name=tasa["BANCO"])
                self.save_model(banco) # Se ha creado el banco nuevo
            
            # Chequear la fecha de la tasa a ver si existe
            existing_tasa = self.session.query(Tasa).filter_by(banco=banco.id, fecha=fecha).first()
            
            if not existing_tasa:
                new_tasa = Tasa(
                    banco=banco.id,
                    usd_compra=tasa["COMPRA"],
                    usd_venta=tasa["VENTA"],
                    fecha=fecha,
                )
                self.save_model(new_tasa)
        
        
        return item
