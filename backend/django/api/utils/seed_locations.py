import logging
from django.db import transaction, connection

logger = logging.getLogger(__name__)

# Hierarchy data till villages, of Nalgonda District
# Divisions contain mandal named keys which are in-turn keys to their respective village lists
NALGONDA_DATA = {
    "district": {"name": "Nalgonda", "code": "NLG"},
    "divisions": {
        "Nalgonda": {
            "Nalgonda": ["Ammaguda", "Anantharam", "Annareddy Guda", "Anneparthy", "Appaji Peta", "Arjalabavi", "Budharam", "Chandan Palle", "Cherlapalle", "Dandampalle", "Donakal", "G.K.Annaram", "Gundlapalle", "K.Kondaram", "Kanchanpalle", "Khudavanpur", "Kotha Palle", "M.Domalapalle", "Mamillagudem", "Medla Duppala Palle", "Musham Palle", "Narsing Batla", "P.Domalapalle", "Rasoolpur", "Velugu Palle", "Other"],
            "Chityal": ["Aipoor", "Chinakaparthy", "Chityala", "Gundram Palle", "Nerada", "Pedakaparthy", "Pere Palle", "Pittam Palle", "Shivaneni Gudem", "Sunkene Palle", "Talla Yellemla", "Urmadla", "Vanipakala", "Veliminedu", "Wattimarthy", "Yelikatta", "Other"],
            "Kanagal": ["Boinpalle", "Chinna Madharam", "Dermaram", "Kanagal", "Kishtapur", "Kurmapalle", "Pangada", "Puvvada", "Regatte", "Sherepalle", "Tirumalgiri", "Yadavally", "Other"],
            "Kattangoor": ["Aiti Pamula", "Bollepalle", "Dugnevally", "Gopulapur", "Kadjikal", "Kalmcheru", "Kattangoor", "Kurmaidu", "Mallaram", "Pamanagundla", "Yerraram", "Other"],
            "Nakrekal": ["Adavi Bollaram", "Chandam Palle", "Chandupatla", "Gorenkal Palle", "Kadaparthy", "Mandalapur", "Mangali Palle", "Marrur", "Nakrekal", "Nellibanda", "Nomula", "Ogode", "Palem", "Tatikal", "Tettekunta", "Vallabhapur", "Other"],
            "Narketpalli": ["Akkenepalle", "Auravani", "Brahmanavellemla", "Cherughat", "Chittaloor", "Damerneenipalle", "Eshwarpalle", "Mamidala", "Narketpalle", "Nemmani", "Pallepahad", "Shapalle", "Tondupalle", "Yellareddyguda", "Other"],
            "Shaligowraram": ["Adavivemula", "Ammanabole", "Guda Pur", "Gurthoor", "Iduluru", "Ithikyal", "Madhavaram", "Nagaramsaligram", "Othkuru", "Peramenipalle", "Shaligowraram", "Vallala", "Vangamarthy", "Other"],
            "Thipparthy": ["Anajpur", "Indugula", "Jungur", "Kannekal", "Mamidi", "Matur", "Pajjur", "Sarvaram", "Thangedpalle", "Thipparthy", "Yerraguntla", "Other"],
            "Kethepalli": ["Bheemaram", "Boigudem", "Gudivada", "Inupamula", "Kappala", "Kasanagode", "Kethepalli", "Koppole", "Korlapahad", "Moodugudem", "Thungathurthy", "Other"],
        },
        "Miryalaguda": {
            "Miryalaguda": ["Ailapuram", "Alagadapa", "Annaram", "Chillapuram", "Chintha Palle", "Gudivada", "Kaloor", "Mulkalkalva", "Nandi Pahad", "Rayanpalem", "Tadkamalla", "Venkatadri Palem", "Yadgarpalle", "Other"],
            "Damaracherla": ["Damaracherla", "Irkyapuram", "Kallapalle", "Kondrapole", "Narsapur", "Tallaveerappagudem", "Vadapally", "Veerlapalem", "Other"],
            "Vemulapally": ["Amanagallu", "Anumula", "Bugga", "Chityala", "Kancharlapalle", "Molkacherla", "Rasalipuram", "Settipalem", "Vemulapally", "Other"],
            "Anumula (Haliya)": ["Anumula", "Hazarigudem", "Kothapalli", "Mukkamula", "Naidupalem", "Peroor", "Pulimamidi", "Srinadhapuram", "Yacharam", "Other"],
            "Nidamanur": ["Gumpula", "Indurthi", "Marreddigudem", "Nidamanur", "Rajavaram", "Tummadam", "Venkatapur", "Other"],
            "Peddavoora": ["Chalakurthy", "Nagamadugu", "Peddavoora", "Pothunuru", "Sunkishala", "Tanimadugu", "Teerthapalle", "Other"],
            "Tripuraram": ["Anajpur", "Babusaipet", "Chowdur", "Kondayapalem", "Nimmikal", "Ryelpalle", "Tripuraram", "Other"],
            "Madugulapally": ["Gummadavally", "Indugula", "Madugulapally", "Pamulpahad", "Peddevidu", "Thimmadam", "Other"],
            "Tirumalagiri (Sagar)": ["Alwal", "Nellikallu", "Nellikal", "Ragadapa", "Tirumalagiri", "Yellapuram", "Other"],
        },
        "Devarakonda": {
            "Devarakonda": ["Atchampet", "Channamneni Palle", "Chennaram", "Chinna Adiserla Palle", "Chinthakuntla", "Devarakonda", "Doniyala", "Fakeerpoor", "Gottimukkala", "Gummadavally", "Iddam Palle", "Kacharam", "Kondabheemana Palle", "Madmadka", "Mudigonda", "Mynam Palle", "Padamati Palle", "Sere Palle", "Tatikole", "Yepoor", "Other"],
            "Chandampet": ["Achampet Patti", "Chandampet", "Chitriyala", "Guvvalagutta", "Kambalapalli", "Korutla", "Murpunuthala", "Teldeverapalli", "Other"],
            "Chinthapalli": ["Chinthapally", "Gollapally", "Kurmaidu", "Mallareddy Pally", "Nelvalapally", "Thakkallapally", "Vinjamoor", "Other"],
            "Gurrampode": ["Gurrampode", "Junuthala", "Koppole", "Mallepalle", "Pittalguda", "Tenepalle", "Other"],
            "Kondamallepally": ["Doniyala", "Gazinagar", "Kondamallepally", "Pervail", "Yellapuram", "Other"],
            "Gundlapalli (Dindi)": ["Brahmanapalle", "Cherukupalle", "Gundlapalli", "Kanchinapalle", "Khajipahad", "Singampalle", "Other"],
            "Neredugommu": ["Bugga Thanda", "Chakalisherpally", "Neredugommu", "Vavila Palle", "Other"],
        },
        "Chandur": {
            "Chandur": ["Angadipeta", "Bangarigadda", "Bodangi Parthy", "Chandur", "Donipamula", "Gundrepalle", "Idikuda", "Kasthala", "Kondapuram", "Nermata", "Pullemla", "Sirdepalle", "Theratpalle", "Thummalapalle", "Other"],
            "Munugodu": ["Chalakurthy", "Chinnakondur", "Kishtapuram", "Kommapalle", "Munugodu", "Nandikonda", "Palivela", "Other"],
            "Gattuppal": ["Gattuppal", "Nandipahad", "Puttapaka", "Sultanpur", "Other"],
            "Nampalli": ["Bheemaram", "Gaddamvari Yadavally", "Nampalli", "Pasnoor", "Peesari", "Revalle", "Other"],
            "Marriguda": ["Damera Bheeman Palle", "Marriguda", "Sarabha Puram", "Yacharam", "Other"],
        },
    },
}


def _tables_exist(required_tables: list[str]) -> bool:
    existing_tables = set(connection.introspection.table_names())
    return all(table in existing_tables for table in required_tables)


def seed_nalgonda_locations(sender=None, **kwargs):
    """
    Seed Nalgonda district → revenue divisions → mandals → villages.
    Idempotent and safe to run multiple times.
    Includes both hierarchical location data and villages.
    """

    try:
        required_tables = {
            "api_district",
            "api_revenuedivision",
            "api_mandal",
            "api_village",
        }

        if not _tables_exist(required_tables):
            logger.warning(
                "Location tables not ready; skipping Nalgonda seed",
                extra={"missing_tables": list(required_tables)},
            )
            return

        # Lazy import (apps are ready now)
        from api.models.location import District, RevenueDivision, Mandal, Village
        from api.utils.translate import translate

        with transaction.atomic():
            district, created = District.objects.get_or_create(
                code=NALGONDA_DATA["district"]["code"],
                defaults={"name": NALGONDA_DATA["district"]["name"]},
            )

            logger.info(
                "District %s",
                "created" if created else "already exists",
                extra={"district": "Nalgonda"},
            )

            villages_created = 0
            
            for division_name, mandals_dict in NALGONDA_DATA["divisions"].items():
                division, _ = RevenueDivision.objects.get_or_create(
                    division_name=division_name,
                    district=district,
                    defaults={
                        "division_code": division_name.upper()[:10],
                    },
                )

                for mandal_index, (mandal_name, villages_list) in enumerate(mandals_dict.items(), start=1):
                    mandal, _ = Mandal.objects.get_or_create(
                        mandal_name=mandal_name,
                        division=division,
                        defaults={
                            "mandal_code": f"{division_name[:3].upper()}-{mandal_index}",
                        },
                    )
                    
                    # Seed villages for this mandal
                    for village_index, village_name in enumerate(villages_list, start=1):
                        Village.objects.get_or_create(
                            village_name=village_name,
                            mandal=mandal,
                            defaults={
                                "village_code": f"{mandal.mandal_code}V{village_index:03d}",
                                "local_name": translate(village_name, "te"),
                                "display_order": village_index,
                            },
                        )
                        villages_created += 1

        logger.info(
            "Nalgonda district data seeded successfully",
            extra={
                "district": "Nalgonda",
                "divisions": len(NALGONDA_DATA["divisions"]),
                "villages_created": villages_created,
            },
        )

    except Exception:
        logger.exception("Failed to seed Nalgonda district data")
