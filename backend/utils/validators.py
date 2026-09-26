"""Input validation helpers for auth and school APIs."""

import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^[+\d][\d\s\-()]{7,19}$")

PUBLIC_ROLES = {"parent", "student"}
ALL_ROLES = {"parent", "student", "admin"}

VALID_BOARDS = {"CBSE", "ICSE", "IB", "State", "Cambridge", "Other"}
VALID_SCHOOL_TYPES = {"Day School", "Boarding", "Day-Boarding"}
VALID_GENDERS = {"Co-ed", "Boys", "Girls"}


def _clean(value):
    if value is None:
        return ""
    return str(value).strip()


def _optional_int(value, field, errors, minimum=0):
    if value is None or value == "":
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        errors[field] = f"{field} must be an integer."
        return None
    if number < minimum:
        errors[field] = f"{field} must be >= {minimum}."
        return None
    return number


def _optional_float(value, field, errors, minimum=0.0, maximum=5.0):
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        errors[field] = f"{field} must be a number."
        return None
    if number < minimum or number > maximum:
        errors[field] = f"{field} must be between {minimum} and {maximum}."
        return None
    return number


def validate_register_payload(data):
    """
    Validate public registration body.
    Returns (cleaned_dict, error_dict). error_dict empty means valid.
    """
    data = data or {}
    errors = {}

    name = _clean(data.get("name"))
    email = _clean(data.get("email")).lower()
    phone = _clean(data.get("phone"))
    password = data.get("password") if data.get("password") is not None else ""
    role = _clean(data.get("role")).lower() or "parent"

    if not name or len(name) < 2:
        errors["name"] = "Name must be at least 2 characters."
    elif len(name) > 120:
        errors["name"] = "Name must be at most 120 characters."

    if not email:
        errors["email"] = "Email is required."
    elif not EMAIL_RE.match(email):
        errors["email"] = "Enter a valid email address."
    elif len(email) > 255:
        errors["email"] = "Email is too long."

    if phone and not PHONE_RE.match(phone):
        errors["phone"] = "Enter a valid phone number."

    if not isinstance(password, str) or len(password) < 8:
        errors["password"] = "Password must be at least 8 characters."
    elif len(password) > 128:
        errors["password"] = "Password must be at most 128 characters."

    if role not in PUBLIC_ROLES:
        errors["role"] = "Public registration allows only 'parent' or 'student' roles."

    cleaned = {
        "name": name,
        "email": email,
        "phone": phone or None,
        "password": password,
        "role": role,
    }
    return cleaned, errors


def validate_login_payload(data):
    """Validate login body. Returns (cleaned_dict, error_dict)."""
    data = data or {}
    errors = {}

    email = _clean(data.get("email")).lower()
    password = data.get("password") if data.get("password") is not None else ""

    if not email:
        errors["email"] = "Email is required."
    elif not EMAIL_RE.match(email):
        errors["email"] = "Enter a valid email address."

    if not password:
        errors["password"] = "Password is required."

    return {"email": email, "password": password}, errors


def validate_school_payload(data, partial=False):
    """
    Validate school create/update body.
    partial=True allows missing fields (PUT updates).
    """
    data = data or {}
    errors = {}

    def require_or_keep(field):
        if field in data:
            return True
        return not partial

    name = _clean(data.get("name")) if "name" in data or not partial else None
    city = _clean(data.get("city")) if "city" in data or not partial else None

    cleaned = {}

    if require_or_keep("name"):
        if not name or len(name) < 2:
            errors["name"] = "School name must be at least 2 characters."
        elif len(name) > 200:
            errors["name"] = "School name must be at most 200 characters."
        else:
            cleaned["name"] = name

    if require_or_keep("city"):
        if not city:
            errors["city"] = "City is required."
        elif len(city) > 100:
            errors["city"] = "City must be at most 100 characters."
        else:
            cleaned["city"] = city

    string_fields = {
        "description": 10000,
        "address": 500,
        "state": 100,
        "phone": 20,
        "email": 255,
        "website": 255,
        "admission_process": 10000,
        "academic_info": 10000,
        "sports_info": 10000,
        "transport_info": 10000,
        "hostel_info": 10000,
    }
    for field, max_len in string_fields.items():
        if field not in data and partial:
            continue
        value = _clean(data.get(field)) if data.get(field) is not None else ""
        if field == "email" and value and not EMAIL_RE.match(value):
            errors["email"] = "Enter a valid school email address."
            continue
        if field == "phone" and value and not PHONE_RE.match(value):
            errors["phone"] = "Enter a valid school phone number."
            continue
        if len(value) > max_len:
            errors[field] = f"{field} is too long."
            continue
        cleaned[field] = value or None

    if "board" in data or not partial:
        board = _clean(data.get("board"))
        if board and board not in VALID_BOARDS:
            errors["board"] = (
                f"board must be one of: {', '.join(sorted(VALID_BOARDS))}."
            )
        else:
            cleaned["board"] = board or None

    if "school_type" in data or not partial:
        school_type = _clean(data.get("school_type"))
        if school_type and school_type not in VALID_SCHOOL_TYPES:
            errors["school_type"] = (
                f"school_type must be one of: {', '.join(sorted(VALID_SCHOOL_TYPES))}."
            )
        else:
            cleaned["school_type"] = school_type or None

    if "gender" in data or not partial:
        gender = _clean(data.get("gender"))
        if gender and gender not in VALID_GENDERS:
            errors["gender"] = (
                f"gender must be one of: {', '.join(sorted(VALID_GENDERS))}."
            )
        else:
            cleaned["gender"] = gender or None

    if "min_fee" in data or not partial:
        cleaned["min_fee"] = _optional_int(data.get("min_fee"), "min_fee", errors)

    if "max_fee" in data or not partial:
        cleaned["max_fee"] = _optional_int(data.get("max_fee"), "max_fee", errors)

    if (
        cleaned.get("min_fee") is not None
        and cleaned.get("max_fee") is not None
        and cleaned["min_fee"] > cleaned["max_fee"]
    ):
        errors["max_fee"] = "max_fee must be greater than or equal to min_fee."

    if "hostel_available" in data or not partial:
        hostel = data.get("hostel_available", False)
        if isinstance(hostel, str):
            hostel = hostel.strip().lower() in {"1", "true", "yes"}
        cleaned["hostel_available"] = bool(hostel)

    if "rating" in data or not partial:
        rating = _optional_float(data.get("rating"), "rating", errors)
        cleaned["rating"] = 4.0 if rating is None and not partial else rating

    if "facility_ids" in data:
        facility_ids = data.get("facility_ids") or []
        if not isinstance(facility_ids, list):
            errors["facility_ids"] = "facility_ids must be a list of integers."
        else:
            cleaned_ids = []
            for item in facility_ids:
                try:
                    cleaned_ids.append(int(item))
                except (TypeError, ValueError):
                    errors["facility_ids"] = "facility_ids must contain integers only."
                    break
            else:
                cleaned["facility_ids"] = cleaned_ids

    if "fees" in data:
        fees, fee_errors = _validate_fees_list(data.get("fees"))
        if fee_errors:
            errors["fees"] = fee_errors
        else:
            cleaned["fees"] = fees

    if "images" in data:
        images, image_errors = _validate_images_list(data.get("images"))
        if image_errors:
            errors["images"] = image_errors
        else:
            cleaned["images"] = images

    if "infrastructure" in data:
        infra, infra_errors = _validate_infrastructure_list(data.get("infrastructure"))
        if infra_errors:
            errors["infrastructure"] = infra_errors
        else:
            cleaned["infrastructure"] = infra

    return cleaned, errors


def _validate_fees_list(fees):
    if fees is None:
        return [], None
    if not isinstance(fees, list):
        return None, "fees must be a list."
    cleaned = []
    for index, row in enumerate(fees):
        if not isinstance(row, dict):
            return None, f"fees[{index}] must be an object."
        class_name = _clean(row.get("class_name"))
        if not class_name:
            return None, f"fees[{index}].class_name is required."
        entry = {"class_name": class_name}
        for field in (
            "admission_fee",
            "tuition_fee",
            "hostel_fee",
            "transport_fee",
            "other_fee",
            "annual_fee",
        ):
            local_errors = {}
            value = _optional_int(row.get(field, 0), field, local_errors)
            if local_errors:
                return None, f"fees[{index}].{field} must be a non-negative integer."
            entry[field] = value or 0
        if not entry["annual_fee"]:
            entry["annual_fee"] = (
                entry["admission_fee"]
                + entry["tuition_fee"]
                + entry["hostel_fee"]
                + entry["transport_fee"]
                + entry["other_fee"]
            )
        cleaned.append(entry)
    return cleaned, None


def _validate_images_list(images):
    if images is None:
        return [], None
    if not isinstance(images, list):
        return None, "images must be a list."
    cleaned = []
    for index, row in enumerate(images):
        if not isinstance(row, dict):
            return None, f"images[{index}] must be an object."
        url = _clean(row.get("image_url"))
        if not url:
            return None, f"images[{index}].image_url is required."
        cleaned.append(
            {
                "image_url": url[:500],
                "caption": (_clean(row.get("caption")) or None),
            }
        )
    return cleaned, None


def _validate_infrastructure_list(items):
    if items is None:
        return [], None
    if not isinstance(items, list):
        return None, "infrastructure must be a list."
    cleaned = []
    for index, row in enumerate(items):
        if not isinstance(row, dict):
            return None, f"infrastructure[{index}] must be an object."
        category = _clean(row.get("category"))
        if not category:
            return None, f"infrastructure[{index}].category is required."
        cleaned.append(
            {
                "category": category[:100],
                "description": _clean(row.get("description")) or None,
            }
        )
    return cleaned, None


def validate_enquiry_payload(data):
    """Validate admission enquiry create body."""
    data = data or {}
    errors = {}

    try:
        school_id = int(data.get("school_id"))
    except (TypeError, ValueError):
        school_id = None
        errors["school_id"] = "school_id is required and must be an integer."

    student_name = _clean(data.get("student_name"))
    parent_name = _clean(data.get("parent_name"))
    class_name = _clean(data.get("class_name"))
    academic_year = _clean(data.get("academic_year"))
    phone = _clean(data.get("phone"))
    email = _clean(data.get("email")).lower()
    message = _clean(data.get("message"))

    if not student_name or len(student_name) < 2:
        errors["student_name"] = "Student name must be at least 2 characters."
    if not parent_name or len(parent_name) < 2:
        errors["parent_name"] = "Parent name must be at least 2 characters."
    if phone and not PHONE_RE.match(phone):
        errors["phone"] = "Enter a valid phone number."
    if email and not EMAIL_RE.match(email):
        errors["email"] = "Enter a valid email address."

    cleaned = {
        "school_id": school_id,
        "student_name": student_name,
        "parent_name": parent_name,
        "class_name": class_name or None,
        "academic_year": academic_year or None,
        "phone": phone or None,
        "email": email or None,
        "message": message or None,
    }
    return cleaned, errors
