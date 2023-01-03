from dataclasses import dataclass

from loguru import logger

from storage import Storage
from webinar import Webinar


@dataclass
class WebinarInfo:
    url: str
    title: str
    dates: str
    year: int

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, webinar_dict: dict) -> "WebinarInfo":
        return WebinarInfo(**webinar_dict)


class WebinarApi:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def import_webinar_from_url(self, url: str) -> int:
        try:
            webinar = Webinar.from_url(url)
        except Exception as err:  # pylint: disable=broad-except
            logger.exception("Could not create webinar", err)
            raise
        info = WebinarInfo(
            url=url,
            title=webinar.title,
            dates=webinar.date_str,
            year=webinar.year,
        )
        webinar_id = self.storage.add_webinar(info.to_dict())
        logger.info("Webinar added: %d", webinar_id)
        return webinar_id

    def list_webinars(self) -> list[dict]:
        return self.storage.list_webinars()

    def get_webinar(self, webinar_id: int) -> dict | None:
        return self.storage.get_webinar(webinar_id)

    def get_name_morph(self, name: str) -> str | None:
        """Suggest name in datv form"""
        return self.storage.get_name_morph(name)

    def set_name_morph(self, name: str, name_datv: str) -> None:
        """Store name and name in datv form as key-pair"""
        self.storage.set_name_morph(name, name_datv)
