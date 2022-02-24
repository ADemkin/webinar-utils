"""
Трансформировать имя из именительного в дательный падеж.

alternative solution: https://github.com/petrovich/pytrovich
"""

from functools import lru_cache
from typing import Any

from requests import request
from requests import Response


MORPHER_URL = 'https://ws3.morpher.ru/russian/declension'


class WordMorphError(Exception):
    @classmethod
    def from_resp(cls, response: Response) -> 'WordMorphError':
        status = response.status_code
        message = response.json()['message']
        return cls(f"Status {status!r}: {message!r}")


@lru_cache
def get_morph_data(fio: str) -> dict[str, str]:
    """Get response from morpher.ru

    raises WordMorphError

    Documentation:
    * https://morpher.ru/ws3/#declension
    * https://morpher.ru/ws3/#fio-split
    """
    resp = request('get', MORPHER_URL, params={'s': fio, 'format': 'json'})
    if not resp.ok:
        raise WordMorphError.from_resp(resp)
    return resp.json()


class Morph:
    def __init__(self, data: dict[str, Any], fio: str) -> None:
        self.data: dict[str, Any] = data
        self.fio = fio

    def __repr__(self) -> str:
        return '<NameMorph data={self.data}>'

    @classmethod
    def from_fio(cls, fio: str) -> 'Morph':
        return cls(data=get_morph_data(fio), fio=fio)

    @property
    def fio_given(self) -> str:
        return self.data['Д']

    @property
    def name(self) -> str:
        return self.data['ФИО']['И']


def run_tests() -> None:
    import pytest  # pylint: disable=import-outside-toplevel

    # test conversion
    name_form_and_given_form = [
        (
            'Пупкин Василий Александрович',
            'Пупкину Василию Александровичу',
            'Василий',
        ),
    ]
    for fio, fio_given, just_name in name_form_and_given_form:
        morph = Morph.from_fio(fio)
        assert morph.fio == fio
        assert morph.fio_given == fio_given
        assert morph.name == just_name

    # test service error
    with pytest.raises(WordMorphError) as err:
        Morph.from_fio("not in russian")
    err_expected = "Status 496: 'Не найдено русских слов.'"
    assert str(err.value) == err_expected, err.value

    print('tests OK')


if __name__ == '__main__':
    run_tests()
