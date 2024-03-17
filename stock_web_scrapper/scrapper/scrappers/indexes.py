import requests
from bs4 import BeautifulSoup
from ..models.indexes import Indexes

class GPWIndexes:
    model = Indexes
    url = "https://www.bankier.pl/gielda/notowania/indeksy-gpw"

    def scrap_indexes(self) -> None:
        response = self._get_site_response()
        indexes = self._parse_site_data(response)
        self._save_to_db(indexes)

    def _get_site_response(self):
        return requests.get(url=self.url, headers={"User-Agent": "Requests"})

    def _parse_site_data(self, response) -> list[str]:
        soup =  BeautifulSoup(response.text, "html.parser")
        return [index.text.strip() for index in soup.find_all("td", class_='colWalor')]

    def _save_to_db(self, indexes: list[str]) -> None:
        for index in indexes:
            obj, created = self.model.objects.update_or_create(
                ticker=index
            )
