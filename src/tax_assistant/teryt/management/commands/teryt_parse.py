from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, DatabaseError, IntegrityError
import csv

from teryt.models import (
    RodzajMiejscowosci, JednostkaAdministracyjna, Miejscowosc, Ulica
)


class Command(BaseCommand):
    args = '[xml file list]'
    help = 'Import TERYT data from CSV files prepared by GUS'

    def add_arguments(self, parser):
        parser.add_argument('WMRODZ', nargs=1, type=str, help='evid')
        parser.add_argument('TERC', nargs=1, type=str, help='marid')
        parser.add_argument('SIMC', nargs=1, type=str, help='marid')
        parser.add_argument('ULIC', nargs=1, type=str, help='marid')

    def handle(self, *args, **options):
        print(args)
        print(options)
        fn_dict = {
            'WMRODZ': RodzajMiejscowosci,
            'TERC': JednostkaAdministracyjna,
            'SIMC': Miejscowosc,
            'ULIC': Ulica,
        }

        for key, value in options.items():
            if key in fn_dict:
                c = fn_dict[key]
            else:
                continue

            a = value[0]
            try:
                with transaction.atomic():
                    c.objects.all().update(aktywny=False)
                    with open(a, encoding='utf-8-sig') as f:
                        reader = csv.DictReader(f, delimiter=';')

                        for vals in reader:
                            print(vals)
                            t = c()
                            t.set_val(vals)
                            t.aktywny = True
                            items = c.objects.filter(pk=t.get_id()).first()
                            if items:
                                t.save()
                            else:
                                t.save(force_insert=True)

            except IntegrityError as e:
                import traceback
                traceback.print_exc()
                raise CommandError("Database integrity error: {}".format(e))
            except DatabaseError as e:
                raise CommandError("General database error: {}\n"
                                   "Make sure you run syncdb or migrate before"
                                   "importing data!".format(e))
