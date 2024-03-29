from datetime import date, datetime, time

from django.db import models
from django.utils import timezone
from django.template import Context, Template
from django.test import TestCase

from .models import Campaign, CampaignLocationShift
from locations.models import District, Location


class CampaignLocationShiftRegroupTest(TestCase):

    def test_regroup(self):
        create_shifts()
        shifts = list(CampaignLocationShift.objects.with_free_places())
        template = Template(TEMPLATE)
        context = Context({'locations_and_shifts': shifts})
        rendered = template.render(context)
        self.maxDiff = None
        self.assertHTMLEqual(rendered, EXPECTED_RESULT)


TEMPLATE = '''
    {% regroup locations_and_shifts by location.district as district_list %}
    var shopsAndShifts = {
    {% for district in district_list %}
    {{ district.grouper.id }}: [
        {% regroup district.list by location as location_shifts %}
        {% for location in location_shifts %}
          {
            shop: '{{ location.grouper.name }}',
            shifts: [
            {% for shift in location.list %}
              {
                pk: '{{ shift.pk }}',
                when: '{{ shift.day }} {{ shift.start }} - {{ shift.end }}',
                freePlaces: {{ shift.free_places|default_if_none:shift.total_places }}
              }{% if not forloop.last %},{% endif %}
            {% endfor %}
            ]
          }{% if not forloop.last %},{% endif %}
        {% endfor %}
      ]{% if not forloop.last %},{% endif %}
    {% endfor %}
    };
'''


def create_shifts() -> None:
    Campaign.objects.create(
            id=5,
            name="Spring 2023 Campaign",
            start=timezone.datetime(2023, 4, 1).date(),
            end=timezone.datetime(2023, 4, 30).date(),
            is_active=True,
            summary="summary",
            registration_form_header="header",
            registration_form_footer="footer",
            registration_form_right_panel="right panel",
            registration_confirmation_template="confirmation template"
    )
    District.objects.create(id=3, name='Harjumaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=16, name='Hiiumaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=5, name='Ida-Virumaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=8, name='Järvamaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=7, name='Jõgevamaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=6, name='Lääne-Virumaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=9, name='Läänemaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=12, name='Pärnumaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=11, name='Põlvamaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=10, name='Raplamaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=4, name='Saaremaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=13, name='Tartumaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=15, name='Valgamaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=14, name='Viljandimaa', send_thank_you_email=False, thank_you_email_template='')
    District.objects.create(id=2, name='Võrumaa', send_thank_you_email=False, thank_you_email_template='')
    Location.objects.create(id=29, name='Annelinna Prisma (Tartu)', district_id=13, address='Nõlvaku 2, Tartu', contact_person='')
    Location.objects.create(id=118, name='Astri Selver (Narva)', district_id=5, address='Tallinna mnt 41, Narva', contact_person='')
    Location.objects.create(id=101, name='Centrumi Selver (Viljandi)', district_id=14, address='Tallinna 22', contact_person='')
    Location.objects.create(id=146, name='Eedeni Maksimarket', district_id=13, address='Kalda tee 1c, 50703 Tartu', contact_person='')
    Location.objects.create(id=149, name='Haabersti Rimi', district_id=3, address='Haabersti 1, Tallinn', contact_person='')
    Location.objects.create(id=86, name='Haapsalu Rimi Super (Haapsalu)', district_id=9, address='Jaama 32, Haapsalu, 90507 Lääne maakond', contact_person='')
    Location.objects.create(id=91, name='Hiiumaa Rimi (Kärdla)', district_id=16, address='Kõrgessaare maantee 25, Kärdla, 92412 Hiiu maakond', contact_person='')
    Location.objects.create(id=89, name='Hiiumaa Selver (Kärdla)', district_id=16, address='Rehemäe, Linnumäe küla, Hiiuamaa vald, Hiiumaa', contact_person='')
    Location.objects.create(id=81, name='Järve Selver (Tallinn)', district_id=3, address='Pärnu mnt 238, 11624 Tallinn', contact_person='')
    Location.objects.create(id=120, name='Jõgeva Grossi pood (Jõgeva)', district_id=7, address='Pargi 1, Jõgeva', contact_person='')
    Location.objects.create(id=43, name='Jõgeva Pae Konsum (Jõgeva)', district_id=7, address='Aia 33, Jõgeva linn', contact_person='')
    Location.objects.create(id=42, name='Jõgeva Selver (Jõgeva)', district_id=7, address='Kesk 3a/4, Jõgeva', contact_person='')
    Location.objects.create(id=39, name='Jõhvi Selver (Jõhvi)', district_id=5, address='Narva mnt. 8, Jõhvi', contact_person='')
    Location.objects.create(id=88, name='Kagukeskuse Selver (Võru)', district_id=2, address='Kooli 6, Võru, 65606 Võru maakond', contact_person='')
    Location.objects.create(id=125, name='Kohila Konsum (Kohila)', district_id=10, address='Lõuna 2, Kohila', contact_person='')
    Location.objects.create(id=5, name='Kristiine Prisma (Tallinn)', district_id=3, address='Endla 45, Tallinn', contact_person='')
    Location.objects.create(id=20, name='Krooni Selver (Rakvere)', district_id=6, address='Kroonikeskus, F.G.Adoffi 11, Rakvere', contact_person='')
    Location.objects.create(id=77, name='Kuressaare Rimi Auriga keskuses (Kuressaare)', district_id=4, address='Tallinna 88, Kuressaare', contact_person='')
    Location.objects.create(id=141, name='Kvartali Maksimarket (Tartu)', district_id=13, address='Riia mnt 2a, Tartu', contact_person='')
    Location.objects.create(id=138, name='Käina Konsum (Käina)', district_id=16, address='Spordi 9, Käina', contact_person='')
    Location.objects.create(id=109, name='Laagri Maksimarket (Laagri)', district_id=3, address='Pärnu mnt., 558a, Saue vald, 76401, Harju', contact_person='')
    Location.objects.create(id=65, name='Lasnamäe Centrumi Rimi Hyper (Tallinn)', district_id=3, address='Mustakivi 13, Tallinn', contact_person='')
    Location.objects.create(id=6, name='Lasnamäe Prisma (Tallinn)', district_id=3, address='Mustakivi Tee 17, Tallinn', contact_person='')
    Location.objects.create(id=100, name='Liiva Konsum (Muhu)', district_id=4, address='Liiva, Muhu vald, 94701, Saare maakond, Eesti.', contact_person='')
    Location.objects.create(id=27, name='Lõunakeskuse Rimi (Tartu)', district_id=13, address='Ringtee 75, Tartu', contact_person='')
    Location.objects.create(id=23, name='Mai Selver (Pärnu)', district_id=12, address='Papiniidu 42, Pärnu', contact_person='')
    Location.objects.create(id=128, name='Maxima Kuressaare (Kuressaare)', district_id=4, address='Tallinna 64, Kuressaare', contact_person='')
    Location.objects.create(id=135, name='Maxima Otepää (Valga)', district_id=15, address='Valga mnt 1b, Otepää', contact_person='')
    Location.objects.create(id=132, name='Maxima Rapla X (Rapla)', district_id=10, address='Tallinna mnt 50a, Rapla', contact_person='')
    Location.objects.create(id=139, name='Maxima X (Viljandi, Tallinna tn)', district_id=14, address='Tallinna 60, Viljandi', contact_person='')
    Location.objects.create(id=147, name='Maxima X Tõrva', district_id=15, address='Tõrva, 68605 Valga maakond', contact_person='')
    Location.objects.create(id=72, name='Maxima XX (Jõhvi)', district_id=5, address='Rakvere 29, Jõhvi, 41533 Ida-Viru maakond', contact_person='')
    Location.objects.create(id=115, name='Maxima XX Raadi (Tartu)', district_id=13, address='Narva mnt 112, Tartu', contact_person='')
    Location.objects.create(id=107, name='Maxima XX Smuuli (Tallinn)', district_id=3, address='J. Smuuli tee 9, 13629 Tallinn', contact_person='')
    Location.objects.create(id=129, name='Maxima XX Stroomi (Tallinn)', district_id=3, address='Tuulemaa 20, Tallinn', contact_person='')
    Location.objects.create(id=148, name='Maxima XX Valga', district_id=15, address='Jaama pst 2b, Valga', contact_person='')
    Location.objects.create(id=121, name='Maxima XXX Pärnu (Pärnu)', district_id=12, address='Riia mnt 131, Pärnu', contact_person='')
    Location.objects.create(id=7, name='Mustamäe Prisma (Tallinn)', district_id=3, address='Karjavälja 4, Tallinn', contact_person='')
    Location.objects.create(id=33, name='Mustvee Konsum (Jõgeva)', district_id=7, address='Tartu mnt. 3, Mustvee linn', contact_person='')
    Location.objects.create(id=140, name='Männimäe Maksimarket', district_id=14, address='Puidu 2, Viljandi', contact_person='')
    Location.objects.create(id=119, name='Narva Fama Rimi (Narva)', district_id=5, address='Fama põik 10, Narva', contact_person='')
    Location.objects.create(id=34, name='Narva Prisma (Narva)', district_id=5, address='Kangelaste Prospekt 29, Narva', contact_person='')
    Location.objects.create(id=127, name='Orissaare Konsum', district_id=4, address='Kuivastu mnt 28, Orissaare', contact_person='')
    Location.objects.create(id=136, name='Paalalinna Maksimarket (Viljandi)', district_id=14, address='Lääne 2, Viljandi', contact_person='')
    Location.objects.create(id=16, name='Paide Maksimarket (Paide)', district_id=8, address='Ringtee 2, 72751, Paide', contact_person='')
    Location.objects.create(id=143, name='Peetri Selver (Peetri)', district_id=3, address='Veesaare tee 2, Peetri', contact_person='')
    Location.objects.create(id=75, name='Pirita Selver', district_id=3, address='Rummu tee 4, 11911 Tallinn', contact_person='')
    Location.objects.create(id=26, name='Pärnu Maksimarket ( Pärnu)', district_id=12, address='Haapsalu mnt 43, Papsaare, 88317, Audru vald, Pärnu maakond', contact_person='')
    Location.objects.create(id=22, name='Pärnu Rimi Hyper (Pärnu)', district_id=12, address='Papiniidu 8, Pärnu', contact_person='')
    Location.objects.create(id=32, name='Põltsamaa Selver (Jõgeva)', district_id=7, address='Jõgeva maantee 1a, Põltsamaa, 48105 Jõgev', contact_person='')
    Location.objects.create(id=71, name='Põlva Coop Maksimarket (Põlva)', district_id=11, address='Ringtee, 4, Põlva, 63308, Põlva maakond, Eesti', contact_person='')
    Location.objects.create(id=18, name='Põlva Selver (Põlva)', district_id=11, address='Jaama 12, Põlva', contact_person='')
    Location.objects.create(id=21, name='Rakvere Maksimarket (Rakvere)', district_id=6, address='Vaala Keskus, Lõõtspilli 2, Rakvere', contact_person='')
    Location.objects.create(id=19, name='Rakvere Rimi Hyper (Rakvere)', district_id=6, address='Põhjakeskus, Tõrremäe küla, Rakvere vald, Lääne-Virumaa', contact_person='')
    Location.objects.create(id=40, name='Rannarootsi Selver (Haapsalu)', district_id=9, address='Rannarootsi tee 1, Uuemõisa', contact_person='')
    Location.objects.create(id=133, name='Rapla Konsum (Rapla)', district_id=10, address='Tallinna mnt 16, Rapla', contact_person='')
    Location.objects.create(id=124, name='Rapla Selver (Rapla)', district_id=10, address='Tallinna mnt 4, Rapla', contact_person='')
    Location.objects.create(id=28, name='Rebase Rimi (Tartu)', district_id=13, address='Rebase 10, Tartu', contact_person='')
    Location.objects.create(id=116, name='Ringtee Selver (Tartu)', district_id=13, address='Aardla 114, Tartu', contact_person='')
    Location.objects.create(id=4, name='Rocca Al Mare Prisma (Tallinn)', district_id=3, address='Paldiski mnt. 102, Tallinn', contact_person='')
    Location.objects.create(id=35, name='Saare Selver (Kuressaare)', district_id=4, address='Tallinna tn 67, Kuressaare', contact_person='')
    Location.objects.create(id=134, name='Saaremaa Kaubamaja Toidumaailm (Kuressaare)', district_id=4, address='Raekoja 1, Kuressaare', contact_person='')
    Location.objects.create(id=59, name='Sikupilli Prisma (Tallinn)', district_id=3, address='Tartu maantee 87, Tallinn', contact_person='')
    Location.objects.create(id=102, name='Suurejõe Selver (Pärnu)', district_id=12, address='Suur-Jõe 57, Pärnu, 80042 Pärnu maakond', contact_person='')
    Location.objects.create(id=30, name='Sõbra Prisma (Tartu)', district_id=13, address='Sõbra 58, Tartu', contact_person='')
    Location.objects.create(id=9, name='Sõpruse Rimi Hyper (Tallinn)', district_id=3, address='Sõpruse pst 174/ 176, Tallinn', contact_person='')
    Location.objects.create(id=142, name='Tabasalu Rimi (Tabasalu)', district_id=3, address='Klooga mnt 10b, Tabasalu', contact_person='')
    Location.objects.create(id=84, name='Tapa Rimi Mini', district_id=6, address='Pikk 5, Tapa, 45106 Lääne-Viru maakond', contact_person='')
    Location.objects.create(id=144, name='Tikste Konsum (Tõrva, Valga)', district_id=15, address='Viljandi 28, Tõrva', contact_person='')
    Location.objects.create(id=90, name='Tormi Konsum (Kärdla)', district_id=16, address='Heltermaa maantee 14a, Kärdla, 92414 Hiiu maakond', contact_person='')
    Location.objects.create(id=61, name='Torupilli Selver (Tallinn)', district_id=3, address='Vesivärava 37, Tallinn', contact_person='')
    Location.objects.create(id=73, name='Türi Konsum (Türi)', district_id=8, address='Tallinna, 4, Türi, 72210, Järva maakond, Eesti', contact_person='')
    Location.objects.create(id=70, name='Valga Rimi Supermarket (Valga)', district_id=15, address='Riia 18, Valga', contact_person='')
    Location.objects.create(id=93, name='Valga Selver (Valga)', district_id=15, address='Raja tn 5, Valga', contact_person='')
    Location.objects.create(id=12, name='Viimsi Selver (Viimsi)', district_id=3, address='Sõpruse tee 15, 74001, Haabneeme, Viimsi vald', contact_person='')
    Location.objects.create(id=69, name='Viljandi Rimi Hyper (Viljandi)', district_id=14, address='Tallinna 41, Viljandi, 71020 Viljandi maakond,', contact_person='')
    Location.objects.create(id=37, name='Võru Maxima (Võru)', district_id=2, address='Kooli 2, Võru', contact_person='')
    Location.objects.create(id=38, name='Võru Rimi supermarket (Võru)', district_id=2, address='Jüri 85, Võru', contact_person='')
    Location.objects.create(id=24, name='Ülejõe Selver (Pärnu)', district_id=12, address='Tallinna mnt 93a/ Roheline 80, Pärnu', contact_person='')
    Location.objects.create(id=67, name='Ülemiste Rimi Hyper (Tallinn)', district_id=3, address='Suur-Sõjamäe tänav 4, Tallinn', contact_person='')
    CampaignLocationShift.objects.create(id=1178, campaign_id=5, location_id=149, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1179, campaign_id=5, location_id=149, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1180, campaign_id=5, location_id=149, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1181, campaign_id=5, location_id=149, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1150, campaign_id=5, location_id=81, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1151, campaign_id=5, location_id=81, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1152, campaign_id=5, location_id=81, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1153, campaign_id=5, location_id=81, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1138, campaign_id=5, location_id=5, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1139, campaign_id=5, location_id=5, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1140, campaign_id=5, location_id=5, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1141, campaign_id=5, location_id=5, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=914, campaign_id=5, location_id=109, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=915, campaign_id=5, location_id=109, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=916, campaign_id=5, location_id=109, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=917, campaign_id=5, location_id=109, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=886, campaign_id=5, location_id=65, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=887, campaign_id=5, location_id=65, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=888, campaign_id=5, location_id=65, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=889, campaign_id=5, location_id=65, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=874, campaign_id=5, location_id=6, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=875, campaign_id=5, location_id=6, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=876, campaign_id=5, location_id=6, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=877, campaign_id=5, location_id=6, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=910, campaign_id=5, location_id=107, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=911, campaign_id=5, location_id=107, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=912, campaign_id=5, location_id=107, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=913, campaign_id=5, location_id=107, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=898, campaign_id=5, location_id=129, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=899, campaign_id=5, location_id=129, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=900, campaign_id=5, location_id=129, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=901, campaign_id=5, location_id=129, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=870, campaign_id=5, location_id=7, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=871, campaign_id=5, location_id=7, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=872, campaign_id=5, location_id=7, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=873, campaign_id=5, location_id=7, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1158, campaign_id=5, location_id=143, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1159, campaign_id=5, location_id=143, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1160, campaign_id=5, location_id=143, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1161, campaign_id=5, location_id=143, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=890, campaign_id=5, location_id=75, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=891, campaign_id=5, location_id=75, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=892, campaign_id=5, location_id=75, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=893, campaign_id=5, location_id=75, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=866, campaign_id=5, location_id=4, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=867, campaign_id=5, location_id=4, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=868, campaign_id=5, location_id=4, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=869, campaign_id=5, location_id=4, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1142, campaign_id=5, location_id=59, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1143, campaign_id=5, location_id=59, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1144, campaign_id=5, location_id=59, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1145, campaign_id=5, location_id=59, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=878, campaign_id=5, location_id=9, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=879, campaign_id=5, location_id=9, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=880, campaign_id=5, location_id=9, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=881, campaign_id=5, location_id=9, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1146, campaign_id=5, location_id=142, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1147, campaign_id=5, location_id=142, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1148, campaign_id=5, location_id=142, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1149, campaign_id=5, location_id=142, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1154, campaign_id=5, location_id=61, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1155, campaign_id=5, location_id=61, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1156, campaign_id=5, location_id=61, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1157, campaign_id=5, location_id=61, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=918, campaign_id=5, location_id=12, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=919, campaign_id=5, location_id=12, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=920, campaign_id=5, location_id=12, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=921, campaign_id=5, location_id=12, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=882, campaign_id=5, location_id=67, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=883, campaign_id=5, location_id=67, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=884, campaign_id=5, location_id=67, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=885, campaign_id=5, location_id=67, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1112, campaign_id=5, location_id=91, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(18, 15, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1113, campaign_id=5, location_id=91, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(18, 30, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1114, campaign_id=5, location_id=89, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(18, 15, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1115, campaign_id=5, location_id=89, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(18, 30, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1107, campaign_id=5, location_id=138, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(18, 15, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1111, campaign_id=5, location_id=138, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(18, 30, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1109, campaign_id=5, location_id=90, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(18, 15, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1110, campaign_id=5, location_id=90, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(18, 30, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=955, campaign_id=5, location_id=118, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=956, campaign_id=5, location_id=118, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=957, campaign_id=5, location_id=118, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=958, campaign_id=5, location_id=118, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1006, campaign_id=5, location_id=39, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1007, campaign_id=5, location_id=39, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1008, campaign_id=5, location_id=39, day=date(2024, 4, 13), start=time(10, 0, 0, 0), end=time(13, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1009, campaign_id=5, location_id=39, day=date(2024, 4, 13), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1108, campaign_id=5, location_id=72, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=8, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1116, campaign_id=5, location_id=72, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=8, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1117, campaign_id=5, location_id=72, day=date(2024, 4, 13), start=time(10, 0, 0, 0), end=time(13, 0, 0, 0), total_places=8, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1118, campaign_id=5, location_id=72, day=date(2024, 4, 13), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=8, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=959, campaign_id=5, location_id=119, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=960, campaign_id=5, location_id=119, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=961, campaign_id=5, location_id=119, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=962, campaign_id=5, location_id=119, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=951, campaign_id=5, location_id=34, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=952, campaign_id=5, location_id=34, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=953, campaign_id=5, location_id=34, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=954, campaign_id=5, location_id=34, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=988, campaign_id=5, location_id=16, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=990, campaign_id=5, location_id=16, day=date(2024, 4, 13), start=time(10, 0, 0, 0), end=time(14, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=992, campaign_id=5, location_id=73, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=994, campaign_id=5, location_id=73, day=date(2024, 4, 13), start=time(10, 0, 0, 0), end=time(14, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1004, campaign_id=5, location_id=120, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1005, campaign_id=5, location_id=120, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(16, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1000, campaign_id=5, location_id=43, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1001, campaign_id=5, location_id=43, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(16, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=996, campaign_id=5, location_id=42, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=997, campaign_id=5, location_id=42, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(16, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1002, campaign_id=5, location_id=33, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1003, campaign_id=5, location_id=33, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(16, 0, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=998, campaign_id=5, location_id=32, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=999, campaign_id=5, location_id=32, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(16, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1025, campaign_id=5, location_id=20, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1121, campaign_id=5, location_id=20, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(17, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1026, campaign_id=5, location_id=20, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1122, campaign_id=5, location_id=20, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(17, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1027, campaign_id=5, location_id=21, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(14, 30, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1028, campaign_id=5, location_id=21, day=date(2024, 4, 12), start=time(14, 30, 0, 0), end=time(17, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1029, campaign_id=5, location_id=21, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(14, 30, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1030, campaign_id=5, location_id=21, day=date(2024, 4, 13), start=time(14, 30, 0, 0), end=time(17, 0, 0, 0), total_places=2, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1023, campaign_id=5, location_id=19, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1119, campaign_id=5, location_id=19, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(17, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1024, campaign_id=5, location_id=19, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1120, campaign_id=5, location_id=19, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(17, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1033, campaign_id=5, location_id=84, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1123, campaign_id=5, location_id=84, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(17, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1034, campaign_id=5, location_id=84, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1124, campaign_id=5, location_id=84, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(17, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1162, campaign_id=5, location_id=86, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1163, campaign_id=5, location_id=86, day=date(2024, 4, 12), start=time(15, 30, 0, 0), end=time(18, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1164, campaign_id=5, location_id=86, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1165, campaign_id=5, location_id=86, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(18, 0, 0, 0), total_places=3, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1014, campaign_id=5, location_id=40, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1015, campaign_id=5, location_id=40, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1016, campaign_id=5, location_id=40, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1017, campaign_id=5, location_id=40, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=6, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=971, campaign_id=5, location_id=23, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=972, campaign_id=5, location_id=23, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=973, campaign_id=5, location_id=23, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=975, campaign_id=5, location_id=23, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=967, campaign_id=5, location_id=121, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=968, campaign_id=5, location_id=121, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=969, campaign_id=5, location_id=121, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=970, campaign_id=5, location_id=121, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=984, campaign_id=5, location_id=26, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=985, campaign_id=5, location_id=26, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=986, campaign_id=5, location_id=26, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=987, campaign_id=5, location_id=26, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=963, campaign_id=5, location_id=22, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=964, campaign_id=5, location_id=22, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=965, campaign_id=5, location_id=22, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=966, campaign_id=5, location_id=22, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=976, campaign_id=5, location_id=102, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=977, campaign_id=5, location_id=102, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=978, campaign_id=5, location_id=102, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=979, campaign_id=5, location_id=102, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=980, campaign_id=5, location_id=24, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=981, campaign_id=5, location_id=24, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=982, campaign_id=5, location_id=24, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=983, campaign_id=5, location_id=24, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1018, campaign_id=5, location_id=71, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1019, campaign_id=5, location_id=71, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1020, campaign_id=5, location_id=71, day=date(2024, 4, 13), start=time(10, 0, 0, 0), end=time(14, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1104, campaign_id=5, location_id=18, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1105, campaign_id=5, location_id=18, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1106, campaign_id=5, location_id=18, day=date(2024, 4, 13), start=time(10, 0, 0, 0), end=time(14, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1047, campaign_id=5, location_id=125, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1048, campaign_id=5, location_id=125, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1049, campaign_id=5, location_id=125, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1050, campaign_id=5, location_id=125, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1039, campaign_id=5, location_id=132, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1040, campaign_id=5, location_id=132, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1041, campaign_id=5, location_id=132, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1042, campaign_id=5, location_id=132, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1043, campaign_id=5, location_id=133, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1044, campaign_id=5, location_id=133, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1045, campaign_id=5, location_id=133, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1046, campaign_id=5, location_id=133, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1100, campaign_id=5, location_id=124, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1101, campaign_id=5, location_id=124, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1102, campaign_id=5, location_id=124, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1103, campaign_id=5, location_id=124, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1059, campaign_id=5, location_id=77, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1060, campaign_id=5, location_id=77, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1055, campaign_id=5, location_id=100, day=date(2024, 4, 13), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1057, campaign_id=5, location_id=128, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1058, campaign_id=5, location_id=128, day=date(2024, 4, 13), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1053, campaign_id=5, location_id=127, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1061, campaign_id=5, location_id=35, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1062, campaign_id=5, location_id=35, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1051, campaign_id=5, location_id=134, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1052, campaign_id=5, location_id=134, day=date(2024, 4, 12), start=time(15, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=930, campaign_id=5, location_id=29, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=931, campaign_id=5, location_id=29, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=932, campaign_id=5, location_id=29, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=933, campaign_id=5, location_id=29, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1170, campaign_id=5, location_id=146, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1171, campaign_id=5, location_id=146, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1172, campaign_id=5, location_id=146, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1173, campaign_id=5, location_id=146, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1130, campaign_id=5, location_id=141, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1131, campaign_id=5, location_id=141, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1132, campaign_id=5, location_id=141, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1133, campaign_id=5, location_id=141, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=943, campaign_id=5, location_id=27, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=944, campaign_id=5, location_id=27, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=945, campaign_id=5, location_id=27, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=946, campaign_id=5, location_id=27, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=922, campaign_id=5, location_id=115, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=923, campaign_id=5, location_id=115, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=924, campaign_id=5, location_id=115, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=925, campaign_id=5, location_id=115, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=938, campaign_id=5, location_id=28, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=940, campaign_id=5, location_id=28, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=941, campaign_id=5, location_id=28, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=942, campaign_id=5, location_id=28, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=947, campaign_id=5, location_id=116, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=948, campaign_id=5, location_id=116, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=949, campaign_id=5, location_id=116, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=950, campaign_id=5, location_id=116, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=934, campaign_id=5, location_id=30, day=date(2024, 4, 12), start=time(13, 0, 0, 0), end=time(16, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=935, campaign_id=5, location_id=30, day=date(2024, 4, 12), start=time(16, 0, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=936, campaign_id=5, location_id=30, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 30, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=937, campaign_id=5, location_id=30, day=date(2024, 4, 13), start=time(15, 30, 0, 0), end=time(19, 0, 0, 0), total_places=10, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1074, campaign_id=5, location_id=135, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1077, campaign_id=5, location_id=135, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1174, campaign_id=5, location_id=147, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1175, campaign_id=5, location_id=147, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1176, campaign_id=5, location_id=148, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1177, campaign_id=5, location_id=148, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1166, campaign_id=5, location_id=144, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1169, campaign_id=5, location_id=144, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=4, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1066, campaign_id=5, location_id=70, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1069, campaign_id=5, location_id=70, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1070, campaign_id=5, location_id=93, day=date(2024, 4, 12), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1073, campaign_id=5, location_id=93, day=date(2024, 4, 13), start=time(12, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1079, campaign_id=5, location_id=101, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1127, campaign_id=5, location_id=139, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1128, campaign_id=5, location_id=140, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1129, campaign_id=5, location_id=140, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1084, campaign_id=5, location_id=136, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1085, campaign_id=5, location_id=136, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1125, campaign_id=5, location_id=69, day=date(2024, 4, 12), start=time(14, 0, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1126, campaign_id=5, location_id=69, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(15, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1134, campaign_id=5, location_id=88, day=date(2024, 4, 12), start=time(11, 30, 0, 0), end=time(14, 30, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1135, campaign_id=5, location_id=88, day=date(2024, 4, 12), start=time(14, 30, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1136, campaign_id=5, location_id=88, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(14, 30, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1137, campaign_id=5, location_id=88, day=date(2024, 4, 13), start=time(14, 30, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1092, campaign_id=5, location_id=37, day=date(2024, 4, 12), start=time(11, 30, 0, 0), end=time(14, 30, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1093, campaign_id=5, location_id=37, day=date(2024, 4, 12), start=time(14, 30, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1094, campaign_id=5, location_id=37, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(14, 30, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1095, campaign_id=5, location_id=37, day=date(2024, 4, 13), start=time(14, 30, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1088, campaign_id=5, location_id=38, day=date(2024, 4, 12), start=time(11, 30, 0, 0), end=time(14, 30, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1089, campaign_id=5, location_id=38, day=date(2024, 4, 12), start=time(14, 30, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1090, campaign_id=5, location_id=38, day=date(2024, 4, 13), start=time(11, 0, 0, 0), end=time(14, 30, 0, 0), total_places=5, shift_leader_id=None)
    CampaignLocationShift.objects.create(id=1091, campaign_id=5, location_id=38, day=date(2024, 4, 13), start=time(14, 30, 0, 0), end=time(18, 0, 0, 0), total_places=5, shift_leader_id=None)


EXPECTED_RESULT = '''
    var shopsAndShifts = {
    
    3: [
        
        
          {
            shop: 'Haabersti Rimi',
            shifts: [
            
              {
                pk: '1178',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1179',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1180',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1181',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Järve Selver (Tallinn)',
            shifts: [
            
              {
                pk: '1150',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1151',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1152',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1153',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Kristiine Prisma (Tallinn)',
            shifts: [
            
              {
                pk: '1138',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1139',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1140',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1141',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Laagri Maksimarket (Laagri)',
            shifts: [
            
              {
                pk: '914',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '915',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '916',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '917',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Lasnamäe Centrumi Rimi Hyper (Tallinn)',
            shifts: [
            
              {
                pk: '886',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '887',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '888',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '889',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Lasnamäe Prisma (Tallinn)',
            shifts: [
            
              {
                pk: '874',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '875',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '876',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '877',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Maxima XX Smuuli (Tallinn)',
            shifts: [
            
              {
                pk: '910',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '911',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '912',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '913',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Maxima XX Stroomi (Tallinn)',
            shifts: [
            
              {
                pk: '898',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '899',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '900',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '901',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Mustamäe Prisma (Tallinn)',
            shifts: [
            
              {
                pk: '870',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '871',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '872',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '873',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Peetri Selver (Peetri)',
            shifts: [
            
              {
                pk: '1158',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1159',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1160',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1161',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Pirita Selver',
            shifts: [
            
              {
                pk: '890',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '891',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '892',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '893',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Rocca Al Mare Prisma (Tallinn)',
            shifts: [
            
              {
                pk: '866',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '867',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '868',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '869',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Sikupilli Prisma (Tallinn)',
            shifts: [
            
              {
                pk: '1142',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1143',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1144',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1145',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Sõpruse Rimi Hyper (Tallinn)',
            shifts: [
            
              {
                pk: '878',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '879',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '880',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '881',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Tabasalu Rimi (Tabasalu)',
            shifts: [
            
              {
                pk: '1146',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1147',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1148',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1149',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Torupilli Selver (Tallinn)',
            shifts: [
            
              {
                pk: '1154',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1155',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1156',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1157',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Viimsi Selver (Viimsi)',
            shifts: [
            
              {
                pk: '918',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '919',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '920',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '921',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Ülemiste Rimi Hyper (Tallinn)',
            shifts: [
            
              {
                pk: '882',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '883',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '884',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '885',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          }
        
      ],
    
    16: [
        
        
          {
            shop: 'Hiiumaa Rimi (Kärdla)',
            shifts: [
            
              {
                pk: '1112',
                when: '12. aprill 2024 13:00 - 18:15',
                freePlaces: 2
              },
            
              {
                pk: '1113',
                when: '13. aprill 2024 11:00 - 18:30',
                freePlaces: 2
              }
            
            ]
          },
        
          {
            shop: 'Hiiumaa Selver (Kärdla)',
            shifts: [
            
              {
                pk: '1114',
                when: '12. aprill 2024 13:00 - 18:15',
                freePlaces: 2
              },
            
              {
                pk: '1115',
                when: '13. aprill 2024 11:00 - 18:30',
                freePlaces: 2
              }
            
            ]
          },
        
          {
            shop: 'Käina Konsum (Käina)',
            shifts: [
            
              {
                pk: '1107',
                when: '12. aprill 2024 13:00 - 18:15',
                freePlaces: 2
              },
            
              {
                pk: '1111',
                when: '13. aprill 2024 11:00 - 18:30',
                freePlaces: 2
              }
            
            ]
          },
        
          {
            shop: 'Tormi Konsum (Kärdla)',
            shifts: [
            
              {
                pk: '1109',
                when: '12. aprill 2024 13:00 - 18:15',
                freePlaces: 2
              },
            
              {
                pk: '1110',
                when: '13. aprill 2024 11:00 - 18:30',
                freePlaces: 2
              }
            
            ]
          }
        
      ],
    
    5: [
        
        
          {
            shop: 'Astri Selver (Narva)',
            shifts: [
            
              {
                pk: '955',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 6
              },
            
              {
                pk: '956',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 6
              },
            
              {
                pk: '957',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 6
              },
            
              {
                pk: '958',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 6
              }
            
            ]
          },
        
          {
            shop: 'Jõhvi Selver (Jõhvi)',
            shifts: [
            
              {
                pk: '1006',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1007',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1008',
                when: '13. aprill 2024 10:00 - 13:00',
                freePlaces: 5
              },
            
              {
                pk: '1009',
                when: '13. aprill 2024 13:00 - 16:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Maxima XX (Jõhvi)',
            shifts: [
            
              {
                pk: '1108',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 8
              },
            
              {
                pk: '1116',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 8
              },
            
              {
                pk: '1117',
                when: '13. aprill 2024 10:00 - 13:00',
                freePlaces: 8
              },
            
              {
                pk: '1118',
                when: '13. aprill 2024 13:00 - 16:00',
                freePlaces: 8
              }
            
            ]
          },
        
          {
            shop: 'Narva Fama Rimi (Narva)',
            shifts: [
            
              {
                pk: '959',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 6
              },
            
              {
                pk: '960',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 6
              },
            
              {
                pk: '961',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 6
              },
            
              {
                pk: '962',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 6
              }
            
            ]
          },
        
          {
            shop: 'Narva Prisma (Narva)',
            shifts: [
            
              {
                pk: '951',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 6
              },
            
              {
                pk: '952',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 6
              },
            
              {
                pk: '953',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 6
              },
            
              {
                pk: '954',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 6
              }
            
            ]
          }
        
      ],
    
    8: [
        
        
          {
            shop: 'Paide Maksimarket (Paide)',
            shifts: [
            
              {
                pk: '988',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 4
              },
            
              {
                pk: '990',
                when: '13. aprill 2024 10:00 - 14:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Türi Konsum (Türi)',
            shifts: [
            
              {
                pk: '992',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 4
              },
            
              {
                pk: '994',
                when: '13. aprill 2024 10:00 - 14:00',
                freePlaces: 4
              }
            
            ]
          }
        
      ],
    
    7: [
        
        
          {
            shop: 'Jõgeva Grossi pood (Jõgeva)',
            shifts: [
            
              {
                pk: '1004',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1005',
                when: '13. aprill 2024 12:00 - 16:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Jõgeva Pae Konsum (Jõgeva)',
            shifts: [
            
              {
                pk: '1000',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 4
              },
            
              {
                pk: '1001',
                when: '13. aprill 2024 12:00 - 16:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Jõgeva Selver (Jõgeva)',
            shifts: [
            
              {
                pk: '996',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '997',
                when: '13. aprill 2024 12:00 - 16:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Mustvee Konsum (Jõgeva)',
            shifts: [
            
              {
                pk: '1002',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 2
              },
            
              {
                pk: '1003',
                when: '13. aprill 2024 12:00 - 16:00',
                freePlaces: 2
              }
            
            ]
          },
        
          {
            shop: 'Põltsamaa Selver (Jõgeva)',
            shifts: [
            
              {
                pk: '998',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '999',
                when: '13. aprill 2024 12:00 - 16:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ],
    
    6: [
        
        
          {
            shop: 'Krooni Selver (Rakvere)',
            shifts: [
            
              {
                pk: '1025',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 3
              },
            
              {
                pk: '1121',
                when: '12. aprill 2024 15:00 - 17:00',
                freePlaces: 3
              },
            
              {
                pk: '1026',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 3
              },
            
              {
                pk: '1122',
                when: '13. aprill 2024 15:00 - 17:00',
                freePlaces: 3
              }
            
            ]
          },
        
          {
            shop: 'Rakvere Maksimarket (Rakvere)',
            shifts: [
            
              {
                pk: '1027',
                when: '12. aprill 2024 12:00 - 14:30',
                freePlaces: 3
              },
            
              {
                pk: '1028',
                when: '12. aprill 2024 14:30 - 17:00',
                freePlaces: 3
              },
            
              {
                pk: '1029',
                when: '13. aprill 2024 12:00 - 14:30',
                freePlaces: 3
              },
            
              {
                pk: '1030',
                when: '13. aprill 2024 14:30 - 17:00',
                freePlaces: 2
              }
            
            ]
          },
        
          {
            shop: 'Rakvere Rimi Hyper (Rakvere)',
            shifts: [
            
              {
                pk: '1023',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 6
              },
            
              {
                pk: '1119',
                when: '12. aprill 2024 15:00 - 17:00',
                freePlaces: 3
              },
            
              {
                pk: '1024',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 6
              },
            
              {
                pk: '1120',
                when: '13. aprill 2024 15:00 - 17:00',
                freePlaces: 6
              }
            
            ]
          },
        
          {
            shop: 'Tapa Rimi Mini',
            shifts: [
            
              {
                pk: '1033',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1123',
                when: '12. aprill 2024 15:00 - 17:00',
                freePlaces: 5
              },
            
              {
                pk: '1034',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1124',
                when: '13. aprill 2024 15:00 - 17:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ],
    
    9: [
        
        
          {
            shop: 'Haapsalu Rimi Super (Haapsalu)',
            shifts: [
            
              {
                pk: '1162',
                when: '12. aprill 2024 12:00 - 15:30',
                freePlaces: 3
              },
            
              {
                pk: '1163',
                when: '12. aprill 2024 15:30 - 18:00',
                freePlaces: 3
              },
            
              {
                pk: '1164',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 3
              },
            
              {
                pk: '1165',
                when: '13. aprill 2024 15:30 - 18:00',
                freePlaces: 3
              }
            
            ]
          },
        
          {
            shop: 'Rannarootsi Selver (Haapsalu)',
            shifts: [
            
              {
                pk: '1014',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 6
              },
            
              {
                pk: '1015',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 6
              },
            
              {
                pk: '1016',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 6
              },
            
              {
                pk: '1017',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 6
              }
            
            ]
          }
        
      ],
    
    12: [
        
        
          {
            shop: 'Mai Selver (Pärnu)',
            shifts: [
            
              {
                pk: '971',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '972',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '973',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '975',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Maxima XXX Pärnu (Pärnu)',
            shifts: [
            
              {
                pk: '967',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '968',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '969',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '970',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Pärnu Maksimarket ( Pärnu)',
            shifts: [
            
              {
                pk: '984',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '985',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '986',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '987',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Pärnu Rimi Hyper (Pärnu)',
            shifts: [
            
              {
                pk: '963',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '964',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '965',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '966',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Suurejõe Selver (Pärnu)',
            shifts: [
            
              {
                pk: '976',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '977',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '978',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '979',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Ülejõe Selver (Pärnu)',
            shifts: [
            
              {
                pk: '980',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '981',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '982',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '983',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          }
        
      ],
    
    11: [
        
        
          {
            shop: 'Põlva Coop Maksimarket (Põlva)',
            shifts: [
            
              {
                pk: '1018',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1019',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1020',
                when: '13. aprill 2024 10:00 - 14:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Põlva Selver (Põlva)',
            shifts: [
            
              {
                pk: '1104',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1105',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1106',
                when: '13. aprill 2024 10:00 - 14:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ],
    
    10: [
        
        
          {
            shop: 'Kohila Konsum (Kohila)',
            shifts: [
            
              {
                pk: '1047',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              },
            
              {
                pk: '1048',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 4
              },
            
              {
                pk: '1049',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              },
            
              {
                pk: '1050',
                when: '13. aprill 2024 15:00 - 18:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Maxima Rapla X (Rapla)',
            shifts: [
            
              {
                pk: '1039',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1040',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1041',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1042',
                when: '13. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Rapla Konsum (Rapla)',
            shifts: [
            
              {
                pk: '1043',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              },
            
              {
                pk: '1044',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 4
              },
            
              {
                pk: '1045',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              },
            
              {
                pk: '1046',
                when: '13. aprill 2024 15:00 - 18:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Rapla Selver (Rapla)',
            shifts: [
            
              {
                pk: '1100',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1101',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1102',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1103',
                when: '13. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ],
    
    4: [
        
        
          {
            shop: 'Kuressaare Rimi Auriga keskuses (Kuressaare)',
            shifts: [
            
              {
                pk: '1059',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1060',
                when: '13. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Liiva Konsum (Muhu)',
            shifts: [
            
              {
                pk: '1055',
                when: '13. aprill 2024 14:00 - 18:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Maxima Kuressaare (Kuressaare)',
            shifts: [
            
              {
                pk: '1057',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              },
            
              {
                pk: '1058',
                when: '13. aprill 2024 15:00 - 18:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Orissaare Konsum',
            shifts: [
            
              {
                pk: '1053',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Saare Selver (Kuressaare)',
            shifts: [
            
              {
                pk: '1061',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              },
            
              {
                pk: '1062',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Saaremaa Kaubamaja Toidumaailm (Kuressaare)',
            shifts: [
            
              {
                pk: '1051',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1052',
                when: '12. aprill 2024 15:00 - 18:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ],
    
    13: [
        
        
          {
            shop: 'Annelinna Prisma (Tartu)',
            shifts: [
            
              {
                pk: '930',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '931',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '932',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '933',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Eedeni Maksimarket',
            shifts: [
            
              {
                pk: '1170',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1171',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1172',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1173',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Kvartali Maksimarket (Tartu)',
            shifts: [
            
              {
                pk: '1130',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '1131',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '1132',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '1133',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Lõunakeskuse Rimi (Tartu)',
            shifts: [
            
              {
                pk: '943',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '944',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '945',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '946',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Maxima XX Raadi (Tartu)',
            shifts: [
            
              {
                pk: '922',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '923',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '924',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '925',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Rebase Rimi (Tartu)',
            shifts: [
            
              {
                pk: '938',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '940',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '941',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '942',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Ringtee Selver (Tartu)',
            shifts: [
            
              {
                pk: '947',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '948',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '949',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '950',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          },
        
          {
            shop: 'Sõbra Prisma (Tartu)',
            shifts: [
            
              {
                pk: '934',
                when: '12. aprill 2024 13:00 - 16:00',
                freePlaces: 10
              },
            
              {
                pk: '935',
                when: '12. aprill 2024 16:00 - 19:00',
                freePlaces: 10
              },
            
              {
                pk: '936',
                when: '13. aprill 2024 12:00 - 15:30',
                freePlaces: 10
              },
            
              {
                pk: '937',
                when: '13. aprill 2024 15:30 - 19:00',
                freePlaces: 10
              }
            
            ]
          }
        
      ],
    
    15: [
        
        
          {
            shop: 'Maxima Otepää (Valga)',
            shifts: [
            
              {
                pk: '1074',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1077',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Maxima X Tõrva',
            shifts: [
            
              {
                pk: '1174',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1175',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Maxima XX Valga',
            shifts: [
            
              {
                pk: '1176',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1177',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Tikste Konsum (Tõrva, Valga)',
            shifts: [
            
              {
                pk: '1166',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              },
            
              {
                pk: '1169',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 4
              }
            
            ]
          },
        
          {
            shop: 'Valga Rimi Supermarket (Valga)',
            shifts: [
            
              {
                pk: '1066',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1069',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Valga Selver (Valga)',
            shifts: [
            
              {
                pk: '1070',
                when: '12. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              },
            
              {
                pk: '1073',
                when: '13. aprill 2024 12:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ],
    
    14: [
        
        
          {
            shop: 'Centrumi Selver (Viljandi)',
            shifts: [
            
              {
                pk: '1079',
                when: '13. aprill 2024 11:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Maxima X (Viljandi, Tallinna tn)',
            shifts: [
            
              {
                pk: '1127',
                when: '13. aprill 2024 11:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Männimäe Maksimarket',
            shifts: [
            
              {
                pk: '1128',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1129',
                when: '13. aprill 2024 11:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Paalalinna Maksimarket (Viljandi)',
            shifts: [
            
              {
                pk: '1084',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1085',
                when: '13. aprill 2024 11:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Viljandi Rimi Hyper (Viljandi)',
            shifts: [
            
              {
                pk: '1125',
                when: '12. aprill 2024 14:00 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1126',
                when: '13. aprill 2024 11:00 - 15:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ],
    
    2: [
        
        
          {
            shop: 'Kagukeskuse Selver (Võru)',
            shifts: [
            
              {
                pk: '1134',
                when: '12. aprill 2024 11:30 - 14:30',
                freePlaces: 5
              },
            
              {
                pk: '1135',
                when: '12. aprill 2024 14:30 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1136',
                when: '13. aprill 2024 11:00 - 14:30',
                freePlaces: 5
              },
            
              {
                pk: '1137',
                when: '13. aprill 2024 14:30 - 18:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Võru Maxima (Võru)',
            shifts: [
            
              {
                pk: '1092',
                when: '12. aprill 2024 11:30 - 14:30',
                freePlaces: 5
              },
            
              {
                pk: '1093',
                when: '12. aprill 2024 14:30 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1094',
                when: '13. aprill 2024 11:00 - 14:30',
                freePlaces: 5
              },
            
              {
                pk: '1095',
                when: '13. aprill 2024 14:30 - 18:00',
                freePlaces: 5
              }
            
            ]
          },
        
          {
            shop: 'Võru Rimi supermarket (Võru)',
            shifts: [
            
              {
                pk: '1088',
                when: '12. aprill 2024 11:30 - 14:30',
                freePlaces: 5
              },
            
              {
                pk: '1089',
                when: '12. aprill 2024 14:30 - 18:00',
                freePlaces: 5
              },
            
              {
                pk: '1090',
                when: '13. aprill 2024 11:00 - 14:30',
                freePlaces: 5
              },
            
              {
                pk: '1091',
                when: '13. aprill 2024 14:30 - 18:00',
                freePlaces: 5
              }
            
            ]
          }
        
      ]
    
    };
'''
