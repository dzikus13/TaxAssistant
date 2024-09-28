from dataclasses import dataclass,field,asdict
from typing import Optional
import json


@dataclass
class Dane:
    Data: str
    Urzad: str
    Cel: str
    Podmiot_skladajacy_deklaracje: str
    rodzaj_podatnika: str
    NIP: int
    Pelna_nazwa: str
    Skrocona_nazwa: str
    Kraj: str
    Wojewodztwo: str
    Powiat: str
    Gmina: str
    Miejscowosc: str
    Nr_domu: int
    Kod_pocztowy: str
    Przedmiot_opodatkowania: str   
    Zwiezle_okreslanie_tresci_i_przedmiotu_czynnosci_cywilnoprawnej: str
    Podatek_do_zaplaty: int
    Miejsce_polozenia_rzeczy_lub_miejsce_wykonywania_prawa_majatkowego : Optional[str] = field(default=None)
    Miejsce_dokonania_czynnosci_cywilnoprawnej: Optional[str] = field(default=None)
    Ulica: Optional[str] = field(default=None)
    Nr_lokalu: Optional[int] = field(default=None)
    Rodzaj_czynnosci_cywilnoprawnej: Optional[str] = field(default=None)
    Typ_spolki: Optional[str] = field(default= None)
    Dodatkowe_wojewodztwo: Optional[str] = field(default=None)
    Dodatkowy_powiat: Optional[str] = field(default=None)
    Dodatkowa_gmina: Optional[str] = field(default=None)
    Dodatkowa_miejscowosc: Optional[str] = field(default=None)
    Dodatkowa_ulica: Optional[str] = field(default=None)
    Dodatkowy_nr_domu: Optional[int] = field(default=None)
    Dodatkowy_nr_lokalu: Optional[int] = field(default=None)
    Dodatkowy_kod_pocztowy: Optional[str] = field(default=None)


    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        
        return Dane(
            Data=data['Data'],
            Urzad=data['Urzad'],
            Cel=data['Cel'],
            Podmiot_skladajacy_deklaracje=data['Podmiot_skladajacy_deklaracje'],
            rodzaj_podatnika=data['rodzaj_podatnika'],
            NIP=data['NIP'],
            Pelna_nazwa=data['Pelna_nazwa'],
            Skrocona_nazwa=data['Skrocona_nazwa'],
            Kraj=data['Kraj'],
            Wojewodztwo=data['Wojewodztwo'],
            Powiat=data['Powiat'],
            Gmina=data['Gmina'],
            Miejscowosc=data['Miejscowosc'],
            Nr_domu=data['Nr_domu'],
            Kod_pocztowy=data['Kod_pocztowy'],
            Przedmiot_opodatkowania=data['Przedmiot_opodatkowania'],
            Zwiezle_okreslanie_tresci_i_przedmiotu_czynnosci_cywilnoprawnej=data['Zwiezle_okreslanie_tresci_i_przedmiotu_czynnosci_cywilnoprawnej'],
            Podatek_do_zaplaty=data['Podatek_do_zaplaty'],
            Miejsce_polozenia_rzeczy_lub_miejsce_wykonywania_prawa_majatkowego=data.get('Miejsce_polozenia_rzeczy_lub_miejsce_wykonywania_prawa_majatkowego'),
            Miejsce_dokonania_czynnosci_cywilnoprawnej=data.get('Miejsce_dokonania_czynnosci_cywilnoprawnej'),
            Ulica=data.get('Ulica'),
            Nr_lokalu=data.get('Nr_lokalu'),
            Rodzaj_czynnosci_cywilnoprawnej=data.get('Rodzaj_czynnosci_cywilnoprawnej'),
            Typ_spolki= data.get('Typ_spolki'),
            Dodatkowe_wojewodztwo=data.get('Dodatkowe_wojewodztwo'),
            Dodatkowy_powiat=data.get('Dodatkowy_powiat'),
            Dodatkowa_gmina=data.get('Dodatkowa_gmina'),
            Dodatkowa_miejscowosc=data.get('Dodatkowa_miejscowosc'),
            Dodatkowa_ulica = data.get('Dodatkowa_ulica'),
            Dodatkowy_nr_domu= data.get('Dodatkowy_nr_domu'),
            Dodatkowy_nr_lokalu= data.get('Dodatkowy_nr_lokalu'),
            Dodatkowy_kod_pocztowy= data.get('Dodatkowy_kod_pocztowy'))
    def to_json(self):
        return json.dumps(asdict(self))