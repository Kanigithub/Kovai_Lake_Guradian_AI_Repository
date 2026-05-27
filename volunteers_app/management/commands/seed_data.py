from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta

from volunteers_app.models import UserProfile, Badge, VolunteerBadge
from lakes_app.models import Lake, LakePhoto
from events_app.models import Event, EventRole, EventRegistration
from dashboard_app.models import Announcement, Message


class Command(BaseCommand):
    help = 'Seed the database with mock data for Kovai Lake Guardians'

    def handle(self, *args, **options):
        self.stdout.write('Seeding mock data...')

        # ── Badges ────────────────────────────────────────────────────────────
        badge_data = [
            ('First Step', 'Attended your first cleanup event', 'first_event', 'fas fa-shoe-prints'),
            ('Dedicated Cleaner', 'Attended 5 cleanup events', 'five_events', 'fas fa-broom'),
            ('Lake Champion', 'Attended 10 cleanup events', 'ten_events', 'fas fa-trophy'),
            ('Early Bird', 'Registered for an event more than a week in advance', 'early_bird', 'fas fa-sun'),
            ('Team Player', 'Participated in a group of 20+ volunteers', 'team_player', 'fas fa-users'),
            ('Eco Warrior', 'Contributed 50+ hours to lake cleanups', 'eco_warrior', 'fas fa-leaf'),
        ]
        badges = {}
        for name, desc, btype, icon in badge_data:
            b, _ = Badge.objects.get_or_create(
                badge_type=btype,
                defaults={'name': name, 'description': desc, 'icon': icon}
            )
            badges[btype] = b
        self.stdout.write(f'  Created {len(badges)} badges')

        # ── Organizer ─────────────────────────────────────────────────────────
        organizer, _ = User.objects.get_or_create(
            username='organizer',
            defaults={
                'first_name': 'Kanimozhi',
                'last_name': 'Sankar',
                'email': 'kanimozhi@cleanlakes.in',
                'is_staff': True,
            }
        )
        organizer.first_name = 'Kanimozhi'
        organizer.last_name = 'Sankar'
        organizer.email = 'kanimozhi@cleanlakes.in'
        organizer.set_password('organizer123')
        organizer.save()
        org_profile, _ = UserProfile.objects.get_or_create(user=organizer)
        org_profile.is_organizer = True
        org_profile.phone = '+91 98765 43210'
        org_profile.bio = 'Lead organizer for Coimbatore lake cleanup initiatives since 2022.'
        org_profile.skills = 'Event planning, Community outreach, Logistics'
        org_profile.availability_weekdays = True
        org_profile.availability_weekends = True
        org_profile.total_points = 500
        org_profile.save()

        # ── Volunteers ────────────────────────────────────────────────────────
        volunteers_data = [
            ('arun_kumar', 'Arun', 'Kumar', 'arun@example.com', '+91 94400 11111', 'Swimming, Photography', True, False, 120),
            ('meena_s', 'Meena', 'Sundar', 'meena@example.com', '+91 94400 22222', 'Botany, Waste management', False, True, 90),
            ('raj_v', 'Rajesh', 'Venkat', 'raj@example.com', '+91 94400 33333', 'First Aid, Diving', True, True, 200),
            ('lakshmi_n', 'Lakshmi', 'Nair', 'lakshmi@example.com', '+91 94400 44444', 'Documentation, Social media', False, True, 60),
            ('karthik_m', 'Karthik', 'Murugan', 'karthik@example.com', '+91 94400 55555', 'Engineering, Equipment handling', True, False, 150),
            ('deepa_r', 'Deepa', 'Rajan', 'deepa@example.com', '+91 94400 66666', 'Teaching, Community coordination', True, True, 80),
            ('siva_p', 'Sivaraj', 'Pandian', 'siva@example.com', '+91 94400 77777', 'Photography, Drone operation', False, True, 40),
            ('anitha_k', 'Anitha', 'Kumar', 'anitha@example.com', '+91 94400 88888', 'Ecology, Water testing', True, False, 110),
            # 100+ additional Tamil volunteers
            ('manivannan_k', 'Manivannan', 'Kanagaraj', 'manivannan.k@example.com', '+91 94401 00001', 'Community outreach, Logistics', True, True, 175),
            ('shalini_kal', 'Shalini', 'Kalyanam', 'shalini.kal@example.com', '+91 94401 00002', 'Social media, Event planning', False, True, 140),
            ('dhivya_p', 'Dhivya', 'Priyanka', 'dhivya.p@example.com', '+91 94401 00003', 'Water testing, Documentation', True, True, 160),
            ('murugesan_s', 'Murugesan', 'Subramaniam', 'murugesan.s@example.com', '+91 94401 00004', 'Engineering, Desilting', True, False, 130),
            ('kavitha_r', 'Kavitha', 'Ravichandran', 'kavitha.r@example.com', '+91 94401 00005', 'Botany, Planting', False, True, 95),
            ('selvam_t', 'Selvam', 'Thangavel', 'selvam.t@example.com', '+91 94401 00006', 'Swimming, Waste collection', True, True, 210),
            ('priya_v', 'Priya', 'Vijayakumar', 'priya.v@example.com', '+91 94401 00007', 'Teaching, Awareness drives', True, False, 85),
            ('senthil_a', 'Senthilkumar', 'Arumugam', 'senthil.a@example.com', '+91 94401 00008', 'Photography, Monitoring', False, True, 70),
            ('nirmala_c', 'Nirmala', 'Chandrasekaran', 'nirmala.c@example.com', '+91 94401 00009', 'First Aid, Healthcare', True, True, 115),
            ('balaji_m', 'Balaji', 'Manikandan', 'balaji.m@example.com', '+91 94401 00010', 'Logistics, Equipment handling', True, False, 190),
            ('suganya_p', 'Suganya', 'Palaniswami', 'suganya.p@example.com', '+91 94401 00011', 'Community coordination, Social media', False, True, 100),
            ('pandian_r', 'Pandian', 'Rajendran', 'pandian.r@example.com', '+91 94401 00012', 'Diving, Water safety', True, True, 155),
            ('vasantha_k', 'Vasantha', 'Krishnamurthy', 'vasantha.k@example.com', '+91 94401 00013', 'Documentation, Photography', False, True, 65),
            ('gopal_s', 'Gopalakrishnan', 'Sundaresan', 'gopal.s@example.com', '+91 94401 00014', 'Engineering, Construction', True, False, 145),
            ('revathi_m', 'Revathi', 'Muthusamy', 'revathi.m@example.com', '+91 94401 00015', 'Ecology, Botany', True, True, 180),
            ('arjun_n', 'Arjun', 'Natarajan', 'arjun.n@example.com', '+91 94401 00016', 'Drone operation, Mapping', False, True, 50),
            ('chitra_b', 'Chitra', 'Balasubramanian', 'chitra.b@example.com', '+91 94401 00017', 'Teaching, Community outreach', True, False, 105),
            ('saravanan_v', 'Saravanan', 'Venkataraman', 'saravanan.v@example.com', '+91 94401 00018', 'Waste management, Logistics', True, True, 230),
            ('lavanya_g', 'Lavanya', 'Ganesan', 'lavanya.g@example.com', '+91 94401 00019', 'Social media, Event planning', False, True, 75),
            ('durai_p', 'Duraisamy', 'Periyasamy', 'durai.p@example.com', '+91 94401 00020', 'Swimming, First Aid', True, False, 165),
            ('mythili_r', 'Mythili', 'Ramaswamy', 'mythili.r@example.com', '+91 94401 00021', 'Documentation, Water testing', True, True, 120),
            ('kannan_s', 'Kannan', 'Subramanian', 'kannan.s@example.com', '+91 94401 00022', 'Equipment handling, Engineering', False, True, 90),
            ('poornima_t', 'Poornima', 'Thiagarajan', 'poornima.t@example.com', '+91 94401 00023', 'Botany, Planting', True, False, 135),
            ('ezhilan_m', 'Ezhilan', 'Muthukumar', 'ezhilan.m@example.com', '+91 94401 00024', 'Photography, Monitoring', True, True, 195),
            ('padmavathi_s', 'Padmavathi', 'Sekar', 'padmavathi.s@example.com', '+91 94401 00025', 'Healthcare, First Aid', False, True, 60),
            ('vijay_a', 'Vijayaraj', 'Annamalai', 'vijay.a@example.com', '+91 94401 00026', 'Community coordination, Logistics', True, False, 170),
            ('sudha_k', 'Sudha', 'Krishnan', 'sudha.k@example.com', '+91 94401 00027', 'Social media, Documentation', True, True, 85),
            ('ravi_c', 'Ravishankar', 'Chelladurai', 'ravi.c@example.com', '+91 94401 00028', 'Diving, Water safety', False, True, 140),
            ('meenakshi_p', 'Meenakshi', 'Ponnusamy', 'meenakshi.p@example.com', '+91 94401 00029', 'Teaching, Awareness drives', True, False, 110),
            ('tamilarasan_v', 'Tamilarasan', 'Velayutham', 'tamilarasan.v@example.com', '+91 94401 00030', 'Engineering, Desilting', True, True, 215),
            ('jayalakshmi_r', 'Jayalakshmi', 'Raghunathan', 'jayalakshmi.r@example.com', '+91 94401 00031', 'Botany, Ecology', False, True, 70),
            ('palani_s', 'Palanisamy', 'Shanmugam', 'palani.s@example.com', '+91 94401 00032', 'Waste collection, Equipment handling', True, False, 155),
            ('usha_b', 'Usha', 'Bharathi', 'usha.b@example.com', '+91 94401 00033', 'Community outreach, Social media', True, True, 95),
            ('chelvan_m', 'Chelvan', 'Maran', 'chelvan.m@example.com', '+91 94401 00034', 'Photography, Drone operation', False, True, 45),
            ('hema_n', 'Hema', 'Narayanan', 'hema.n@example.com', '+91 94401 00035', 'Documentation, Water testing', True, False, 125),
            ('vignesh_r', 'Vignesh', 'Rathnam', 'vignesh.r@example.com', '+91 94401 00036', 'First Aid, Swimming', True, True, 185),
            ('saroja_k', 'Saroja', 'Kandasamy', 'saroja.k@example.com', '+91 94401 00037', 'Teaching, Planting', False, True, 80),
            ('baskaran_t', 'Baskaran', 'Tamilselvan', 'baskaran.t@example.com', '+91 94401 00038', 'Engineering, Monitoring', True, False, 200),
            ('divya_s', 'Divya', 'Suresh', 'divya.s@example.com', '+91 94401 00039', 'Ecology, Botany', True, True, 115),
            ('manikandan_p', 'Manikandan', 'Perumal', 'manikandan.p@example.com', '+91 94401 00040', 'Logistics, Community coordination', False, True, 160),
            ('parvathi_v', 'Parvathi', 'Venkatesan', 'parvathi.v@example.com', '+91 94401 00041', 'Social media, Event planning', True, False, 75),
            ('kumaresan_a', 'Kumaresan', 'Alagappan', 'kumaresan.a@example.com', '+91 94401 00042', 'Diving, Water safety', True, True, 145),
            ('sumathi_m', 'Sumathi', 'Murugesan', 'sumathi.m@example.com', '+91 94401 00043', 'Documentation, Photography', False, True, 90),
            ('ilango_s', 'Ilango', 'Sathyamurthy', 'ilango.s@example.com', '+91 94401 00044', 'Waste management, Equipment handling', True, False, 170),
            ('rajeswari_n', 'Rajeswari', 'Natarajan', 'rajeswari.n@example.com', '+91 94401 00045', 'Healthcare, First Aid', True, True, 105),
            ('sundaram_c', 'Sundaram', 'Chidambaram', 'sundaram.c@example.com', '+91 94401 00046', 'Photography, Monitoring', False, True, 55),
            ('kamala_r', 'Kamala', 'Ramachandran', 'kamala.r@example.com', '+91 94401 00047', 'Botany, Planting', True, False, 130),
            ('prasad_v', 'Prasad', 'Vijayan', 'prasad.v@example.com', '+91 94401 00048', 'Engineering, Desilting', True, True, 220),
            ('latha_s', 'Latha', 'Selvakumar', 'latha.s@example.com', '+91 94401 00049', 'Community outreach, Teaching', False, True, 85),
            ('anand_t', 'Anand', 'Thiruvengadam', 'anand.t@example.com', '+91 94401 00050', 'Swimming, Water safety', True, False, 150),
            ('nandini_k', 'Nandini', 'Karunakaran', 'nandini.k@example.com', '+91 94401 00051', 'Social media, Documentation', True, True, 100),
            ('suresh_p', 'Suresh', 'Palanivel', 'suresh.p@example.com', '+91 94401 00052', 'Logistics, Equipment handling', False, True, 165),
            ('valli_m', 'Valli', 'Murugan', 'valli.m@example.com', '+91 94401 00053', 'Ecology, Water testing', True, False, 120),
            ('hariharan_r', 'Hariharan', 'Ramasamy', 'hariharan.r@example.com', '+91 94401 00054', 'Drone operation, Photography', True, True, 195),
            ('selvi_a', 'Selvi', 'Annamalai', 'selvi.a@example.com', '+91 94401 00055', 'Event planning, Community coordination', False, True, 70),
            ('thangam_s', 'Thangam', 'Subramanian', 'thangam.s@example.com', '+91 94401 00056', 'First Aid, Healthcare', True, False, 140),
            ('mohan_v', 'Mohanraj', 'Velu', 'mohan.v@example.com', '+91 94401 00057', 'Engineering, Construction', True, True, 205),
            ('rani_k', 'Rani', 'Krishnaswamy', 'rani.k@example.com', '+91 94401 00058', 'Botany, Planting', False, True, 80),
            ('karthi_t', 'Karthikeyan', 'Thirumalai', 'karthi.t@example.com', '+91 94401 00059', 'Waste collection, Logistics', True, False, 155),
            ('ambika_s', 'Ambika', 'Sundarajan', 'ambika.s@example.com', '+91 94401 00060', 'Documentation, Social media', True, True, 95),
            ('thirumaran_p', 'Thirumaran', 'Palanisamy', 'thirumaran.p@example.com', '+91 94401 00061', 'Swimming, Diving', False, True, 175),
            ('geetha_r', 'Geetha', 'Rajan', 'geetha.r@example.com', '+91 94401 00062', 'Teaching, Community outreach', True, False, 110),
            ('maheswaran_a', 'Maheswaran', 'Arumugam', 'maheswaran.a@example.com', '+91 94401 00063', 'Monitoring, Water testing', True, True, 185),
            ('indira_m', 'Indira', 'Muruganantham', 'indira.m@example.com', '+91 94401 00064', 'Social media, Event planning', False, True, 65),
            ('rajan_s', 'Rajan', 'Somasundaram', 'rajan.s@example.com', '+91 94401 00065', 'Equipment handling, Engineering', True, False, 145),
            ('mangai_v', 'Mangai', 'Vairavan', 'mangai.v@example.com', '+91 94401 00066', 'Botany, Ecology', True, True, 100),
            ('perumal_k', 'Perumal', 'Karuppasamy', 'perumal.k@example.com', '+91 94401 00067', 'Waste management, Desilting', False, True, 170),
            ('santhi_n', 'Santhi', 'Nagarajan', 'santhi.n@example.com', '+91 94401 00068', 'First Aid, Healthcare', True, False, 125),
            ('dhinesh_r', 'Dhinesh', 'Raghupathi', 'dhinesh.r@example.com', '+91 94401 00069', 'Photography, Drone operation', True, True, 210),
            ('gomathi_s', 'Gomathi', 'Sekar', 'gomathi.s@example.com', '+91 94401 00070', 'Community coordination, Teaching', False, True, 75),
            ('murugan_t', 'Murugan', 'Thangaraj', 'murugan.t@example.com', '+91 94401 00071', 'Swimming, Water safety', True, False, 160),
            ('vasuki_p', 'Vasuki', 'Parthasarathy', 'vasuki.p@example.com', '+91 94401 00072', 'Documentation, Photography', True, True, 90),
            ('senthur_m', 'Senthur', 'Marimuthu', 'senthur.m@example.com', '+91 94401 00073', 'Engineering, Logistics', False, True, 135),
            ('alamelu_r', 'Alamelu', 'Radhakrishnan', 'alamelu.r@example.com', '+91 94401 00074', 'Ecology, Water testing', True, False, 180),
            ('bharath_s', 'Bharath', 'Subramaniam', 'bharath.s@example.com', '+91 94401 00075', 'Community outreach, Social media', True, True, 50),
            ('prema_k', 'Prema', 'Krishnamurthy', 'prema.k@example.com', '+91 94401 00076', 'Botany, Planting', False, True, 115),
            ('sathish_v', 'Sathish', 'Velmurugan', 'sathish.v@example.com', '+91 94401 00077', 'Equipment handling, Waste collection', True, False, 145),
            ('malathi_c', 'Malathi', 'Chellappan', 'malathi.c@example.com', '+91 94401 00078', 'First Aid, Healthcare', True, True, 190),
            ('prabhu_n', 'Prabhu', 'Nallasivam', 'prabhu.n@example.com', '+91 94401 00079', 'Drone operation, Monitoring', False, True, 60),
            ('rekha_t', 'Rekha', 'Thilagavathi', 'rekha.t@example.com', '+91 94401 00080', 'Teaching, Event planning', True, False, 130),
            ('chelladurai_m', 'Chelladurai', 'Manoharan', 'chelladurai.m@example.com', '+91 94401 00081', 'Engineering, Desilting', True, True, 200),
            ('kalpana_s', 'Kalpana', 'Sundaramurthy', 'kalpana.s@example.com', '+91 94401 00082', 'Social media, Documentation', False, True, 85),
            ('dinakaran_r', 'Dinakaran', 'Rangasamy', 'dinakaran.r@example.com', '+91 94401 00083', 'Swimming, Diving', True, False, 155),
            ('nalini_a', 'Nalini', 'Asokan', 'nalini.a@example.com', '+91 94401 00084', 'Botany, Ecology', True, True, 105),
            ('vijayakumar_p', 'Vijayakumar', 'Pillai', 'vijayakumar.p@example.com', '+91 94401 00085', 'Logistics, Community coordination', False, True, 170),
            ('malliga_s', 'Malliga', 'Suresh', 'malliga.s@example.com', '+91 94401 00086', 'Water testing, First Aid', True, False, 90),
            ('kumaran_v', 'Kumaran', 'Velayutham', 'kumaran.v@example.com', '+91 94401 00087', 'Photography, Monitoring', True, True, 215),
            ('ponni_m', 'Ponni', 'Murugappan', 'ponni.m@example.com', '+91 94401 00088', 'Teaching, Community outreach', False, True, 70),
            ('venkatesh_k', 'Venkatesh', 'Krishnan', 'venkatesh.k@example.com', '+91 94401 00089', 'Engineering, Equipment handling', True, False, 140),
            ('subha_r', 'Subha', 'Ramesh', 'subha.r@example.com', '+91 94401 00090', 'Event planning, Social media', True, True, 95),
            ('thiyagarajan_s', 'Thiyagarajan', 'Sundaram', 'thiyagarajan.s@example.com', '+91 94401 00091', 'Waste management, Desilting', False, True, 165),
            ('radha_n', 'Radha', 'Narayanasamy', 'radha.n@example.com', '+91 94401 00092', 'Documentation, Healthcare', True, False, 120),
            ('ashok_t', 'Ashok', 'Thangarajan', 'ashok.t@example.com', '+91 94401 00093', 'Swimming, Water safety', True, True, 185),
            ('komalavalli_p', 'Komalavalli', 'Palaniappan', 'komalavalli.p@example.com', '+91 94401 00094', 'Botany, Planting', False, True, 75),
            ('ilayaraja_m', 'Ilayaraja', 'Murugesan', 'ilayaraja.m@example.com', '+91 94401 00095', 'Photography, Drone operation', True, False, 150),
            ('savitha_v', 'Savitha', 'Venkataramanan', 'savitha.v@example.com', '+91 94401 00096', 'Community coordination, Teaching', True, True, 100),
            ('rathnam_s', 'Rathnam', 'Sathyanarayanan', 'rathnam.s@example.com', '+91 94401 00097', 'Engineering, Logistics', False, True, 175),
            ('thenmozhi_k', 'Thenmozhi', 'Kalidoss', 'thenmozhi.k@example.com', '+91 94401 00098', 'Ecology, Water testing', True, False, 110),
            ('srinivasan_r', 'Srinivasan', 'Ramamurthy', 'srinivasan.r@example.com', '+91 94401 00099', 'First Aid, Healthcare', True, True, 195),
            ('padma_c', 'Padma', 'Chandran', 'padma.c@example.com', '+91 94401 00100', 'Social media, Event planning', False, True, 65),
            ('natarajan_p', 'Natarajan', 'Periasamy', 'natarajan.p@example.com', '+91 94401 00101', 'Equipment handling, Waste collection', True, False, 135),
            ('kasthuri_s', 'Kasthuri', 'Subramanian', 'kasthuri.s@example.com', '+91 94401 00102', 'Documentation, Photography', True, True, 205),
        ]
        volunteer_users = []
        for username, first, last, email, phone, skills, weekday, weekend, points in volunteers_data:
            u, _ = User.objects.get_or_create(username=username, defaults={
                'first_name': first, 'last_name': last, 'email': email
            })
            u.set_password('volunteer123')
            u.save()
            p, _ = UserProfile.objects.get_or_create(user=u)
            p.phone = phone
            p.skills = skills
            p.availability_weekdays = weekday
            p.availability_weekends = weekend
            p.total_points = points
            p.bio = f'Passionate volunteer dedicated to keeping Coimbatore lakes clean.'
            p.save()
            volunteer_users.append(u)
        self.stdout.write(f'  Created {len(volunteer_users)} volunteers + 1 organizer')

        # ── Award badges to top volunteers ────────────────────────────────────
        for u in volunteer_users[:3]:
            VolunteerBadge.objects.get_or_create(user=u, badge=badges['first_event'])
        for u in volunteer_users[:2]:
            VolunteerBadge.objects.get_or_create(user=u, badge=badges['five_events'])
        VolunteerBadge.objects.get_or_create(user=volunteer_users[2], badge=badges['ten_events'])
        VolunteerBadge.objects.get_or_create(user=volunteer_users[2], badge=badges['eco_warrior'])

        # ── Lakes ─────────────────────────────────────────────────────────────
        valankulam, _ = Lake.objects.get_or_create(
            name='Valankulam Lake',
            defaults={
                'location': 'RS Puram, Coimbatore, Tamil Nadu',
                'description': (
                    'Valankulam Lake is one of the oldest and most iconic water bodies in Coimbatore. '
                    'Spread over 45 acres, it serves as a vital habitat for migratory birds and supports '
                    'local groundwater recharge. The lake is surrounded by a popular walking track frequented '
                    'by thousands of residents daily.'
                ),
                'ecology_info': (
                    'Home to over 60 species of birds including painted storks, pelicans, and herons. '
                    'The lake supports aquatic vegetation like lotus and water hyacinth. '
                    'Fish species include catla, rohu, and common carp. '
                    'The surrounding trees provide nesting grounds for egrets and cormorants.'
                ),
                'current_status': (
                    'Water quality has improved by 30% over the last year due to volunteer cleanup efforts. '
                    'Plastic waste has been significantly reduced along the bunds. '
                    'Two bio-ponds have been installed to filter inflow water. '
                    'Regular boat-based cleanups are ongoing.'
                ),
                'cleanup_needs': (
                    'Removal of invasive water hyacinth from the eastern shore. '
                    'Clearing plastic and domestic waste near the boat jetty. '
                    'Planting native tree saplings along the northern bund. '
                    'Installation of mesh filters at storm water drains.'
                ),
                'area_sq_km': 0.18,
                'pollution_level': 'moderate',
            }
        )

        ukkadam, _ = Lake.objects.get_or_create(
            name='Ukkadam Lake',
            defaults={
                'location': 'Ukkadam, Coimbatore, Tamil Nadu',
                'description': (
                    'Ukkadam Lake, also known as Periyakulam, is the largest lake in Coimbatore covering '
                    'over 1,300 acres. It is a critical source of drinking water and supports the livelihoods '
                    'of fishing communities. The lake faces significant pressure from urban runoff and '
                    'encroachment along its banks.'
                ),
                'ecology_info': (
                    'Supports diverse aquatic life including freshwater turtles, otters, and over 80 bird species. '
                    'Dense patches of reed beds provide breeding grounds for waterbirds. '
                    'Water chestnut and lotus are dominant aquatic plants. '
                    'The lake is an important node in the Coimbatore wetland network.'
                ),
                'current_status': (
                    'Facing high pollution load from surrounding residential areas. '
                    'Industrial effluents have raised biochemical oxygen demand (BOD) levels. '
                    'Encroachments have reduced the lake area by nearly 15% over two decades. '
                    'Active desilting drive underway with corporation support.'
                ),
                'cleanup_needs': (
                    'Large-scale plastic waste collection along the 8 km bund road. '
                    'Removal of sewage discharge points and installation of interceptors. '
                    'Desilting of inlet channels to improve water flow. '
                    'Community awareness drives in surrounding neighborhoods. '
                    'Restoration of shoreline vegetation with native species.'
                ),
                'area_sq_km': 5.26,
                'pollution_level': 'high',
            }
        )

        singanallur, _ = Lake.objects.get_or_create(
            name='Singanallur Lake',
            defaults={
                'location': 'Singanallur, Coimbatore, Tamil Nadu',
                'description': (
                    'Singanallur Lake is a medium-sized urban lake in eastern Coimbatore. '
                    'It supports local fisheries and acts as a flood retention basin. '
                    'The lake was recently designated as a bird sanctuary due to its rich avian diversity.'
                ),
                'ecology_info': (
                    'A recognized bird sanctuary hosting flamingos, pelicans, and painted storks during winter. '
                    'The lake supports freshwater ecosystems with diverse fish and amphibian populations. '
                    'Native vegetation includes water lily, reeds, and cattails.'
                ),
                'current_status': (
                    'Water quality is relatively good due to reduced industrial activity nearby. '
                    'Regular monitoring by Tamil Nadu Pollution Control Board is in place. '
                    'Bird population has increased by 25% in the past two years.'
                ),
                'cleanup_needs': (
                    'Removal of polythene bags and thermocol waste near picnic areas. '
                    'Controlling illegal sand mining activities. '
                    'Planting buffer zone vegetation to reduce runoff.'
                ),
                'area_sq_km': 0.65,
                'pollution_level': 'low',
            }
        )

        # ── Additional 5 lakes (completing all 8 major Coimbatore lakes) ────────
        selvampathy, _ = Lake.objects.get_or_create(
            name='Selvampathy Lake',
            defaults={
                'location': 'Selvampathy, Coimbatore, Tamil Nadu',
                'description': (
                    'Selvampathy Lake is one of the eight major tanks of Coimbatore, located in the '
                    'western part of the city. It is an important recharge basin for groundwater in the '
                    'surrounding residential areas and supports local agriculture. The lake is part of the '
                    'Noyyal River basin system that sustains Coimbatore\'s ecology.'
                ),
                'ecology_info': (
                    'Hosts several species of waterbirds including egrets and pond herons. '
                    'The shallow margins support aquatic vegetation such as reeds and water lily. '
                    'Acts as a buffer wetland improving downstream water quality. '
                    'Local communities depend on the lake for irrigation.'
                ),
                'current_status': (
                    'The lake faces moderate encroachment pressure from surrounding urban expansion. '
                    'Silt accumulation has reduced its water-holding capacity. '
                    'Community groups have begun awareness campaigns for its protection. '
                    'Regular water quality monitoring is being initiated.'
                ),
                'cleanup_needs': (
                    'Desilting operations to restore original storage capacity. '
                    'Removal of solid waste dumped along the lake margins. '
                    'Fencing of the lake boundary to prevent further encroachment. '
                    'Plantation of native shrubs and grasses on the bund.'
                ),
                'area_sq_km': 0.30,
                'pollution_level': 'medium',
            }
        )

        narasampathi, _ = Lake.objects.get_or_create(
            name='Narasampathi Lake',
            defaults={
                'location': 'Narasampathi, Coimbatore, Tamil Nadu',
                'description': (
                    'Narasampathi Lake is a medium-sized urban wetland located in eastern Coimbatore. '
                    'It serves as a critical stormwater retention basin protecting low-lying areas from '
                    'flooding during the northeast monsoon. The lake receives water from surrounding '
                    'catchment areas and contributes to recharging local aquifers.'
                ),
                'ecology_info': (
                    'Supports a diverse community of waterbirds and wading birds. '
                    'Aquatic vegetation including water hyacinth and lotus is present. '
                    'The lake provides habitat for freshwater fish and amphibians. '
                    'Seasonal migrants visit during winter months.'
                ),
                'current_status': (
                    'Urban runoff and sedimentation have reduced lake depth significantly. '
                    'Partial encroachments have occurred on the northern bank. '
                    'A desilting drive was carried out in 2022 by the Coimbatore Corporation. '
                    'The lake still fulfils its flood-moderation role during heavy rains.'
                ),
                'cleanup_needs': (
                    'Restoration of feeder channels blocked by construction debris. '
                    'Clearing garbage deposits along access roads. '
                    'Establishing a green buffer zone to filter agricultural runoff. '
                    'Reinstating traditional sluice gates for regulated water release.'
                ),
                'area_sq_km': 0.25,
                'pollution_level': 'medium',
            }
        )

        krishnampathi, _ = Lake.objects.get_or_create(
            name='Krishnampathi Lake',
            defaults={
                'location': 'Seeranaickenpalayam, Coimbatore, Tamil Nadu',
                'description': (
                    'Krishnampathi Lake, situated near Seeranaickenpalayam in northeastern Coimbatore, '
                    'is a tranquil urban lake celebrated for its rich birdlife. It is a favourite spot '
                    'for bird watchers and nature enthusiasts who flock here to observe migratory waterfowl. '
                    'The lake forms part of the wetland chain connecting the Noyyal River system.'
                ),
                'ecology_info': (
                    'A notable habitat for migratory ducks, painted storks, and herons. '
                    'Over 45 bird species have been recorded here during winter. '
                    'The lake supports thriving fish populations sustaining local fisher families. '
                    'Aquatic plants such as lotus and water chestnut dominate the shallows.'
                ),
                'current_status': (
                    'Water quality has shown improvement following recent clean-up events. '
                    'Bird sightings have increased, indicating a healthier ecosystem. '
                    'Encroachments on the eastern bank remain a concern. '
                    'Local NGOs and birding clubs are active in monitoring and conservation.'
                ),
                'cleanup_needs': (
                    'Clearing plastic litter from the popular birding viewpoints. '
                    'Removal of invasive water hyacinth from the centre of the lake. '
                    'Planting vetiver grass on eroding bund slopes. '
                    'Creating a designated bird-watching platform with minimal disturbance.'
                ),
                'area_sq_km': 0.20,
                'pollution_level': 'low',
            }
        )

        selvachinthamani, _ = Lake.objects.get_or_create(
            name='Selvachinthamani Lake',
            defaults={
                'location': 'Selvachinthamani, Coimbatore, Tamil Nadu',
                'description': (
                    'Selvachinthamani Lake lies upstream of Ukkadam Lake and feeds it via a canal, '
                    'playing a vital hydrological role in the Coimbatore tank cascade system. '
                    'It acts as a primary settling basin for water entering the larger Ukkadam Lake '
                    'to the south. The lake has cultural and religious significance for nearby communities.'
                ),
                'ecology_info': (
                    'The shallow basin supports diverse aquatic macrophytes including water lilies. '
                    'Home to a range of waterbirds including egrets, cormorants, and moorhens. '
                    'Fish species present include catfish and tilapia. '
                    'Seasonal influx of water improves local biodiversity significantly.'
                ),
                'current_status': (
                    'High siltation levels have reduced the lake\'s effective storage. '
                    'Sewage intrusion from adjoining areas is a concern. '
                    'Coimbatore Corporation has included the lake in its water body rejuvenation plan. '
                    'Volunteer groups regularly remove floating debris.'
                ),
                'cleanup_needs': (
                    'Urgent desilting to restore the cascading supply to Ukkadam Lake. '
                    'Interception of sewage inflows at source. '
                    'Strengthening the lake bund and planting native trees. '
                    'Community outreach to reduce direct waste disposal into the water.'
                ),
                'area_sq_km': 0.15,
                'pollution_level': 'high',
            }
        )

        kumaraswami, _ = Lake.objects.get_or_create(
            name='Kumaraswami Lake',
            defaults={
                'location': 'Coimbatore, Tamil Nadu',
                'description': (
                    'Kumaraswami Lake is the smallest of the eight major tanks of Coimbatore but plays '
                    'a crucial role in the local water table. Situated within a densely populated '
                    'neighbourhood, the lake is an island of nature that has survived decades of '
                    'urban sprawl. Conservation efforts by resident groups have kept the lake alive '
                    'against heavy development pressure.'
                ),
                'ecology_info': (
                    'Supports diverse waterbirds and small mammals along its vegetated margins. '
                    'Aquatic flora including rushes and water grass provide breeding cover. '
                    'The lake helps moderate local temperatures in a dense urban setting. '
                    'Seasonal fish population supports small-scale artisanal fishing.'
                ),
                'current_status': (
                    'Significant reduction in lake area due to encroachment over the decades. '
                    'Water quality is heavily impacted by surrounding drains. '
                    'Resident Welfare Association is actively lobbying for official protection status. '
                    'Area partially fenced after community protests against further encroachment.'
                ),
                'cleanup_needs': (
                    'Complete garbage removal and deep cleaning of the lake margins. '
                    'Diversion of stormwater drains away from the lake body. '
                    'Legal demarcation of full tank bed to prevent further land-grabbing. '
                    'Habitat restoration with native aquatic plants and bund vegetation.'
                ),
                'area_sq_km': 0.10,
                'pollution_level': 'high',
            }
        )

        # Add sample lake photo URLs
        # Delete old photos and replace with verified Wikimedia Commons images
        all_lakes = [valankulam, ukkadam, singanallur, selvampathy, narasampathi,
                     krishnampathi, selvachinthamani, kumaraswami]
        for lake_obj in all_lakes:
            lake_obj.photos.all().delete()

        photo_data = [
            # Valankulam Lake — beautiful sunset panoramic (Wikimedia Commons)
            (valankulam,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Valankulam_Lake_at_Sunset.jpg?width=1280',
             'Valankulam Lake at sunset — panoramic view', 'general'),

            # Ukkadam Lake — current real photos of the lake (Wikimedia Commons)
            (ukkadam,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Ukkadam_Lake,_Ukkadam,_Coimbatore,_Tamil_Nadu.jpg?width=1280',
             'Ukkadam Lake — current view, Coimbatore', 'general'),
            (ukkadam,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Ukkadam_Lake_Road_JEG_JEG6961.jpg?width=1280',
             'Ukkadam Lake road and bund panoramic', 'general'),
            (ukkadam,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Periya-Kulam-Ukkadam-Kovai.JPG?width=1280',
             'Periya Kulam (Ukkadam Lake) overview', 'before'),

            # Singanallur Lake — panoramic and wildlife photos (Wikimedia Commons)
            (singanallur,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Singanallur_Lake_JEG_JEG6969.jpg?width=1280',
             'Singanallur Lake panoramic view', 'general'),
            (singanallur,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Singanallur_Lake_JEG_JEG6970.jpg?width=1280',
             'Singanallur Lake wide view', 'general'),
            (singanallur,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Cormorants-Egrets-Singanallur_Lake.JPG?width=1280',
             'Cormorants and Egrets at Singanallur Lake', 'general'),

            # Selvampathy Lake — natural tank near Noyyal River, Coimbatore (Wikimedia Commons confirmed)
            (selvampathy,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Natural_Tank_in_Vellalur_near_Noyyal_River,_Coimbatore.jpg?width=1280',
             'Natural tank near Noyyal River, Coimbatore — similar to Selvampathy Lake', 'general'),
            (selvampathy,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Ukkadam_Lake_Road_JEG_JEG6964.jpg?width=1280',
             'Coimbatore lake bund — representative view of urban tank ecosystem', 'general'),

            # Narasampathi Lake — Vellalore Tank (Coimbatore urban tank, same type) — Wikimedia Commons confirmed
            (narasampathi,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Vellalore_Tank_in_January_2011.jpg?width=1280',
             'Vellalore Tank, Coimbatore — representative Coimbatore urban lake in January', 'general'),
            (narasampathi,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Ukkadam_Lake_Road_JEG_JEG6965.jpg?width=1280',
             'Coimbatore lake bund road — urban tank ecosystem', 'general'),

            # Krishnampathi Lake — Unsplash photo explicitly tagged "Krishnampathi Lake, Seeranaickenpalayam, Coimbatore"
            (krishnampathi,
             'https://source.unsplash.com/ICXvMKUOuvw/1280x720',
             'Ducks on Krishnampathi Lake, Seeranaickenpalayam, Coimbatore', 'general'),
            (krishnampathi,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Ukkadam_big_lake.jpg?width=1280',
             'Urban lake ecosystem — Coimbatore wetland, similar scale to Krishnampathi', 'general'),

            # Selvachinthamani Lake — Coimbatore lake algal bloom (Wikimedia Commons, Lakes of Coimbatore category)
            (selvachinthamani,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Algal_blooming.jpg?width=1280',
             'Algal bloom on a Coimbatore lake — pollution condition at Selvachinthamani', 'before'),
            (selvachinthamani,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Ukkadam_Lake_Road_JEG_JEG6962.jpg?width=1280',
             'Coimbatore lake bund — Ukkadam area near Selvachinthamani', 'general'),

            # Kumaraswami Lake — Coimbatore lake algal bloom 2 (Wikimedia Commons, Lakes of Coimbatore category)
            (kumaraswami,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Algal_blooming_2.jpg?width=1280',
             'Algal bloom on Coimbatore lake — pollution state at Kumaraswami Lake', 'before'),
            (kumaraswami,
             'https://commons.wikimedia.org/wiki/Special:FilePath/Ukkadam_big_lake1.jpg?width=1280',
             'Coimbatore urban lake — water body similar in scale to Kumaraswami', 'general'),
        ]
        for lake, url, caption, ptype in photo_data:
            LakePhoto.objects.create(lake=lake, image_url=url, caption=caption, photo_type=ptype)
        self.stdout.write('  Created 8 lakes with photos (all major Coimbatore lakes)')

        # ── Events ────────────────────────────────────────────────────────────
        today = date.today()
        events_data = [
            {
                'title': 'Valankulam Mega Cleanup Drive',
                'description': (
                    'Join us for the biggest cleanup drive at Valankulam Lake this season! '
                    'We will be collecting plastic waste, removing invasive water hyacinth, '
                    'and planting native saplings along the bund. Refreshments provided. '
                    'Please bring gloves, wear comfortable shoes, and carry a water bottle.'
                ),
                'lake': valankulam,
                'location': 'Valankulam Lake, RS Puram – Main Gate Entrance',
                'date': today + timedelta(days=7),
                'start_time': time(7, 0),
                'end_time': time(11, 0),
                'required_materials': 'Gloves, Water bottle, Sunscreen, Comfortable shoes',
                'max_volunteers': 50,
                'status': 'upcoming',
            },
            {
                'title': 'Ukkadam Lake Bund Restoration',
                'description': (
                    'A focused effort to restore the northern bund of Ukkadam Lake. '
                    'Activities include planting vetiver grass, removing encroachments, '
                    'and clearing storm drain blockages. Heavy-duty gloves provided on site. '
                    'Lunch will be sponsored by Coimbatore Green Trust.'
                ),
                'lake': ukkadam,
                'location': 'Ukkadam Lake, Northern Bund – Near Police Quarters',
                'date': today + timedelta(days=14),
                'start_time': time(6, 30),
                'end_time': time(12, 0),
                'required_materials': 'Boots, Work clothes, Hat',
                'max_volunteers': 80,
                'status': 'upcoming',
            },
            {
                'title': 'Singanallur Bird Sanctuary Cleanup',
                'description': (
                    'Help protect the Singanallur Bird Sanctuary by removing waste from picnic areas '
                    'and installing bio-degradable waste bins. This event is family-friendly and '
                    'includes a guided bird-watching session after the cleanup.'
                ),
                'lake': singanallur,
                'location': 'Singanallur Lake – Picnic Zone Entrance',
                'date': today + timedelta(days=21),
                'start_time': time(7, 30),
                'end_time': time(10, 30),
                'required_materials': 'Gloves, Binoculars (optional), Water bottle',
                'max_volunteers': 30,
                'status': 'upcoming',
            },
            {
                'title': 'Valankulam Water Quality Workshop',
                'description': (
                    'A combined field session and workshop on water quality testing at Valankulam Lake. '
                    'Volunteers will collect water samples, conduct basic BOD/pH tests, and attend '
                    'a talk by environmental engineers on urban lake restoration techniques.'
                ),
                'lake': valankulam,
                'location': 'Valankulam Lake – Boathouse Pavilion',
                'date': today + timedelta(days=30),
                'start_time': time(9, 0),
                'end_time': time(13, 0),
                'required_materials': 'Notebook, Pen, Closed-toe shoes',
                'max_volunteers': 25,
                'status': 'upcoming',
            },
            {
                'title': 'Krishnampathi Lake Restoration Day',
                'description': (
                    'A community restoration event at Krishnampathi Lake focusing on clearing water hyacinth, '
                    'planting native reeds, and repairing footpaths. Ideal for volunteers who enjoy hands-on work.'
                ),
                'lake': krishnampathi,
                'location': 'Krishnampathi Lake – Western Bund Entrance',
                'date': today + timedelta(days=35),
                'start_time': time(7, 30),
                'end_time': time(12, 30),
                'required_materials': 'Gloves, Long sleeves, Water bottle',
                'max_volunteers': 40,
                'status': 'upcoming',
            },
            {
                'title': 'Selvachinthamani Eco-Build Day',
                'description': (
                    'Join the Selvachinthamani Eco-Build Day to construct trash traps, plant vetiver grass, '
                    'and set up awareness signs around the lake. Volunteers will learn about urban wetland conservation.'
                ),
                'lake': selvachinthamani,
                'location': 'Selvachinthamani Lake – Canal End',
                'date': today + timedelta(days=42),
                'start_time': time(8, 0),
                'end_time': time(12, 0),
                'required_materials': 'Work gloves, Hat, Comfortable shoes',
                'max_volunteers': 35,
                'status': 'upcoming',
            },
            {
                'title': 'Kumaraswami Lake Community Green Walk',
                'description': (
                    'A gentle green walk around Kumaraswami Lake that combines cleanup with a short conservation '
                    'talk. Perfect for families and volunteers who want a low-impact, high-value experience.'
                ),
                'lake': kumaraswami,
                'location': 'Kumaraswami Lake – South Entrance',
                'date': today + timedelta(days=50),
                'start_time': time(8, 30),
                'end_time': time(11, 30),
                'required_materials': 'Comfortable shoes, Water bottle, Mask',
                'max_volunteers': 30,
                'status': 'upcoming',
            },
            {
                'title': 'Ukkadam Community Awareness March',
                'description': (
                    'Walk along the Ukkadam Lake bund road and spread awareness about lake conservation '
                    'to local residents. Distribute pamphlets, interact with fishing communities, and '
                    'collect pledges for responsible waste disposal. This is a non-physical, outreach event.'
                ),
                'lake': ukkadam,
                'location': 'Ukkadam Lake – Main Bund Road',
                'date': today - timedelta(days=10),
                'start_time': time(8, 0),
                'end_time': time(11, 0),
                'required_materials': 'Walking shoes, Cap',
                'max_volunteers': 40,
                'status': 'completed',
            },
            {
                'title': 'Valankulam Night Cleanup',
                'description': (
                    'A special evening cleanup targeting the litter left by weekend visitors. '
                    'Illuminated vests and torches provided. '
                    'Great opportunity to meet fellow eco-warriors in a unique setting!'
                ),
                'lake': valankulam,
                'location': 'Valankulam Lake – Walking Track',
                'date': today - timedelta(days=20),
                'start_time': time(18, 30),
                'end_time': time(21, 0),
                'required_materials': 'Torch, Reflective vest (provided), Gloves',
                'max_volunteers': 35,
                'status': 'completed',
            },
        ]

        created_events = []
        for ed in events_data:
            ev, _ = Event.objects.get_or_create(
                title=ed['title'],
                defaults={**ed, 'created_by': organizer}
            )
            created_events.append(ev)

        # ── Event Roles ───────────────────────────────────────────────────────
        roles_by_event = {
            created_events[0].title: [
                ('Waste Collector', 'Collect and bag plastic and solid waste along the bund', 20),
                ('Planting Crew', 'Plant native saplings under the guidance of horticulturists', 15),
                ('Water Hyacinth Removal', 'Remove invasive water hyacinth from the eastern shore', 10),
                ('Coordinator', 'Manage volunteer groups and distribute materials', 5),
            ],
            created_events[1].title: [
                ('Bund Planting Team', 'Plant vetiver grass along the northern bund', 30),
                ('Drain Clearing Crew', 'Clear blockages from storm water drains', 20),
                ('Documentation Team', 'Photograph and document progress for records', 10),
                ('Community Liaison', 'Coordinate with local residents and fishermen', 10),
                ('Safety Officer', 'Ensure volunteer safety during heavy-duty tasks', 5),
            ],
            created_events[2].title: [
                ('Waste Picker', 'Collect litter from picnic and entry zones', 15),
                ('Bin Installation Crew', 'Assemble and place biodegradable waste bins', 8),
                ('Bird Watch Guide', 'Lead the guided bird-watching session post-cleanup', 3),
            ],
        }

        for ev in created_events:
            roles = roles_by_event.get(ev.title, [
                ('General Volunteer', 'Assist with all cleanup activities', ev.max_volunteers)
            ])
            for role_name, role_desc, max_vol in roles:
                EventRole.objects.get_or_create(
                    event=ev, name=role_name,
                    defaults={'description': role_desc, 'max_volunteers': max_vol}
                )

        # ── Event Registrations ───────────────────────────────────────────────
        reg_count = 0
        upcoming_events = [e for e in created_events if e.status == 'upcoming']
        completed_events = [e for e in created_events if e.status == 'completed']

        for i, vol in enumerate(volunteer_users):
            ev = upcoming_events[i % len(upcoming_events)]
            role = ev.roles.first()
            _, created = EventRegistration.objects.get_or_create(
                volunteer=vol, event=ev,
                defaults={'role': role, 'status': 'registered'}
            )
            if created:
                reg_count += 1

        # Register some volunteers for completed events
        for i, vol in enumerate(volunteer_users[:4]):
            ev = completed_events[i % len(completed_events)]
            role = ev.roles.first()
            _, created = EventRegistration.objects.get_or_create(
                volunteer=vol, event=ev,
                defaults={'role': role, 'status': 'attended', 'hours_logged': 3}
            )
            if created:
                reg_count += 1

        self.stdout.write(f'  Created {len(created_events)} events, {reg_count} registrations')

        # ── Announcements ─────────────────────────────────────────────────────
        announcements = [
            (
                'Welcome to Kovai Lake Guardians!',
                'We are thrilled to launch the Kovai Lake Guardians volunteer platform for Coimbatore. '
                'Together, we can restore Valankulam, Ukkadam, and Singanallur lakes to their former glory. '
                'Register for an upcoming event and earn your first badge today!',
                None, True
            ),
            (
                'Mega Cleanup Drive – 50 Volunteers Needed!',
                'Our biggest event yet — the Valankulam Mega Cleanup Drive — needs 50 dedicated volunteers. '
                'Slots are filling fast. Register now to secure your spot. '
                'All materials provided. Refreshments and certificates for all participants.',
                created_events[0], True
            ),
            (
                'Ukkadam Bund Restoration — Corporate Volunteers Welcome',
                'We are partnering with local companies for the Ukkadam Bund Restoration event. '
                'CSR teams can register groups of up to 15. Contact us for bulk registration assistance. '
                'This is a rare chance to make a visible impact on Coimbatore\'s largest lake.',
                created_events[1], True
            ),
            (
                'Community Awareness March — Completed Successfully!',
                'Thank you to all 38 volunteers who joined the Ukkadam Community Awareness March! '
                'We distributed 500+ pamphlets and collected 200 plastic-free pledges from local residents. '
                'Your efforts are making a real difference. Watch this space for more events!',
                created_events[4], True
            ),
        ]
        for title, content, event, published in announcements:
            Announcement.objects.get_or_create(
                title=title,
                defaults={
                    'content': content,
                    'author': organizer,
                    'event': event,
                    'is_published': published,
                }
            )
        self.stdout.write(f'  Created {len(announcements)} announcements')

        # ── Messages ──────────────────────────────────────────────────────────
        msg_data = [
            (
                created_events[0],
                'Reminder: Valankulam Cleanup Drive Next Week',
                'Dear Volunteers,\n\nThis is a reminder that the Valankulam Mega Cleanup Drive is happening next week. '
                'Please arrive by 6:45 AM at the Main Gate Entrance. Gloves will be provided but please bring your own water bottle. '
                'Looking forward to seeing you all there!\n\nBest regards,\nOrganizer Team'
            ),
            (
                created_events[1],
                'Ukkadam Bund Restoration – What to Bring',
                'Dear Volunteers,\n\nFor the Ukkadam Bund Restoration event, please wear sturdy boots and work clothes '
                'as the terrain can be muddy. Heavy-duty gloves will be provided. Lunch is sponsored — no need to bring food. '
                'We will divide into 5 teams of 16 each.\n\nThank you for your commitment!\n\nOrganizer Team'
            ),
            (
                None,
                'New Badges Now Available!',
                'Dear all,\n\nWe have added 6 new achievement badges to the platform. '
                'Attend your first event to earn the "First Step" badge, and keep coming back to unlock more. '
                'Check your profile to see your current badges and points on the leaderboard.\n\nKovai Lake Guardians Team'
            ),
        ]
        for event, subject, content in msg_data:
            Message.objects.get_or_create(
                subject=subject,
                defaults={'sender': organizer, 'event': event, 'content': content}
            )
        self.stdout.write(f'  Created {len(msg_data)} messages')

        self.stdout.write(self.style.SUCCESS('\nMock data seeded successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Organizer  -> username: organizer   | password: organizer123')
        self.stdout.write('  Volunteers -> username: arun_kumar  | password: volunteer123')
        self.stdout.write('              (same password for all volunteer accounts)')
