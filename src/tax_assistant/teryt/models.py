# coding: utf-8

from django.db import models

from .utils import xstr


class CommonInfo(models.Model):
    stan_na = models.DateField()
    aktywny = models.BooleanField(default=False)

    objects = models.Manager()

    def get_id(self):
        return self.id

    class Meta:
        abstract = True


# WMRODZ
class RodzajMiejscowosci(CommonInfo):
    id = models.CharField(max_length=2, primary_key=True)
    nazwa = models.CharField(max_length=30)

    def set_val(self, d):
        # {'RM': '01', 'STAN_NA': '2013-02-28', 'NAZWA_RM': u'wie\u015b'}
        print(d)
        self.id = d['RM']
        self.nazwa = d['NAZWA_RM']
        self.stan_na = d['STAN_NA']

    def __str__(self):
        return '{}: {}'.format(self.id, self.nazwa)


# SIMC
class MiastoManager(models.Manager):
    def get_queryset(self):
        return super(
            MiastoManager,
            self).get_queryset().filter(rodzaj_miejscowosci_id__exact='96')


class WiesManager(models.Manager):
    def get_queryset(self):
        return super(
            WiesManager,
            self).get_queryset().filter(rodzaj_miejscowosci_id__exact='01')


class Miejscowosc(CommonInfo):
    symbol = models.CharField(max_length=7, primary_key=True)
    jednostka = models.ForeignKey('JednostkaAdministracyjna', on_delete=models.CASCADE)
    miejscowosc_nadrzedna = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    nazwa = models.CharField(max_length=100)
    rodzaj_miejscowosci = models.ForeignKey('RodzajMiejscowosci', on_delete=models.CASCADE)

    woj = models.CharField(max_length=10, null=True)
    pow = models.CharField(max_length=10, null=True)
    gmi = models.CharField(max_length=10, null=True)
    rodz_gmi = models.CharField(max_length=10, null=True)
    rm = models.CharField(max_length=10, null=True)
    mz = models.CharField(max_length=10, null=True)

    miasta = MiastoManager()
    wsie = WiesManager()

    def get_id(self):
        return self.symbol

    def set_val(self, d):
        # {'GMI': '06', 'RODZ_GMI': '5', 'POW': '18', 'STAN_NA': '2013-03-06',
        #  'SYM': '0861110', 'NAZWA': 'Strzygowska Kolonia', 'WOJ': '04', 'RM':
        #  '02', 'SYMPOD': '0861110', 'MZ': '1'}
        self.symbol = d['SYM']
        self.nazwa = d['NAZWA']
        self.rodzaj_miejscowosci_id = d['RM']
        self.stan_na = d['STAN_NA']

        woj = d.get("WOJ")
        pow = d.get("POW")
        gmi = d.get("GMI")
        rodz_gmi = d.get("RODZ_GMI")
        rm = d.get("RM")
        mz = d.get("MZ")
        if d['SYMPOD'] != d['SYM']:
            self.miejscowosc_nadrzedna_id = d['SYMPOD']
        self.jednostka_id = (
            d['WOJ'] + xstr(d['POW']) + xstr(d['GMI']) + xstr(d['RODZ_GMI'])
        )

    def __str__(self):
        return '{}: {}'.format(self.symbol, self.nazwa)


# TERC
class WojewodztwoManager(models.Manager):
    def get_queryset(self):
        return super(WojewodztwoManager,
                     self).get_queryset().filter(typ__exact='WOJ')


class PowiatManager(models.Manager):
    def get_queryset(self):
        return super(PowiatManager,
                     self).get_queryset().filter(typ__exact='POW')


class GminaManager(models.Manager):
    def get_queryset(self):
        return super(GminaManager,
                     self).get_queryset().filter(typ__exact='GMI')


class JednostkaAdministracyjna(CommonInfo):
    LEN_TYPE = {
        7: 'GMI',
        4: 'POW',
        2: 'WOJ',
    }

    id = models.CharField(max_length=20, primary_key=True)
    nazwa = models.CharField(max_length=50)
    nazwa_dod = models.CharField(max_length=50)
    typ = models.CharField(max_length=20)

    woj = models.CharField(max_length=10, null=True)
    pow = models.CharField(max_length=10, null=True)
    gmi = models.CharField(max_length=10, null=True)
    rodz = models.CharField(max_length=10, null=True)

    wojewodztwa = WojewodztwoManager()
    powiaty = PowiatManager()
    gminy = GminaManager()

    def powiat(self):
        return JednostkaAdministracyjna.objects.get(id__exact=self.id[:4])

    def wojewodztwo(self):
        return JednostkaAdministracyjna.objects.get(id__exact=self.id[:2])

    def miejscowosci(self):
        return Miejscowosc.objects.filter(jednostka__id__startswith=self.id)

    def set_val(self, d):
        # {'GMI': None, 'POW': None, 'STAN_NA': '2013-01-01', 'NAZDOD':
        #  u'wojew\xf3dztwo', 'RODZ': None, 'NAZWA': u'DOLNO\u015aL\u0104SKIE',
        #  'WOJ': '02'}
        # {'GMI': '01', 'POW': '01', 'STAN_NA': '2013-01-01', 'NAZDOD':
        #  'gmina miejska', 'RODZ': '1', 'NAZWA': u'Boles\u0142awiec', 'WOJ':
        #  '02'}
        self.nazwa = d['NAZWA']
        self.nazwa_dod = d['NAZWA_DOD']
        self.stan_na = d['STAN_NA']
        self.woj = d.get("WOJ")
        self.pow = d.get("POW")
        self.gmi = d.get("GMI")
        self.rodz = d.get("RODZ")
        self.id = d['WOJ'] + xstr(d['POW']) + xstr(d['GMI']) + xstr(d['RODZ'])

        self.typ = self.LEN_TYPE[len(self.id)]
        if self.typ == 'WOJ':
            self.nazwa = self.nazwa.lower()

    def __str__(self):
        return '{}: {}'.format(self.id, self.nazwa)


# ULIC
class Ulica(CommonInfo):
    id = models.CharField(max_length=12, primary_key=True)
    miejscowosc = models.ForeignKey('Miejscowosc', on_delete=models.CASCADE)
    symbol_ulicy = models.CharField(max_length=10)
    cecha = models.CharField(max_length=10)
    nazwa_1 = models.CharField(max_length=100)
    nazwa_2 = models.CharField(max_length=100, null=True, blank=True)

    def set_val(self, d):
        # {'GMI': '03', 'RODZ_GMI': '2', 'NAZWA_1': 'Cicha', 'NAZWA_2': None,
        # 'POW': '03', 'STAN_NA': '2013-12-16', 'SYM': '0185962',
        # 'CECHA': 'ul.', 'WOJ': '08', 'SYM_UL': '02974'}
        self.id = d['SYM'] + d['SYM_UL']
        self.miejscowosc_id = d["SYM"]
        self.symbol_ulicy = d['SYM_UL']
        self.cecha = d['CECHA']
        self.nazwa_1 = d['NAZWA_1']
        self.nazwa_2 = d['NAZWA_2']
        self.stan_na = d['STAN_NA']

    def __str__(self):
        if self.nazwa_2:
            return '{s.cecha} {s.nazwa_2} {s.nazwa_1} '\
                '({s.miejscowosc.nazwa})'.format(s=self)
        return '{s.cecha} {s.nazwa_1} ({s.miejscowosc.nazwa})'.format(s=self)
