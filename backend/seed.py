"""
Database seed script for BoardingEdu demo data.

Creates tables (if needed), facilities, demo admin/parent users,
and ~13 fictional schools with fees, facilities, infrastructure, and images.

Usage (from backend/):
    python seed.py

Requires DATABASE_URL and optional DEMO_* credentials in .env
"""

import sys

from werkzeug.security import generate_password_hash

from app import create_app
from config import Config
from extensions import db
from models import (
    AdmissionEnquiry,
    Facility,
    Infrastructure,
    School,
    SchoolFacility,
    SchoolFee,
    SchoolImage,
    Shortlist,
    User,
)


FACILITY_DEFS = [
    ("Library", "Well-stocked library with digital resources"),
    ("Computer Lab", "Modern computer laboratory with internet access"),
    ("Science Lab", "Physics, chemistry and biology laboratories"),
    ("Sports Complex", "Indoor and outdoor sports facilities"),
    ("Swimming Pool", "On-campus swimming pool"),
    ("Transportation", "School bus and transport routes"),
    ("Hostel", "Residential boarding facilities"),
    ("Auditorium", "Multi-purpose auditorium for events"),
    ("Cafeteria", "Hygienic cafeteria / dining hall"),
    ("Medical Room", "On-campus infirmary with trained staff"),
    ("Smart Classrooms", "AV-enabled digital classrooms"),
    ("Playground", "Spacious outdoor playground"),
]


# Demo campus images (public placeholders — replace with own assets later)
def _img(seed: int) -> str:
    return f"https://picsum.photos/seed/boardingedu{seed}/800/500"


def _fee_row(class_name, admission, tuition, hostel, transport, other):
    annual = admission + tuition + hostel + transport + other
    return {
        "class_name": class_name,
        "admission_fee": admission,
        "tuition_fee": tuition,
        "hostel_fee": hostel,
        "transport_fee": transport,
        "other_fee": other,
        "annual_fee": annual,
    }


SCHOOL_DEFS = [
    {
        "name": "Horizon Valley International School",
        "city": "Mumbai",
        "state": "Maharashtra",
        "board": "IB",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 4.6,
        "min_fee": 280000,
        "max_fee": 420000,
        "address": "12 Palm Grove Road, Bandra West",
        "phone": "+91-22-40001001",
        "email": "admissions@horizonvalley.demo",
        "website": "https://horizonvalley.demo",
        "description": (
            "DEMO DATA: A fictional IB day school focused on inquiry-based learning, "
            "global citizenship, and strong parent partnership programmes."
        ),
        "academic_info": "IB Primary Years and Middle Years programmes with bilingual support.",
        "sports_info": "Football, basketball, athletics, and swimming partnerships.",
        "transport_info": "AC bus routes covering western and central Mumbai suburbs.",
        "hostel_info": "Hostel not available — day school only.",
        "admission_process": (
            "Online enquiry → campus visit → assessment → interaction → offer letter. "
            "(Demo process for evaluation purposes.)"
        ),
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Swimming Pool",
            "Transportation",
            "Auditorium",
            "Smart Classrooms",
        ],
        "fees": [
            _fee_row("Grade 1–5", 50000, 220000, 0, 35000, 15000),
            _fee_row("Grade 6–10", 55000, 280000, 0, 35000, 20000),
        ],
        "infrastructure": [
            ("Campus", "4-acre campus with landscaped courtyards (demo)."),
            ("Classrooms", "Air-conditioned smart classrooms with interactive boards."),
            ("Safety", "CCTV coverage and visitor management system."),
        ],
        "images": [
            (_img(101), "Campus exterior (demo image)"),
            (_img(102), "Learning space (demo image)"),
        ],
    },
    {
        "name": "Sahyadri Crest Public School",
        "city": "Pune",
        "state": "Maharashtra",
        "board": "CBSE",
        "school_type": "Day-Boarding",
        "gender": "Co-ed",
        "hostel_available": True,
        "rating": 4.4,
        "min_fee": 120000,
        "max_fee": 260000,
        "address": "Survey No. 45, Baner–Balewadi Link Road",
        "phone": "+91-20-40002002",
        "email": "hello@sahyadricrest.demo",
        "website": "https://sahyadricrest.demo",
        "description": (
            "DEMO DATA: Fictional CBSE school with optional day-boarding, "
            "strong STEM clubs, and weekend enrichment activities."
        ),
        "academic_info": "CBSE curriculum with Olympiad mentoring and lab-heavy STEM tracks.",
        "sports_info": "Cricket nets, athletics track, and indoor badminton courts.",
        "transport_info": "Routes across Baner, Aundh, Hinjewadi, and Kothrud.",
        "hostel_info": "Supervised day-boarding till 7 PM; limited weekly boarding beds.",
        "admission_process": "Application form → entrance test → parent meeting → confirmation.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Hostel",
            "Transportation",
            "Cafeteria",
            "Medical Room",
            "Playground",
        ],
        "fees": [
            _fee_row("Class 1–5", 25000, 90000, 40000, 20000, 8000),
            _fee_row("Class 6–10", 30000, 110000, 55000, 22000, 10000),
        ],
        "infrastructure": [
            ("Campus", "Spacious hill-view campus with open play fields (demo)."),
            ("Boarding", "Separate supervised boarding wings for boys and girls."),
            ("Labs", "Dedicated robotics and maker space."),
        ],
        "images": [(_img(201), "Main gate (demo)"), (_img(202), "Sports field (demo)")],
    },
    {
        "name": "Maple Grove Boarding Academy",
        "city": "Dehradun",
        "state": "Uttarakhand",
        "board": "ICSE",
        "school_type": "Boarding",
        "gender": "Co-ed",
        "hostel_available": True,
        "rating": 4.7,
        "min_fee": 350000,
        "max_fee": 520000,
        "address": "Rajpur Road Extension, Mussoorie foothills",
        "phone": "+91-135-40003003",
        "email": "office@maplegrove.demo",
        "website": "https://maplegrove.demo",
        "description": (
            "DEMO DATA: Fictional full-boarding ICSE academy emphasising pastoral care, "
            "outdoor education, and balanced academics."
        ),
        "academic_info": "ICSE/ISC with small class sizes and supervised evening prep.",
        "sports_info": "Horse riding, trekking clubs, football, and tennis.",
        "transport_info": "Airport and railway pickup for boarding students on session open/close.",
        "hostel_info": "Full residential programme with house system and resident tutors.",
        "admission_process": "Registration → written test → interview → medical clearance → fee payment.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Swimming Pool",
            "Hostel",
            "Auditorium",
            "Cafeteria",
            "Medical Room",
        ],
        "fees": [
            _fee_row("Class 4–8", 40000, 180000, 220000, 0, 25000),
            _fee_row("Class 9–12", 45000, 210000, 240000, 0, 30000),
        ],
        "infrastructure": [
            ("Campus", "Wooded residential campus with house dormitories (demo)."),
            ("Hostel", "Twin-sharing rooms with study desks and common lounges."),
            ("Outdoor", "Adventure course and nature trails."),
        ],
        "images": [(_img(301), "Boarding house (demo)"), (_img(302), "Library (demo)")],
    },
    {
        "name": "Narmada River Day School",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "board": "CBSE",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 4.2,
        "min_fee": 65000,
        "max_fee": 140000,
        "address": "SG Highway, Near Science City",
        "phone": "+91-79-40004004",
        "email": "info@narmadaday.demo",
        "website": "https://narmadaday.demo",
        "description": "DEMO DATA: Affordable fictional CBSE day school with strong value education focus.",
        "academic_info": "CBSE with remedial support and competitive exam awareness sessions.",
        "sports_info": "Kabaddi, kho-kho, cricket, and yoga.",
        "transport_info": "City-wide bus network with GPS-tracked fleet.",
        "hostel_info": "Not applicable.",
        "admission_process": "Walk-in counselling → documents → interaction → admission confirmation.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Transportation",
            "Playground",
            "Cafeteria",
            "Medical Room",
        ],
        "fees": [
            _fee_row("Class 1–5", 15000, 45000, 0, 12000, 5000),
            _fee_row("Class 6–10", 18000, 70000, 0, 14000, 7000),
        ],
        "infrastructure": [
            ("Campus", "Compact urban campus with multipurpose hall (demo)."),
            ("Safety", "ID-card entry and parent app updates."),
        ],
        "images": [(_img(401), "Classroom block (demo)")],
    },
    {
        "name": "Coastal Beacon International",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "board": "IB",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 4.5,
        "min_fee": 300000,
        "max_fee": 480000,
        "address": "OMR, Sholinganallur",
        "phone": "+91-44-40005005",
        "email": "admissions@coastalbeacon.demo",
        "website": "https://coastalbeacon.demo",
        "description": "DEMO DATA: Fictional coastal IB school known for arts and design studios.",
        "academic_info": "IB continuum with strong visual arts and design technology offerings.",
        "sports_info": "Swimming, tennis, basketball, and sailing club tie-ups.",
        "transport_info": "AC coaches along OMR, ECR, and central Chennai corridors.",
        "hostel_info": "Day school — no hostel.",
        "admission_process": "Online form → portfolio/assessment → family interview → offer.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Swimming Pool",
            "Transportation",
            "Auditorium",
            "Smart Classrooms",
        ],
        "fees": [
            _fee_row("PYP", 60000, 250000, 0, 40000, 20000),
            _fee_row("MYP / DP", 70000, 320000, 0, 40000, 25000),
        ],
        "infrastructure": [
            ("Arts", "Dedicated design and performing arts wing (demo)."),
            ("Campus", "Eco-friendly buildings with rainwater harvesting."),
        ],
        "images": [(_img(501), "Arts wing (demo)"), (_img(502), "Pool (demo)")],
    },
    {
        "name": "Deccan Heights Senior Secondary",
        "city": "Hyderabad",
        "state": "Telangana",
        "board": "CBSE",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 4.3,
        "min_fee": 90000,
        "max_fee": 180000,
        "address": "Gachibowli Financial District Road",
        "phone": "+91-40-40006006",
        "email": "contact@deccanheights.demo",
        "website": "https://deccanheights.demo",
        "description": "DEMO DATA: Fictional CBSE senior secondary with strong pre-university coaching tie-ins.",
        "academic_info": "CBSE Classes 1–12 with integrated foundation programmes for Classes 9–12.",
        "sports_info": "Indoor sports arena and athletic coaching.",
        "transport_info": "Routes covering Gachibowli, Madhapur, Kondapur, and Jubilee Hills.",
        "hostel_info": "Not available.",
        "admission_process": "Registration → aptitude test → counselling → fee payment.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Transportation",
            "Smart Classrooms",
            "Auditorium",
            "Cafeteria",
        ],
        "fees": [
            _fee_row("Class 1–8", 20000, 70000, 0, 18000, 8000),
            _fee_row("Class 9–12", 25000, 110000, 0, 20000, 12000),
        ],
        "infrastructure": [
            ("Labs", "Separate physics, chemistry, biology, and computer labs."),
            ("Campus", "High-rise academic tower with rooftop sports court (demo)."),
        ],
        "images": [(_img(601), "Academic block (demo)")],
    },
    {
        "name": "Garden City Girls' School",
        "city": "Bengaluru",
        "state": "Karnataka",
        "board": "ICSE",
        "school_type": "Day School",
        "gender": "Girls",
        "hostel_available": False,
        "rating": 4.5,
        "min_fee": 150000,
        "max_fee": 260000,
        "address": "Indiranagar 100 Feet Road",
        "phone": "+91-80-40007007",
        "email": "office@gardencitygirls.demo",
        "website": "https://gardencitygirls.demo",
        "description": "DEMO DATA: Fictional ICSE girls' day school with leadership and STEM emphasis.",
        "academic_info": "ICSE/ISC with coding, robotics, and debate as core co-scholastic tracks.",
        "sports_info": "Basketball, badminton, athletics, and swimming.",
        "transport_info": "East and south Bengaluru routes.",
        "hostel_info": "Day school only.",
        "admission_process": "Enquiry → interaction → assessment → provisional admission.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Swimming Pool",
            "Transportation",
            "Auditorium",
            "Smart Classrooms",
            "Medical Room",
        ],
        "fees": [
            _fee_row("Class 1–5", 30000, 110000, 0, 25000, 10000),
            _fee_row("Class 6–10", 35000, 150000, 0, 25000, 15000),
        ],
        "infrastructure": [
            ("Campus", "Urban campus with amphitheatre garden (demo)."),
            ("STEM", "Innovation lab and makerspace for girls in STEM."),
        ],
        "images": [(_img(701), "Main building (demo)"), (_img(702), "Lab (demo)")],
    },
    {
        "name": "Northern Ridge Boys' Academy",
        "city": "Delhi",
        "state": "Delhi",
        "board": "CBSE",
        "school_type": "Day-Boarding",
        "gender": "Boys",
        "hostel_available": True,
        "rating": 4.1,
        "min_fee": 180000,
        "max_fee": 320000,
        "address": "Civil Lines / Ridge Road Area",
        "phone": "+91-11-40008008",
        "email": "admin@northernridge.demo",
        "website": "https://northernridge.demo",
        "description": "DEMO DATA: Fictional boys' academy with structured day-boarding and sports focus.",
        "academic_info": "CBSE with supervised prep hours and career counselling from Class 9.",
        "sports_info": "Football, cricket, boxing, and athletics.",
        "transport_info": "North and central Delhi pick-up points.",
        "hostel_info": "Weekly boarding option for senior classes.",
        "admission_process": "Form → entrance exam → sports trial (optional) → interview.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Hostel",
            "Transportation",
            "Playground",
            "Cafeteria",
            "Medical Room",
        ],
        "fees": [
            _fee_row("Class 4–8", 35000, 120000, 60000, 22000, 12000),
            _fee_row("Class 9–12", 40000, 150000, 80000, 25000, 15000),
        ],
        "infrastructure": [
            ("Sports", "Full-size football ground and indoor gym (demo)."),
            ("Boarding", "Senior weekly boarding dormitory."),
        ],
        "images": [(_img(801), "Sports ground (demo)")],
    },
    {
        "name": "Konkan Heritage Vidyalaya",
        "city": "Mumbai",
        "state": "Maharashtra",
        "board": "State",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 3.9,
        "min_fee": 35000,
        "max_fee": 85000,
        "address": "Thane West, Ghodbunder Road",
        "phone": "+91-22-40009009",
        "email": "info@konkanheritage.demo",
        "website": "https://konkanheritage.demo",
        "description": "DEMO DATA: Fictional Maharashtra State Board school with Marathi and English mediums.",
        "academic_info": "State board curriculum with language labs and cultural programmes.",
        "sports_info": "Kabaddi, volleyball, and athletics.",
        "transport_info": "Thane–Mira Road corridor buses.",
        "hostel_info": "Not available.",
        "admission_process": "Document verification → seat allotment based on availability.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Transportation",
            "Playground",
            "Cafeteria",
        ],
        "fees": [
            _fee_row("Class 1–5", 8000, 25000, 0, 8000, 3000),
            _fee_row("Class 6–10", 10000, 40000, 0, 10000, 5000),
        ],
        "infrastructure": [
            ("Campus", "Neighbourhood campus with multipurpose court (demo)."),
            ("Culture", "Dedicated hall for performing arts and festivals."),
        ],
        "images": [(_img(901), "School entrance (demo)")],
    },
    {
        "name": "Lakeside Multinational School",
        "city": "Bengaluru",
        "state": "Karnataka",
        "board": "IB",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 4.8,
        "min_fee": 400000,
        "max_fee": 650000,
        "address": "Whitefield–Sarjapur Road",
        "phone": "+91-80-40001010",
        "email": "enrol@lakesidemulti.demo",
        "website": "https://lakesidemulti.demo",
        "description": "DEMO DATA: Premium fictional IB school for globally mobile families.",
        "academic_info": "Full IB continuum with extensive university counselling.",
        "sports_info": "Olympic-size pool, tennis courts, and fitness centre.",
        "transport_info": "Premium AC fleet across east Bengaluru.",
        "hostel_info": "Day school — residential not offered.",
        "admission_process": "Rolling admissions → assessment day → offer within 10 working days (demo).",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Swimming Pool",
            "Transportation",
            "Auditorium",
            "Smart Classrooms",
            "Cafeteria",
            "Medical Room",
        ],
        "fees": [
            _fee_row("Early Years / PYP", 80000, 350000, 0, 50000, 30000),
            _fee_row("MYP / DP", 90000, 450000, 0, 50000, 40000),
        ],
        "infrastructure": [
            ("Campus", "Lakeside landscaped campus with STEAM centre (demo)."),
            ("Technology", "1:1 device programme for middle and senior years."),
        ],
        "images": [(_img(1001), "Lake campus (demo)"), (_img(1002), "STEAM centre (demo)")],
    },
    {
        "name": "Aravali Desert Bloom School",
        "city": "Jaipur",
        "state": "Rajasthan",
        "board": "CBSE",
        "school_type": "Boarding",
        "gender": "Co-ed",
        "hostel_available": True,
        "rating": 4.0,
        "min_fee": 220000,
        "max_fee": 380000,
        "address": "Ajmer Road, outskirts",
        "phone": "+91-141-40001111",
        "email": "admissions@desertbloom.demo",
        "website": "https://desertbloom.demo",
        "description": "DEMO DATA: Fictional CBSE boarding school with heritage and outdoor learning themes.",
        "academic_info": "CBSE with environmental studies and leadership camps.",
        "sports_info": "Horse riding, cricket, athletics, and archery.",
        "transport_info": "Seasonal city transfers for boarding families.",
        "hostel_info": "Full boarding with house parents and weekend activities.",
        "admission_process": "Prospectus → entrance test → medical → confirmation deposit.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Hostel",
            "Auditorium",
            "Cafeteria",
            "Medical Room",
            "Playground",
        ],
        "fees": [
            _fee_row("Class 4–8", 30000, 100000, 140000, 0, 15000),
            _fee_row("Class 9–12", 35000, 130000, 160000, 0, 20000),
        ],
        "infrastructure": [
            ("Campus", "Semi-arid landscaped boarding campus (demo)."),
            ("Hostel", "Cottage-style dormitories with study halls."),
        ],
        "images": [(_img(1101), "Hostel cottage (demo)")],
    },
    {
        "name": "Marine Drive Progressive School",
        "city": "Mumbai",
        "state": "Maharashtra",
        "board": "ICSE",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 4.4,
        "min_fee": 200000,
        "max_fee": 340000,
        "address": "Near Marine Drive, South Mumbai",
        "phone": "+91-22-40001212",
        "email": "hello@marineprogressive.demo",
        "website": "https://marineprogressive.demo",
        "description": "DEMO DATA: Fictional ICSE day school with strong performing arts and languages.",
        "academic_info": "ICSE/ISC with French/Spanish electives and theatre integration.",
        "sports_info": "Swimming partnerships, table tennis, and basketball.",
        "transport_info": "Limited south Mumbai shuttle service.",
        "hostel_info": "Not available.",
        "admission_process": "Online registration → interaction → assessment → waitlist/offer.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Swimming Pool",
            "Auditorium",
            "Smart Classrooms",
            "Transportation",
            "Medical Room",
        ],
        "fees": [
            _fee_row("Class 1–5", 40000, 160000, 0, 20000, 15000),
            _fee_row("Class 6–10", 45000, 210000, 0, 22000, 20000),
        ],
        "infrastructure": [
            ("Campus", "Heritage-inspired urban campus (demo)."),
            ("Arts", "Black-box theatre and music practice rooms."),
        ],
        "images": [(_img(1201), "Arts foyer (demo)"), (_img(1202), "Classroom (demo)")],
    },
    {
        "name": "Silicon Springs Academy",
        "city": "Pune",
        "state": "Maharashtra",
        "board": "CBSE",
        "school_type": "Day School",
        "gender": "Co-ed",
        "hostel_available": False,
        "rating": 4.2,
        "min_fee": 110000,
        "max_fee": 210000,
        "address": "Hinjewadi Phase 2",
        "phone": "+91-20-40001313",
        "email": "connect@siliconsprings.demo",
        "website": "https://siliconsprings.demo",
        "description": "DEMO DATA: Fictional tech-corridor CBSE school popular with IT-park families.",
        "academic_info": "CBSE with coding from primary and AI awareness modules in senior school.",
        "sports_info": "Indoor sports complex and weekend football leagues.",
        "transport_info": "Hinjewadi, Wakad, and Baner corporate-park routes.",
        "hostel_info": "Day school only.",
        "admission_process": "Digital application → virtual tour → on-campus assessment → offer.",
        "facilities": [
            "Library",
            "Computer Lab",
            "Science Lab",
            "Sports Complex",
            "Transportation",
            "Smart Classrooms",
            "Cafeteria",
            "Playground",
        ],
        "fees": [
            _fee_row("Class 1–5", 22000, 85000, 0, 18000, 8000),
            _fee_row("Class 6–10", 28000, 120000, 0, 20000, 12000),
        ],
        "infrastructure": [
            ("Technology", "High-speed campus network and coding labs (demo)."),
            ("Campus", "Modern glass-front academic blocks."),
        ],
        "images": [(_img(1301), "Tech lab (demo)")],
    },
]


def _clear_demo_data():
    """Remove existing seeded rows so seed is idempotent for local resets."""
    # Order matters due to FKs — children first
    db.session.query(AdmissionEnquiry).delete()
    db.session.query(Shortlist).delete()
    db.session.query(SchoolFacility).delete()
    db.session.query(SchoolFee).delete()
    db.session.query(SchoolImage).delete()
    db.session.query(Infrastructure).delete()
    db.session.query(School).delete()
    db.session.query(Facility).delete()
    db.session.query(User).delete()
    db.session.commit()


def _seed_facilities():
    facilities = {}
    for name, description in FACILITY_DEFS:
        facility = Facility(name=name, description=description)
        db.session.add(facility)
        facilities[name] = facility
    db.session.flush()
    return facilities


def _seed_users():
    admin = User(
        name="BoardingEdu Admin",
        email=Config.DEMO_ADMIN_EMAIL,
        phone="+91-9000000001",
        role="admin",
        password_hash=generate_password_hash(Config.DEMO_ADMIN_PASSWORD),
    )
    parent = User(
        name="Demo Parent",
        email=Config.DEMO_PARENT_EMAIL,
        phone="+91-9000000002",
        role="parent",
        password_hash=generate_password_hash(Config.DEMO_PARENT_PASSWORD),
    )
    db.session.add_all([admin, parent])
    db.session.flush()
    return admin, parent


def _seed_schools(facilities_by_name):
    schools = []
    for data in SCHOOL_DEFS:
        school = School(
            name=data["name"],
            description=data["description"],
            address=data["address"],
            city=data["city"],
            state=data["state"],
            board=data["board"],
            school_type=data["school_type"],
            gender=data["gender"],
            min_fee=data["min_fee"],
            max_fee=data["max_fee"],
            hostel_available=data["hostel_available"],
            rating=data["rating"],
            phone=data["phone"],
            email=data["email"],
            website=data["website"],
            admission_process=data["admission_process"],
            academic_info=data["academic_info"],
            sports_info=data["sports_info"],
            transport_info=data["transport_info"],
            hostel_info=data["hostel_info"],
        )
        db.session.add(school)
        db.session.flush()

        for fee in data["fees"]:
            db.session.add(SchoolFee(school_id=school.id, **fee))

        for category, description in data["infrastructure"]:
            db.session.add(
                Infrastructure(
                    school_id=school.id,
                    category=category,
                    description=description,
                )
            )

        for url, caption in data["images"]:
            db.session.add(
                SchoolImage(school_id=school.id, image_url=url, caption=caption)
            )

        for facility_name in data["facilities"]:
            facility = facilities_by_name.get(facility_name)
            if facility:
                db.session.add(
                    SchoolFacility(school_id=school.id, facility_id=facility.id)
                )

        schools.append(school)

    db.session.flush()
    return schools


def _seed_sample_parent_activity(parent, schools):
    """Optional sample shortlist + enquiry so dashboards are not empty."""
    if len(schools) < 2:
        return

    db.session.add(Shortlist(user_id=parent.id, school_id=schools[0].id))
    db.session.add(Shortlist(user_id=parent.id, school_id=schools[1].id))
    db.session.add(
        AdmissionEnquiry(
            user_id=parent.id,
            school_id=schools[0].id,
            student_name="Aarav Sharma",
            parent_name=parent.name,
            class_name="Class 5",
            academic_year="2026-27",
            phone=parent.phone,
            email=parent.email,
            message="DEMO: Interested in a campus visit and fee counselling.",
            status="Pending",
        )
    )


def seed(reset: bool = True):
    app = create_app()
    with app.app_context():
        print("Creating tables (if not present)...")
        db.create_all()

        if reset:
            print("Clearing existing data for a clean demo seed...")
            _clear_demo_data()

        print("Seeding facilities...")
        facilities = _seed_facilities()

        print("Seeding demo users...")
        _admin, parent = _seed_users()

        print(f"Seeding {len(SCHOOL_DEFS)} fictional schools...")
        schools = _seed_schools(facilities)

        print("Seeding sample parent shortlist & enquiry...")
        _seed_sample_parent_activity(parent, schools)

        db.session.commit()

        print("\nSeed completed successfully.")
        print(f"  Facilities : {Facility.query.count()}")
        print(f"  Schools    : {School.query.count()}")
        print(f"  Users      : {User.query.count()}")
        print(f"  Shortlists : {Shortlist.query.count()}")
        print(f"  Enquiries  : {AdmissionEnquiry.query.count()}")
        print("\nDemo accounts (from environment / defaults):")
        print(f"  Admin  : {Config.DEMO_ADMIN_EMAIL}")
        print(f"  Parent : {Config.DEMO_PARENT_EMAIL}")
        print("  Passwords are set via DEMO_ADMIN_PASSWORD / DEMO_PARENT_PASSWORD in .env")
        print("  (See backend/.env.example — do not commit real credentials.)")


if __name__ == "__main__":
    do_reset = "--no-reset" not in sys.argv
    seed(reset=do_reset)
