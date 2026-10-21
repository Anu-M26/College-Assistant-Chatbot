"""
College Assistant
Flask Backend
College JSON Database
Separate Pages
Chatbot + Chat History
"""

import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from data.chat_db import (
    get_chat_history,
    init_database,
    save_chat
)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
COLLEGE_DATA_PATH = DATA_DIR / "college_data.json"


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# LOAD COLLEGE DATA
# =========================================================

def load_college_data():

    try:
        with open(
            COLLEGE_DATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        print("College data loaded successfully.")
        return data

    except FileNotFoundError:

        print(
            f"ERROR: college_data.json not found at "
            f"{COLLEGE_DATA_PATH}"
        )

        return {}

    except json.JSONDecodeError as error:

        print(
            f"ERROR: Invalid JSON - {error}"
        )

        return {}

    except Exception as error:

        print(
            f"ERROR loading college data - {error}"
        )

        return {}


COLLEGE_DATA = load_college_data()


# =========================================================
# CONSTANTS
# =========================================================

COLLEGE_NOT_FOUND_MESSAGE = (
    "Sorry, I don't have this information. "
    "Please contact the college administration."
)


COLLEGE_KEYWORDS = (
    "college",
    "campus",
    "course",
    "courses",
    "department",
    "departments",
    "admission",
    "eligibility",
    "entrance",
    "fee",
    "fees",
    "tuition",
    "facility",
    "facilities",
    "placement",
    "placements",
    "package",
    "company",
    "companies",
    "attendance",
    "attend",
    "library",
    "book",
    "books",
    "hostel",
    "transport",
    "exam",
    "event",
    "events",
    "sports",
    "contact",
    "email",
    "phone",
    "working",
    "hours",
    "timing",
    "lab",
    "computer",
    "hod",
    "head"
)


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(value):

    return " ".join(
        str(value)
        .lower()
        .replace("-", " ")
        .split()
    )


# =========================================================
# CHATBOT ANSWER
# =========================================================

def answer_college_question(question):

    if not question:
        return COLLEGE_NOT_FOUND_MESSAGE

    normalized_question = normalize_text(question)

    # -----------------------------------------------------
    # COLLEGE RELATED CHECK
    # -----------------------------------------------------

    is_college_related = any(
        keyword in normalized_question
        for keyword in COLLEGE_KEYWORDS
    )

    if not is_college_related:

        return (
            "I can only help with college-related questions. "
            "Please ask me about courses, admission, fees, "
            "facilities, placements, attendance, library, "
            "or other college information."
        )

    if not COLLEGE_DATA:
        return COLLEGE_NOT_FOUND_MESSAGE


    # =====================================================
    # COLLEGE NAME
    # =====================================================

    if (
        "college name" in normalized_question
        or (
            "name" in normalized_question
            and "college" in normalized_question
        )
    ):

        value = COLLEGE_DATA.get("college_name")

        if value:
            return str(value)


    # =====================================================
    # LOCATION
    # =====================================================

    if (
        "location" in normalized_question
        or "located" in normalized_question
        or "where is" in normalized_question
    ):

        value = COLLEGE_DATA.get("college_location")

        if value:
            return f"The college is located in {value}."


    # =====================================================
    # FOUNDED
    # =====================================================

    if (
        "founded" in normalized_question
        or "established" in normalized_question
        or "started" in normalized_question
    ):

        value = COLLEGE_DATA.get("college_founded")

        if value:
            return f"The college was founded in {value}."


    # =====================================================
    # EMAIL
    # =====================================================

    if "email" in normalized_question:

        value = COLLEGE_DATA.get("contact_email")

        if value:
            return f"The college email is {value}."


    # =====================================================
    # PHONE
    # =====================================================

    if (
        "phone" in normalized_question
        or "contact number" in normalized_question
        or "phone number" in normalized_question
    ):

        value = COLLEGE_DATA.get("contact_phone")

        if value:
            return f"The college contact number is {value}."


    # =====================================================
    # ADMISSION
    # =====================================================

    if (
        "admission" in normalized_question
        or "eligibility" in normalized_question
        or "entrance" in normalized_question
    ):

        admission = COLLEGE_DATA.get(
            "admission",
            {}
        )

        if "eligibility" in normalized_question:

            value = admission.get("eligibility")

            if value:
                return f"Admission eligibility: {value}."


        if "entrance" in normalized_question:

            value = admission.get("entrance_exam")

            if value:
                return f"The entrance exam is {value}."


        if (
            "deadline" in normalized_question
            or "last date" in normalized_question
        ):

            value = admission.get(
                "application_deadline"
            )

            if value:
                return (
                    f"The application deadline is {value}."
                )


        if (
            "application fee" in normalized_question
            or "application fees" in normalized_question
        ):

            value = admission.get("application_fee")

            if value is not None:
                return (
                    f"The application fee is ₹{value:,}."
                )


        if (
            "document" in normalized_question
            or "documents" in normalized_question
        ):

            documents = admission.get(
                "required_documents",
                []
            )

            if documents:

                return (
                    "Required documents:\n"
                    + "\n".join(
                        f"• {document}"
                        for document in documents
                    )
                )


        if (
            "process" in normalized_question
            or "procedure" in normalized_question
        ):

            process = admission.get(
                "admission_process",
                []
            )

            if process:

                return (
                    "Admission process:\n"
                    + "\n".join(
                        f"{index + 1}. {step}"
                        for index, step
                        in enumerate(process)
                    )
                )


        if admission:

            return (
                f"Admission eligibility: "
                f"{admission.get('eligibility', 'Not available')}.\n"
                f"Entrance exam: "
                f"{admission.get('entrance_exam', 'Not available')}.\n"
                f"Application deadline: "
                f"{admission.get('application_deadline', 'Not available')}."
            )


    # =====================================================
    # COURSES / DEPARTMENTS
    # =====================================================

    if (
        "department" in normalized_question
        or "course" in normalized_question
    ):

        departments = COLLEGE_DATA.get(
            "departments",
            []
        )

        # Specific department

        for department in departments:

            department_name = str(
                department.get("name", "")
            )

            normalized_department = normalize_text(
                department_name
            )

            department_words = [
                word
                for word in normalized_department.split()
                if len(word) > 2
            ]

            if (
                normalized_department in normalized_question
                or any(
                    word in normalized_question
                    for word in department_words
                )
            ):

                courses = department.get(
                    "courses",
                    []
                )

                head = department.get("head")

                if (
                    "head" in normalized_question
                    or "hod" in normalized_question
                ):

                    if head:
                        return (
                            f"The Head of the "
                            f"{department_name} department "
                            f"is {head}."
                        )

                if courses:

                    return (
                        f"The {department_name} department "
                        f"offers: "
                        f"{', '.join(courses)}."
                    )


        # All departments

        if departments:

            department_names = ", ".join(
                department.get("name", "")
                for department in departments
            )

            return (
                "The college has the following departments: "
                f"{department_names}."
            )


    # =====================================================
    # FEES
    # =====================================================

    if (
        "fee" in normalized_question
        or "fees" in normalized_question
    ):

        fees = COLLEGE_DATA.get(
            "fees",
            {}
        )


        # Course fees

        if (
            "course" in normalized_question
            or "tuition" in normalized_question
        ):

            course_fees = fees.get(
                "course_fees",
                {}
            )

            result = []

            for course, amount in course_fees.items():

                if course in (
                    "currency",
                    "period"
                ):
                    continue

                if isinstance(
                    amount,
                    (int, float)
                ):

                    result.append(
                        f"{course}: ₹{amount:,}"
                    )

            if result:

                return (
                    "Course fees:\n"
                    + "\n".join(result)
                    + f"\nFee period: "
                    f"{course_fees.get('period', 'Not available')}"
                )


        # Hostel fees

        if "hostel" in normalized_question:

            hostel_fees = fees.get(
                "hostel_fees",
                {}
            )

            boys = hostel_fees.get(
                "boys_hostel"
            )

            girls = hostel_fees.get(
                "girls_hostel"
            )

            period = hostel_fees.get(
                "period",
                ""
            )

            if (
                boys is not None
                and girls is not None
            ):

                return (
                    f"Boys hostel fee: ₹{boys:,}\n"
                    f"Girls hostel fee: ₹{girls:,}\n"
                    f"Fee period: {period}"
                )


        # Exam fees

        if "exam" in normalized_question:

            exam_fees = fees.get(
                "exam_fees",
                {}
            )

            regular = exam_fees.get(
                "regular_exam"
            )

            arrear = exam_fees.get(
                "arrear_exam"
            )

            if regular is not None:

                answer = (
                    f"Regular exam fee: ₹{regular:,}"
                )

                if arrear is not None:
                    answer += (
                        f"\nArrear exam fee: ₹{arrear:,}"
                    )

                return answer


        # Transport fees

        if "transport" in normalized_question:

            transport_fees = fees.get(
                "transport_fees",
                {}
            )

            result = []

            city = transport_fees.get(
                "coimbatore_city"
            )

            nearby = transport_fees.get(
                "nearby_routes"
            )

            long_distance = transport_fees.get(
                "long_distance_routes"
            )

            if city is not None:
                result.append(
                    f"Coimbatore city: ₹{city:,}"
                )

            if nearby is not None:
                result.append(
                    f"Nearby routes: ₹{nearby:,}"
                )

            if long_distance is not None:
                result.append(
                    f"Long distance routes: ₹{long_distance:,}"
                )

            if result:
                return "\n".join(result)


        # Library fee

        if "library" in normalized_question:

            value = fees.get(
                "library_fee_per_semester"
            )

            if value is not None:

                return (
                    f"The library fee per semester "
                    f"is ₹{value:,}."
                )


        # Lab fee

        if "lab" in normalized_question:

            value = fees.get(
                "lab_fee_per_semester"
            )

            if value is not None:

                return (
                    f"The lab fee per semester "
                    f"is ₹{value:,}."
                )


        if fees:

            return (
                "Available fee information includes "
                "course fees, hostel fees, exam fees, "
                "transport fees, library fees, and lab fees."
            )


    # =====================================================
    # LIBRARY
    # =====================================================

    if "library" in normalized_question:

        library = COLLEGE_DATA.get(
            "library",
            {}
        )

        if (
            "time" in normalized_question
            or "open" in normalized_question
            or "close" in normalized_question
        ):

            return (
                f"The library opens at "
                f"{library.get('opening_time')} "
                f"and closes at "
                f"{library.get('closing_time')}."
            )


        if (
            "book" in normalized_question
            or "books" in normalized_question
        ):

            total_books = library.get(
                "total_books"
            )

            if total_books is not None:

                return (
                    f"The library has "
                    f"{total_books:,} books."
                )


        if (
            "computer" in normalized_question
            or "wifi" in normalized_question
            or "wi fi" in normalized_question
        ):

            wifi = (
                "available"
                if library.get("wifi_available")
                else "not available"
            )

            return (
                f"The library has "
                f"{library.get('computers_available')} "
                f"computers available and Wi-Fi is {wifi}."
            )


        if library:

            return (
                f"Library timing: "
                f"{library.get('opening_time')} to "
                f"{library.get('closing_time')}.\n"
                f"Total books: "
                f"{library.get('total_books'):,}."
            )


    # =====================================================
    # FACILITIES
    # =====================================================

    if (
        "facility" in normalized_question
        or "facilities" in normalized_question
    ):

        facilities = COLLEGE_DATA.get(
            "campus_facilities",
            []
        )

        if facilities:

            return (
                "Campus facilities include:\n"
                + "\n".join(
                    f"• {facility}"
                    for facility in facilities
                )
            )


    # =====================================================
    # PLACEMENT
    # =====================================================

    if (
        "placement" in normalized_question
        or "package" in normalized_question
        or "company" in normalized_question
    ):

        placement = COLLEGE_DATA.get(
            "placement",
            {}
        )


        if (
            "average" in normalized_question
            or "package" in normalized_question
        ):

            value = placement.get(
                "average_package"
            )

            if value is not None:

                return (
                    f"The average placement package "
                    f"is ₹{value:,}."
                )


        if (
            "percentage" in normalized_question
            or "placed" in normalized_question
        ):

            value = placement.get(
                "placement_percentage"
            )

            if value is not None:

                return (
                    f"The placement percentage is "
                    f"{value}%."
                )


        placement_departments = placement.get(
            "departments",
            {}
        )

        for department_name, data in placement_departments.items():

            normalized_department = normalize_text(
                department_name
            )

            department_words = [
                word
                for word in normalized_department.split()
                if len(word) > 2
            ]

            if (
                normalized_department in normalized_question
                or any(
                    word in normalized_question
                    for word in department_words
                )
            ):

                companies = data.get(
                    "companies",
                    []
                )

                roles = data.get(
                    "job_roles",
                    []
                )

                answer = (
                    f"{department_name} placement details:\n"
                )

                if companies:
                    answer += (
                        "Companies: "
                        + ", ".join(companies)
                        + "\n"
                    )

                if roles:
                    answer += (
                        "Job roles: "
                        + ", ".join(roles)
                    )

                return answer


        if placement:

            return (
                f"Average package: "
                f"₹{placement.get('average_package', 0):,}\n"
                f"Placement percentage: "
                f"{placement.get('placement_percentage', 'N/A')}%"
            )


    # =====================================================
    # ATTENDANCE
    # =====================================================

    if (
        "attendance" in normalized_question
        or "attend" in normalized_question
    ):

        attendance = COLLEGE_DATA.get(
            "attendance",
            {}
        )


        if (
            "minimum" in normalized_question
            or "percentage" in normalized_question
        ):

            value = attendance.get(
                "minimum_percentage"
            )

            if value is not None:

                return (
                    f"The minimum attendance requirement "
                    f"is {value}%."
                )


        if (
            "medical" in normalized_question
            or "leave" in normalized_question
        ):

            return (
                f"Medical leave policy: "
                f"{attendance.get('medical_leave', 'Not available')}."
            )


        if attendance:

            return (
                f"Minimum attendance required: "
                f"{attendance.get('minimum_percentage')}%.\n"
                f"Policy: "
                f"{attendance.get('policy', 'Not available')}."
            )


    # =====================================================
    # WORKING HOURS
    # =====================================================

    if (
        "working hours" in normalized_question
        or "college timing" in normalized_question
        or "college hours" in normalized_question
        or "office timing" in normalized_question
        or "working time" in normalized_question
    ):

        working_hours = COLLEGE_DATA.get(
            "working_hours",
            {}
        )

        if working_hours:

            return (
                f"College timing: "
                f"{working_hours.get('college_opens')} to "
                f"{working_hours.get('college_closes')}.\n"
                f"Office timing: "
                f"{working_hours.get('office_opens')} to "
                f"{working_hours.get('office_closes')}."
            )


    # =====================================================
    # EVENTS
    # =====================================================

    if (
        "event" in normalized_question
        or "events" in normalized_question
        or "fest" in normalized_question
        or "sports" in normalized_question
    ):

        events = COLLEGE_DATA.get(
            "events",
            []
        )

        if events:

            return (
                "College events include:\n"
                + "\n".join(
                    f"• {event}"
                    for event in events
                )
            )


    return COLLEGE_NOT_FOUND_MESSAGE


# =========================================================
# PAGE ROUTES
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        college=COLLEGE_DATA
    )


@app.route("/courses")
def courses():

    return render_template(
        "courses.html",
        college=COLLEGE_DATA
    )


@app.route("/admission")
def admission():

    return render_template(
        "admission.html",
        college=COLLEGE_DATA
    )


@app.route("/fees")
def fees():

    return render_template(
        "fees.html",
        college=COLLEGE_DATA
    )


@app.route("/facilities")
def facilities():

    return render_template(
        "facilities.html",
        college=COLLEGE_DATA
    )


@app.route("/placement")
def placement():

    return render_template(
        "placement.html",
        college=COLLEGE_DATA
    )


@app.route("/attendance")
def attendance():

    return render_template(
        "attendance.html",
        college=COLLEGE_DATA
    )


# =========================================================
# COLLEGE DATA API
# =========================================================

@app.route("/api/college-data")
def get_college_data():

    if not COLLEGE_DATA:

        return jsonify({
            "error": "College data is empty."
        }), 500

    return jsonify(COLLEGE_DATA)


# =========================================================
# CHAT API
# =========================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        student_question = (
            data.get("question", "")
            .strip()
        )

        student_name = (
            data.get("student_name", "Student")
            .strip()
            or "Student"
        )

        if not student_question:

            return jsonify({
                "error": "Please enter a question"
            }), 400

        if len(student_question) > 500:

            return jsonify({
                "error":
                "Question is too long. "
                "Please keep it under 500 characters."
            }), 400

        ai_response = answer_college_question(
            student_question
        )

        try:

            save_chat(
                student_name,
                student_question,
                ai_response
            )

        except Exception as db_error:

            print(
                f"Database error: {db_error}"
            )

        return jsonify({
            "response": ai_response,
            "student_name": student_name
        })

    except Exception as error:

        print(
            f"Chat error: {error}"
        )

        return jsonify({
            "error":
            "An error occurred while processing "
            "your question."
        }), 500


# =========================================================
# CHAT HISTORY
# =========================================================

@app.route("/api/history")
def get_history():

    try:

        student_name = (
            request.args.get(
                "student_name",
                "Student"
            )
            .strip()
        )

        if not student_name:

            return jsonify({
                "error": "Student name required"
            }), 400

        history = get_chat_history(
            student_name,
            limit=10
        )

        return jsonify({
            "history": history,
            "student_name": student_name
        })

    except Exception as error:

        print(
            f"History error: {error}"
        )

        return jsonify({
            "error": "Could not retrieve history"
        }), 500


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Page not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    try:

        init_database()

        print(
            "Database initialized successfully."
        )

    except Exception as error:

        print(
            f"Database initialization error: {error}"
        )


    print("=" * 60)
    print("COLLEGE ASSISTANT STARTING")
    print("=" * 60)

    print(
        f"College: "
        f"{COLLEGE_DATA.get('college_name', 'Unknown')}"
    )

    print(
        f"Location: "
        f"{COLLEGE_DATA.get('college_location', 'Unknown')}"
    )

    print()
    print("Server running at:")
    print("http://127.0.0.1:5000")

    print()
    print("Pages:")
    print("Home       → /")
    print("Courses    → /courses")
    print("Admission  → /admission")
    print("Fees       → /fees")
    print("Facilities → /facilities")
    print("Placement  → /placement")
    print("Attendance → /attendance")

    print("=" * 60)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )