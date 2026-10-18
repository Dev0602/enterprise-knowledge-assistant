HARD_EVALUATION_DATASET = [

    # =========================================================
    # 01 - Employee Handbook
    # =========================================================
    {
        "question": "If I need to change my normal work schedule, who should I coordinate with?",
        "expected_source": "01_employee_handbook.pdf",
        "category": "paraphrase",
    },
    {
        "question": "I want the company to pay for a conference. What details should I provide before registering?",
        "expected_source": "01_employee_handbook.pdf",
        "category": "indirect",
    },
    {
        "question": "If I raise a workplace concern in good faith, can the company retaliate against me?",
        "expected_source": "01_employee_handbook.pdf",
        "category": "paraphrase",
    },
    {
        "question": "What should happen before the manager portion of a formal performance review?",
        "expected_source": "01_employee_handbook.pdf",
        "category": "detail",
    },

    # =========================================================
    # 02 - Remote Work Policy
    # =========================================================
    {
        "question": "If my job can be performed from home, what else affects whether remote work is allowed?",
        "expected_source": "02_remote_work_policy.pdf",
        "category": "indirect",
    },
    {
        "question": "While working from home, what information about my availability should I keep current?",
        "expected_source": "02_remote_work_policy.pdf",
        "category": "paraphrase",
    },
    {
        "question": "Is it acceptable to do company work from a public computer?",
        "expected_source": "02_remote_work_policy.pdf",
        "category": "detail",
    },
    {
        "question": "Does working remotely lower the standards for attendance or delivery?",
        "expected_source": "02_remote_work_policy.pdf",
        "category": "paraphrase",
    },

    # =========================================================
    # 03 - Information Security Policy
    # =========================================================
    {
        "question": "Can I save a customer document in my personal cloud drive?",
        "expected_source": "03_information_security_policy.pdf",
        "category": "indirect",
    },
    {
        "question": "A message asks me to click an unexpected login link. What should I do?",
        "expected_source": "03_information_security_policy.pdf",
        "category": "scenario",
    },
    {
        "question": "Am I allowed to open information in a system just because I technically have access to it?",
        "expected_source": "03_information_security_policy.pdf",
        "category": "indirect",
    },
    {
        "question": "What should happen if someone's company credentials may have been compromised?",
        "expected_source": "03_information_security_policy.pdf",
        "category": "scenario",
    },

    # =========================================================
    # 04 - Leave and Attendance Policy
    # =========================================================
    {
        "question": "I woke up sick and cannot work today. What am I expected to do?",
        "expected_source": "04_leave_and_attendance_policy.pdf",
        "category": "scenario",
    },
    {
        "question": "Where am I supposed to enter a PTO request?",
        "expected_source": "04_leave_and_attendance_policy.pdf",
        "category": "paraphrase",
    },
    {
        "question": "I need to be away from work for an extended period. Who should I speak with?",
        "expected_source": "04_leave_and_attendance_policy.pdf",
        "category": "indirect",
    },
    {
        "question": "If I unexpectedly cannot come to work, how quickly should I notify someone?",
        "expected_source": "04_leave_and_attendance_policy.pdf",
        "category": "scenario",
    },

    # =========================================================
    # 05 - IT Support and Acceptable Use
    # =========================================================
    {
        "question": "My computer problem is affecting many employees. Will that issue receive higher priority?",
        "expected_source": "05_it_support_and_acceptable_use.pdf",
        "category": "scenario",
    },
    {
        "question": "Can I download and install software from any website on my work computer?",
        "expected_source": "05_it_support_and_acceptable_use.pdf",
        "category": "indirect",
    },
    {
        "question": "What should I do before walking away from my workstation?",
        "expected_source": "05_it_support_and_acceptable_use.pdf",
        "category": "paraphrase",
    },
    {
        "question": "An email asks me to transfer money unexpectedly. What should I do before acting on it?",
        "expected_source": "05_it_support_and_acceptable_use.pdf",
        "category": "scenario",
    },

    # =========================================================
    # 06 - Business Travel Policy
    # =========================================================
    {
        "question": "For a normal work trip, should I book business class or economy?",
        "expected_source": "06_business_travel_policy.pdf",
        "category": "scenario",
    },
    {
        "question": "What documentation do I need when claiming expenses from a business trip?",
        "expected_source": "06_business_travel_policy.pdf",
        "category": "paraphrase",
    },
    {
        "question": "My trip was cancelled and I still have hotel and flight reservations. What should I do?",
        "expected_source": "06_business_travel_policy.pdf",
        "category": "scenario",
    },
    {
        "question": "Is a rideshare an allowed transportation option during a work trip?",
        "expected_source": "06_business_travel_policy.pdf",
        "category": "paraphrase",
    },

    # =========================================================
    # 07 - Employee Onboarding Guide
    # =========================================================
    {
        "question": "Besides getting equipment, what other things should a new hire complete on day one?",
        "expected_source": "07_employee_onboarding_guide.pdf",
        "category": "indirect",
    },
    {
        "question": "Who sets up the system accounts a new employee needs for their role?",
        "expected_source": "07_employee_onboarding_guide.pdf",
        "category": "paraphrase",
    },
    {
        "question": "During my first month, what topics should I discuss with my manager?",
        "expected_source": "07_employee_onboarding_guide.pdf",
        "category": "paraphrase",
    },
    {
        "question": "As a new employee, who should I contact if I cannot access a company system?",
        "expected_source": "07_employee_onboarding_guide.pdf",
        "category": "scenario",
    },
]
