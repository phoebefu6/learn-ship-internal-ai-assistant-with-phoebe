#!/usr/bin/env python3
"""Build the CONSTRUCTED data for learn-ship-internal-ai-assistant-with-phoebe.

Tidewell Freight is a constructed 1,200-person freight forwarder. Nothing here is a real company's
policy. This script writes, deterministically:
  materials/assist-data.json   the corpus, the golden set, the ticket log, the bench settings
  assets/assist-data.js        the same object for the browser, serialised with json.dumps

Corpus: policy clauses across HR, IT and Finance. Every clause carries a stable key (the clause
that answers a question, across versions), a version, an effective date, a superseded flag, an
owner and an access group. Old versions stay in the store with superseded = true, because real
document stores keep them.
Golden set: staff questions with the asker's group, the gold clause key(s), the risk tier, the
kind (answerable / restricted / no-policy), and a constructed thumbs signal.
Ticket log: 600 constructed tickets over one quarter, generated from a topic table with a seeded
mulberry32 so the browser and Python see the same rows.

Run:  python3 materials/build_assist_data.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# access groups: who may read a clause. Asker groups: staff, manager, hr, finance, it.
ACCESS = {
    "all": ["staff", "manager", "hr", "finance", "it"],
    "managers": ["manager", "hr"],
    "hr": ["hr"],
    "finance": ["finance"],
    "it": ["it"],
}

DOCS = {
    "HR-LV": ("Leave policy", "HR policy lead"),
    "HR-WFH": ("Hybrid work policy", "HR policy lead"),
    "HR-PAY": ("Pay and grading policy", "Reward manager"),
    "HR-PERF": ("Performance and conduct procedure", "HR business partner lead"),
    "HR-REC": ("Recruitment and referral policy", "Talent acquisition lead"),
    "HR-CON": ("Code of conduct", "General counsel"),
    "IT-ACC": ("Access and password standard", "IT security manager"),
    "IT-DEV": ("Devices standard", "IT operations manager"),
    "IT-SW": ("Software and AI tools standard", "IT operations manager"),
    "IT-INC": ("Security incident procedure", "IT security manager"),
    "IT-ADM": ("Privileged access procedure", "IT security manager"),
    "FIN-EXP": ("Expenses policy", "Financial controller"),
    "FIN-TRV": ("Travel policy", "Financial controller"),
    "FIN-PRO": ("Procurement policy", "Procurement manager"),
    "FIN-DOA": ("Delegation of authority", "Chief financial officer"),
    "FIN-AP": ("Supplier payments procedure", "Accounts payable lead"),
}

# (key, version, effective, superseded, access, title, text, answer)
C = [
    # ---------------- HR: leave ----------------
    ("HR-LV-1", "v3", "2026-01-01", False, "all", "Annual leave",
     "Annual leave, formerly called holiday entitlement: full-time staff earn 20 days of annual leave each calendar year. Part-time staff earn annual leave pro rata to contracted hours.",
     "Full-time staff earn 20 days of annual leave a year; part-time staff earn it pro rata."),
    ("HR-LV-1", "v2", "2023-04-01", True, "all", "Holiday entitlement",
     "Holiday entitlement: every employee receives 18 days holiday entitlement each year. Holiday entitlement days are added on 1 April.",
     "Every employee receives 18 days of holiday entitlement a year, added on 1 April."),
    ("HR-LV-2", "v3", "2026-01-01", False, "all", "Carrying leave over",
     "Up to 5 unused annual leave days carry over into the next calendar year and must be taken by 31 March. Days above 5 lapse unless HR agrees an exception in writing.",
     "Up to 5 unused days carry over and must be taken by 31 March; the rest lapse."),
    ("HR-LV-2", "v2", "2023-04-01", True, "all", "Carry forward",
     "Unused holiday can be carried forward: up to 10 unused holiday days carry forward to the next year and must be used by 30 June.",
     "Up to 10 unused holiday days carry forward and must be used by 30 June."),
    ("HR-LV-3", "v3", "2026-01-01", False, "all", "Sick leave",
     "Staff receive 14 days of paid sick leave each calendar year. A medical certificate is required for any sickness absence longer than 2 consecutive working days.",
     "You get 14 days of paid sick leave a year; a medical certificate is needed after 2 consecutive working days."),
    ("HR-LV-4", "v3", "2026-01-01", False, "all", "Parental leave",
     "The primary caregiver receives 16 weeks of paid parental leave after a birth or adoption. The secondary caregiver receives 4 weeks of paid parental leave, taken within 12 months.",
     "Primary caregivers get 16 weeks of paid parental leave, secondary caregivers 4 weeks within 12 months."),
    ("HR-LV-5", "v3", "2026-01-01", False, "all", "Compassionate leave",
     "Compassionate leave of 3 paid days is granted on the death of an immediate family member: spouse, child, parent or sibling. Managers may grant 2 further days.",
     "You get 3 paid days of compassionate leave for an immediate family bereavement; your manager may add 2."),
    ("HR-LV-6", "v3", "2026-01-01", False, "all", "Requesting leave",
     "Request leave in the HR portal. Requests for more than 3 consecutive days must be made at least 10 working days ahead, and your line manager approves or declines within 3 working days.",
     "Request leave in the HR portal; blocks over 3 days need 10 working days' notice and manager approval."),
    # ---------------- HR: hybrid work ----------------
    ("HR-WFH-1", "v2", "2025-07-01", False, "all", "Working from home",
     "Staff may work from home up to 2 days a week with their line manager's agreement. Core hours are 10:00 to 16:00 Singapore time on every working day, at home or in the office.",
     "You may work from home up to 2 days a week with your manager's agreement; core hours are 10:00 to 16:00."),
    ("HR-WFH-1", "v1", "2022-03-01", True, "all", "Remote work",
     "Remote work: employees may take up to 3 remote work days per week. Remote work days are agreed with the team each month.",
     "You may take up to 3 remote work days per week, agreed with your team monthly."),
    ("HR-WFH-2", "v2", "2025-07-01", False, "all", "Working abroad",
     "Working temporarily from another country needs written HR approval before travel, and is limited to 10 working days in a calendar year because of tax and immigration rules.",
     "Working from another country needs HR approval first and is capped at 10 working days a year."),
    # ---------------- HR: pay ----------------
    ("HR-PAY-1", "v4", "2025-01-01", False, "all", "Pay day",
     "Salary is paid monthly on the 25th. When the 25th falls on a weekend or public holiday, salary is paid on the previous working day. Payslips are published in the HR portal.",
     "Salaries are paid on the 25th, or the working day before; payslips are in the HR portal."),
    ("HR-PAY-2", "v4", "2025-01-01", False, "hr", "Salary bands",
     "Salary bands by grade, 2025: grade 5 SGD 48,000 to 62,000; grade 6 SGD 60,000 to 78,000; grade 7 SGD 76,000 to 98,000; grade 8 SGD 95,000 to 125,000 base salary a year.",
     "Grade 7 base salary band is SGD 76,000 to 98,000 a year."),
    ("HR-PAY-3", "v4", "2025-01-01", False, "all", "Overtime",
     "Non-exempt staff are paid overtime at 1.5 times the hourly rate for hours above 44 a week. Overtime must be approved by the line manager in advance and is paid with the next month's salary.",
     "Non-exempt staff get 1.5x for hours above 44 a week, approved in advance and paid next month."),
    ("HR-PAY-4", "v4", "2025-01-01", False, "managers", "Salary review",
     "Managers submit salary increase recommendations in the annual review cycle in March. Off-cycle increases need HR business partner and finance approval with a written business case.",
     "Salary increases go through the March review; off-cycle increases need HR and finance approval."),
    # ---------------- HR: performance and conduct ----------------
    ("HR-PERF-1", "v2", "2025-05-01", False, "managers", "Performance improvement plan",
     "Before starting a performance improvement plan, the manager must consult the HR business partner. A performance improvement plan lasts 8 weeks with fortnightly written reviews.",
     "Consult your HR business partner first; a performance improvement plan lasts 8 weeks with fortnightly reviews."),
    ("HR-PERF-2", "v2", "2025-05-01", False, "all", "Disciplinary hearing",
     "An employee invited to a disciplinary hearing receives written notice 5 working days before, and may bring a colleague or union representative as a companion.",
     "You get 5 working days' written notice and may bring a colleague or union representative."),
    ("HR-PERF-3", "v2", "2025-05-01", False, "all", "Probation",
     "New employees serve a probation period of 3 months. The notice period during probation is 1 week from either side; after confirmation it follows the employment contract.",
     "Probation is 3 months with 1 week's notice; after confirmation your contract's notice applies."),
    ("HR-REC-1", "v1", "2024-09-01", False, "all", "Employee referral bonus",
     "Staff who refer a candidate who is hired receive a referral bonus of SGD 1,000, paid after the new hire completes probation. Hiring managers are not eligible for their own vacancies.",
     "A successful referral earns SGD 1,000, paid once the new hire completes probation."),
    ("HR-REC-2", "v1", "2024-09-01", False, "managers", "Opening a vacancy",
     "To open a new headcount vacancy, the hiring manager submits a requisition with a finance sign-off. Replacement vacancies need only the department head's approval.",
     "New headcount needs a requisition with finance sign-off; replacements need the department head."),
    ("HR-CON-1", "v3", "2025-02-01", False, "all", "Gifts and hospitality",
     "Gifts or hospitality from customers or suppliers worth more than SGD 100 must be declared in the gifts register within 5 working days. Cash gifts must always be refused.",
     "Declare gifts or hospitality over SGD 100 within 5 working days; never accept cash."),
    ("HR-CON-2", "v3", "2025-02-01", False, "all", "Conflicts of interest",
     "Declare any conflict of interest, such as a family member (spouse, parent, brother or sister) who works for a supplier, or a second job, to your manager and in the conflicts register before taking part in the related decision.",
     "Declare conflicts of interest to your manager and in the register before the related decision."),
    # ---------------- IT ----------------
    ("IT-ACC-1", "v4", "2026-03-01", False, "all", "Passwords",
     "Passwords must be at least 14 characters. Passwords no longer expire on a schedule; change your password only if you suspect it is compromised, and never reuse a work password elsewhere.",
     "Use at least 14 characters; passwords do not expire, change it only if you suspect compromise."),
    ("IT-ACC-1", "v3", "2023-06-01", True, "all", "Password change",
     "Change your password every 90 days. Passwords must be at least 12 characters and the system blocks your last 5 passwords.",
     "Change your password every 90 days; at least 12 characters."),
    ("IT-ACC-2", "v4", "2026-03-01", False, "all", "Multi-factor authentication",
     "Multi-factor authentication is required for email, the VPN and every finance system. Register the authenticator app on your phone; lost phones are reported to the IT service desk.",
     "MFA is required for email, VPN and finance systems; register the authenticator app."),
    ("IT-ACC-3", "v4", "2026-03-01", False, "all", "Account lockout and reset",
     "After 5 failed sign-in attempts your account locks for 15 minutes. Reset a forgotten password yourself in the self-service password portal, or call the IT service desk.",
     "Accounts lock for 15 minutes after 5 failures; reset in the self-service password portal."),
    ("IT-DEV-1", "v2", "2025-04-01", False, "all", "Laptop refresh",
     "Company laptops are refreshed every 4 years. Request an earlier replacement through an IT ticket if the laptop fails or no longer runs required software.",
     "Laptops are refreshed every 4 years; raise an IT ticket for an early replacement."),
    ("IT-DEV-2", "v2", "2025-04-01", False, "all", "Lost or stolen devices",
     "Report a lost or stolen laptop or phone to IT security within 1 hour on the security hotline, so the device can be locked and wiped remotely.",
     "Report a lost or stolen device to IT security within 1 hour on the security hotline."),
    ("IT-DEV-3", "v2", "2025-04-01", False, "all", "Personal phones",
     "Personal phones may access company email and chat only after the device management app is installed. Company files must not be stored on personal devices.",
     "Personal phones can use email and chat only with the device management app installed."),
    ("IT-SW-1", "v3", "2026-02-01", False, "all", "Installing software",
     "Install software only from the company software catalogue. For anything not in the catalogue, raise an IT ticket with a business justification; IT security reviews it within 5 working days.",
     "Install only from the software catalogue; request anything else by IT ticket with a justification."),
    ("IT-SW-2", "v3", "2026-02-01", False, "all", "External AI tools",
     "Do not paste confidential or restricted data, including customer shipment records, into external AI tools. Public information may be used in the approved AI tools listed in the catalogue.",
     "Never paste confidential data, such as shipment records, into external AI tools; use the approved ones."),
    ("IT-INC-1", "v2", "2025-08-01", False, "all", "Phishing",
     "Report a suspicious email with the Report phishing button in your mail client. Do not click links or open attachments; if you already clicked, call the security hotline at once.",
     "Use the Report phishing button; if you already clicked, call the security hotline."),
    ("IT-INC-2", "v2", "2025-08-01", False, "all", "Data breach",
     "If you suspect personal data has been lost or exposed, report it to the data protection officer within 24 hours. The data protection officer decides whether regulators must be notified.",
     "Report a suspected personal data breach to the data protection officer within 24 hours."),
    ("IT-ADM-1", "v2", "2025-10-01", False, "it", "Local admin rights",
     "Local administrator rights on a laptop are granted for 24 hours through a privileged access request, approved by the IT security manager, and every session is logged.",
     "Local admin rights are granted for 24 hours via a privileged access request approved by IT security."),
    ("IT-ADM-2", "v2", "2025-10-01", False, "it", "Firewall exceptions",
     "Firewall rule exceptions need a change request, a named business owner and an expiry date no later than 90 days, reviewed at the weekly change board.",
     "Firewall exceptions need a change request, an owner and an expiry within 90 days."),
    # ---------------- Finance ----------------
    ("FIN-EXP-1", "v5", "2026-02-01", False, "all", "Submitting expense claims",
     "Submit expense claims in the expenses app within 30 days of the expense date, with an itemised receipt for every item over SGD 25. Late claims need the financial controller's approval.",
     "Submit claims within 30 days with itemised receipts over SGD 25; late claims need approval."),
    ("FIN-EXP-1", "v4", "2024-01-01", True, "all", "Expense claim deadline",
     "Expense claims must be submitted within 60 days. Attach a receipt for each expense claim item over SGD 50.",
     "Submit expense claims within 60 days, with receipts over SGD 50."),
    ("FIN-EXP-2", "v5", "2026-02-01", False, "all", "Meals when travelling",
     "When travelling on business, meals are covered by a daily allowance of SGD 60 in Singapore and up to SGD 90 abroad, claimed without receipts. Alcohol is never reimbursed.",
     "Meals on business travel are covered by a daily allowance of SGD 60 in Singapore, up to SGD 90 abroad."),
    ("FIN-EXP-2", "v4", "2024-01-01", True, "all", "Per diem",
     "Per diem for meals when travelling: SGD 50 per day in Singapore and SGD 70 per day abroad. Keep the per diem receipts.",
     "The meal per diem is SGD 50 a day in Singapore and SGD 70 abroad."),
    ("FIN-EXP-3", "v5", "2026-02-01", False, "all", "Client entertainment",
     "Client entertainment up to SGD 150 per guest needs no approval in advance. Above that, get your director's approval first and list every guest's name and company on the claim.",
     "Client entertainment up to SGD 150 per guest is fine; above that, get director approval first."),
    ("FIN-TRV-1", "v3", "2025-09-01", False, "all", "Flight class",
     "Book economy class for flights under 6 hours. Business class is allowed for flights of 6 hours or more with director approval. All flights are booked through the travel desk.",
     "Economy under 6 hours; business class from 6 hours with director approval, via the travel desk."),
    ("FIN-TRV-1", "v2", "2022-01-01", True, "all", "Business class",
     "Business class flights are permitted when the flight is longer than 8 hours. Book business class flights through the travel agent.",
     "Business class is permitted on flights longer than 8 hours."),
    ("FIN-TRV-2", "v3", "2025-09-01", False, "all", "Hotels",
     "Hotel rates are capped at SGD 250 a night in Asia and SGD 350 a night elsewhere, booked through the travel desk. Staying with friends earns no allowance.",
     "Hotels are capped at SGD 250 a night in Asia and SGD 350 elsewhere, via the travel desk."),
    ("FIN-PRO-1", "v2", "2025-03-01", False, "all", "Quotes for purchases",
     "Purchases over SGD 5,000 need three written quotes from different suppliers. Purchases over SGD 50,000 go to a tender run by procurement.",
     "Over SGD 5,000 you need three written quotes; over SGD 50,000 procurement runs a tender."),
    ("FIN-PRO-2", "v2", "2025-03-01", False, "all", "Purchase orders",
     "Raise a purchase order in the finance system before the supplier starts work. Invoices without a matching purchase order are returned to the supplier unpaid.",
     "Raise a purchase order before the supplier starts work; invoices without one are returned."),
    ("FIN-PRO-3", "v2", "2025-03-01", False, "all", "Corporate cards",
     "Corporate cards are for business expenses only, never personal use. Reconcile your corporate card statement in the expenses app by the 5th of each month.",
     "Corporate cards are business-only; reconcile your statement by the 5th of each month."),
    ("FIN-DOA-1", "v6", "2025-11-01", False, "managers", "Spending limits",
     "Delegated spending limits: team managers approve spend up to SGD 10,000; directors up to SGD 100,000; the chief financial officer up to SGD 500,000; above that, the board.",
     "Managers approve up to SGD 10,000, directors SGD 100,000, the CFO SGD 500,000, above that the board."),
    ("FIN-AP-1", "v2", "2025-06-01", False, "finance", "Supplier payment terms",
     "Suppliers are paid 30 days after the end of the invoice month. Early payment of a supplier invoice needs the chief financial officer's approval and a recorded reason.",
     "Suppliers are paid 30 days after month end; early payment needs CFO approval."),
    ("FIN-AP-2", "v2", "2025-06-01", False, "finance", "Month-end close",
     "Month-end close timetable: accruals posted by working day 3, intercompany balances agreed by working day 4, and management accounts issued on working day 6.",
     "Accruals by working day 3, intercompany by day 4, management accounts on day 6."),
]

CLAUSES = []
for key, ver, eff, sup, acc, title, text, ans in C:
    doc = key.rsplit("-", 1)[0]
    CLAUSES.append({
        "id": key + "@" + ver, "key": key, "doc": doc, "docTitle": DOCS[doc][0], "owner": DOCS[doc][1],
        "domain": doc.split("-")[0], "version": ver, "effective": eff, "superseded": sup,
        "access": acc, "title": title, "text": text, "answer": ans,
    })
# superseded clauses name the date their replacement took effect
for c in CLAUSES:
    if c["superseded"]:
        cur = [d for d in CLAUSES if d["key"] == c["key"] and not d["superseded"]][0]
        c["retiredOn"] = cur["effective"]

# Golden questions. kind: answerable (gold readable by the asker), restricted (gold exists, asker
# may not read it, so the right move is a hand-off), no-policy (no clause answers it).
# topic: the ticket-log topic the question was drawn from. tier: Tidewell's risk tier.
G = [
    # answerable, ordinary wording
    ("staff", "How many days of sick leave do I get, and when do I need a medical certificate?", ["HR-LV-3"], "answerable", "high", "leave"),
    ("staff", "How much paid parental leave does the primary caregiver get?", ["HR-LV-4"], "answerable", "high", "leave"),
    ("staff", "My grandmother died. How many days of compassionate leave can I take?", ["HR-LV-5"], "answerable", "medium", "leave"),
    ("staff", "How far ahead must I request leave for a two week trip?", ["HR-LV-6"], "answerable", "medium", "leave"),
    ("staff", "Can I work from another country for a few weeks?", ["HR-WFH-2"], "answerable", "high", "hybrid"),
    ("staff", "What are the core hours when working from home?", ["HR-WFH-1"], "answerable", "low", "hybrid"),
    ("staff", "Which day is salary paid this month?", ["HR-PAY-1"], "answerable", "medium", "pay"),
    ("staff", "How is overtime paid and who approves it?", ["HR-PAY-3"], "answerable", "high", "pay"),
    ("staff", "What notice do I get before a disciplinary hearing, and can I bring someone?", ["HR-PERF-2"], "answerable", "high", "conduct"),
    ("staff", "How long is probation and what is the notice period during it?", ["HR-PERF-3"], "answerable", "medium", "conduct"),
    ("staff", "Is there a bonus for referring a friend who gets hired?", ["HR-REC-1"], "answerable", "low", "recruiting"),
    ("staff", "A supplier sent me a hamper worth about SGD 200. Do I need to declare it?", ["HR-CON-1"], "answerable", "high", "conduct"),
    ("staff", "My brother works at one of our suppliers. What do I need to do?", ["HR-CON-2"], "answerable", "high", "conduct"),
    ("staff", "How many characters must a password have?", ["IT-ACC-1"], "answerable", "low", "access"),
    ("staff", "Is multi-factor authentication needed for the VPN?", ["IT-ACC-2"], "answerable", "low", "access"),
    ("staff", "My account is locked after failed sign-in attempts. How do I reset it?", ["IT-ACC-3"], "answerable", "low", "access"),
    ("staff", "When will my laptop be replaced with a new one?", ["IT-DEV-1"], "answerable", "low", "devices"),
    ("staff", "I lost my laptop in a taxi. Who do I report it to, and how fast?", ["IT-DEV-2"], "answerable", "high", "devices"),
    ("staff", "Can I read work email on my personal phone?", ["IT-DEV-3"], "answerable", "medium", "devices"),
    ("staff", "How do I get software installed that is not in the catalogue?", ["IT-SW-1"], "answerable", "low", "software"),
    ("staff", "Can I paste customer shipment records into an external AI tool to summarise them?", ["IT-SW-2"], "answerable", "high", "software"),
    ("staff", "I clicked a link in a suspicious phishing email. What now?", ["IT-INC-1"], "answerable", "high", "security"),
    ("staff", "I think customer personal data was exposed by mistake. Who do I report it to?", ["IT-INC-2"], "answerable", "high", "security"),
    ("staff", "What is the hotel limit per night in Asia?", ["FIN-TRV-2"], "answerable", "medium", "travel"),
    ("staff", "How much can I spend per guest on client entertainment without approval?", ["FIN-EXP-3"], "answerable", "medium", "expenses"),
    ("staff", "How many quotes do I need for a purchase of SGD 8,000?", ["FIN-PRO-1"], "answerable", "medium", "purchasing"),
    ("staff", "Do I need a purchase order before the supplier starts work?", ["FIN-PRO-2"], "answerable", "medium", "purchasing"),
    ("staff", "When do I reconcile my corporate card statement?", ["FIN-PRO-3"], "answerable", "low", "expenses"),
    ("manager", "What must I do before starting a performance improvement plan?", ["HR-PERF-1"], "answerable", "high", "conduct"),
    ("manager", "How do I open a new headcount vacancy?", ["HR-REC-2"], "answerable", "medium", "recruiting"),
    ("manager", "Up to what amount can I approve spend as a team manager?", ["FIN-DOA-1"], "answerable", "high", "purchasing"),
    ("manager", "Can I give someone an off-cycle salary increase?", ["HR-PAY-4"], "answerable", "high", "pay"),
    ("hr", "What is the salary band for grade 7?", ["HR-PAY-2"], "answerable", "high", "pay"),
    ("finance", "When are suppliers paid, and who approves early payment?", ["FIN-AP-1"], "answerable", "medium", "purchasing"),
    ("it", "How are local admin rights granted on a laptop?", ["IT-ADM-1"], "answerable", "medium", "access"),
    # answerable, asked in the OLD policy's words (staff keep the vocabulary of the version they learned)
    ("staff", "How many days of holiday entitlement do I get each year?", ["HR-LV-1"], "answerable", "high", "leave"),
    ("staff", "Can I carry forward unused holiday days, and until when?", ["HR-LV-2"], "answerable", "high", "leave"),
    ("staff", "How many remote work days per week can I take?", ["HR-WFH-1"], "answerable", "medium", "hybrid"),
    ("staff", "How often must I change my password?", ["IT-ACC-1"], "answerable", "low", "access"),
    ("staff", "How long do I have to submit an expense claim?", ["FIN-EXP-1"], "answerable", "high", "expenses"),
    ("staff", "What is the per diem for meals when travelling?", ["FIN-EXP-2"], "answerable", "high", "expenses"),
    ("staff", "When am I allowed to fly business class?", ["FIN-TRV-1"], "answerable", "medium", "travel"),
    # restricted: a clause answers it, but not one this asker may read
    ("staff", "What is the salary band for grade 7?", ["HR-PAY-2"], "restricted", "high", "pay"),
    ("staff", "How do I get local admin rights on my laptop?", ["IT-ADM-1"], "restricted", "medium", "access"),
    ("staff", "What spending limit does a director have?", ["FIN-DOA-1"], "restricted", "medium", "purchasing"),
    ("staff", "How long does a performance improvement plan last?", ["HR-PERF-1"], "restricted", "high", "conduct"),
    ("manager", "When are the month-end close accruals due?", ["FIN-AP-2"], "restricted", "medium", "purchasing"),
    ("staff", "Who approves early payment of a supplier invoice?", ["FIN-AP-1"], "restricted", "medium", "purchasing"),
    # no policy covers it
    ("staff", "Can I bring my dog to the office?", [], "no-policy", "low", "facilities"),
    ("staff", "Do we get a day off on our birthday?", [], "no-policy", "medium", "leave"),
    ("staff", "How do I book a meeting room for a client visit?", [], "no-policy", "low", "facilities"),
    ("staff", "Is there a staff discount at the gym near the office?", [], "no-policy", "low", "facilities"),
    ("staff", "What is the dress code for client visits?", [], "no-policy", "low", "conduct"),
    ("staff", "When is the annual staff party this year?", [], "no-policy", "low", "facilities"),
]


def mulberry32(a):
    """Same generator as the browser engine (assist-live.js)."""
    state = [a & 0xFFFFFFFF]

    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF

    def r():
        state[0] = (state[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = state[0]
        t = imul(t ^ (t >> 15), 1 | t)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


# constructed satisfaction signal: staff tend to thumb up an answer that sounds sure, and thumb down
# a hand-off. Drawn once here, stored, never recomputed (so both engines read the same bits).
rs = mulberry32(20261017)
GOLDEN = []
for i, (asker, q, gold, kind, tier, topic) in enumerate(G, 1):
    GOLDEN.append({"id": "G%02d" % i, "asker": asker, "q": q, "gold": gold, "kind": kind, "tier": tier,
                   "topic": topic, "thumbsAnswer": rs() < 0.88, "thumbsHandoff": rs() < 0.30})

# Ticket log topics: (topic, team, resolution, weight, minutes lo, minutes hi)
# resolution: policy = answered by pointing at a clause; action = a person had to do something
# (reset, repair, payroll fix); no-policy = nobody had written the answer down.
TOPICS = [
    ("leave", "HR", "policy", 70, 6, 15), ("leave", "HR", "action", 22, 15, 40),
    ("hybrid", "HR", "policy", 24, 6, 12),
    ("pay", "HR", "policy", 30, 8, 20), ("pay", "HR", "action", 26, 20, 60),
    ("conduct", "HR", "policy", 14, 10, 30), ("recruiting", "HR", "policy", 10, 6, 15),
    ("access", "IT", "policy", 36, 5, 12), ("access", "IT", "action", 64, 10, 25),
    ("devices", "IT", "policy", 18, 5, 12), ("devices", "IT", "action", 46, 30, 120),
    ("software", "IT", "policy", 22, 6, 15), ("software", "IT", "action", 30, 20, 60),
    ("security", "IT", "policy", 12, 10, 25),
    ("expenses", "Finance", "policy", 48, 6, 15), ("expenses", "Finance", "action", 20, 15, 45),
    ("travel", "Finance", "policy", 26, 6, 15), ("purchasing", "Finance", "policy", 24, 8, 20),
    ("purchasing", "Finance", "action", 12, 20, 60),
    ("facilities", "HR", "no-policy", 26, 5, 20), ("leave", "HR", "no-policy", 8, 10, 25),
    ("conduct", "HR", "no-policy", 6, 10, 30), ("software", "IT", "no-policy", 6, 10, 30),
]
rt = mulberry32(7741)
WSUM = sum(t[3] for t in TOPICS)
TICKETS = []  # [topic index, month 0..2, minutes]
for n in range(600):
    x = rt() * WSUM
    k = 0
    while x >= TOPICS[k][3]:
        x -= TOPICS[k][3]
        k += 1
    lo, hi = TOPICS[k][4], TOPICS[k][5]
    TICKETS.append([k, int(rt() * 3), lo + int(rt() * (hi - lo + 1))])

SETTINGS = {
    "bm25": {"k1": 1.2, "b": 0.75},
    "k": 3,
    "abstainBelow": 3.0,
    "access": ACCESS,
    "rungs": [
        {"id": "r1", "label": "1 · No permission filter", "perm": False, "version": False, "abstain": False},
        {"id": "r2", "label": "2 · + permission filter", "perm": True, "version": False, "abstain": False},
        {"id": "r3", "label": "3 · + current-version filter", "perm": True, "version": True, "abstain": False},
        {"id": "r4", "label": "4 · + abstain and hand off", "perm": True, "version": True, "abstain": True},
    ],
    # Tidewell's own go/no-go policy. A policy choice, not a standard.
    "gate": {"maxLeaks": 0, "maxStale": 0, "maxWrongRate": {"high": 0.05, "medium": 0.10, "low": 0.20},
             "minCoverage": 0.70, "minHandoffRight": 0.80},
    "thumbsGate": 0.75,
    # Break button: the expenses policy v4 PDF was re-imported and lost its superseded flag.
    "breakDoc": "FIN-EXP", "breakVersion": "v4",
    # Cost assumptions. ASSUMPTION, not a vendor price list.
    "cost": {"systemTokens": 350, "outputTokens": 150, "tokensPerWord": 1.3,
             "inPerM": [0.10, 3.00], "outPerM": [0.40, 15.00], "usdToSgd": 1.35,
             "questionsPerMonth": 2400, "ticketMinutes": 12, "ticketSgdPerHour": 45},
    "staff": 1200,
}

DATA = {"constructed": True, "company": "Tidewell Freight (constructed)", "clauses": CLAUSES,
        "golden": GOLDEN, "topics": [list(t) for t in TOPICS], "tickets": TICKETS, "settings": SETTINGS}

if __name__ == "__main__":
    with open(os.path.join(HERE, "assist-data.json"), "w", encoding="utf-8") as f:
        json.dump(DATA, f, indent=1, ensure_ascii=True)
    js = ("/* assist-data.js - CONSTRUCTED data for the go/no-go bench. Tidewell Freight is invented.\n"
          "   Generated by materials/build_assist_data.py with json.dumps; do not hand-edit. */\n"
          "window.ASSIST_DATA = " + json.dumps(DATA, ensure_ascii=True, separators=(",", ":")) + ";\n")
    with open(os.path.join(REPO, "assets", "assist-data.js"), "w", encoding="utf-8") as f:
        f.write(js)
    print("clauses", len(CLAUSES), "current", sum(not c["superseded"] for c in CLAUSES),
          "golden", len(GOLDEN), "tickets", len(TICKETS), "js bytes", len(js))
