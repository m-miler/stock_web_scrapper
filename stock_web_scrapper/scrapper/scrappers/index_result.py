from .prices import PriceScrapper
from ..models.indexes import Indexes, IndexResult
import logging


class IndexResultScrapper(PriceScrapper):
    def __init__(self,
                 ticker: str,
                 start=None,
                 end=None,
                 interval: str = "d",):
        super().__init__(ticker, start, end, interval)


    def _save_to_db(self, data: str, ticker: str):
        if data:
            try:
                date, open_price, max_price, min_price, close_price, volume = data.split(',')
                index: Indexes = Indexes.objects.get(ticker=ticker)
                obj, created = IndexResult.objects.update_or_create(
                    index=index,
                    date=date,
                    open_price=open_price,
                    max_price=max_price,
                    min_price=min_price,
                    close_price=close_price,
                    volume=volume
                )
            except Exception as error:
                logging.error(error)
