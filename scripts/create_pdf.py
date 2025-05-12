from fpdf import FPDF

def clean(text):
    return text.replace("’", "'").replace("–", "-").replace("—", "-")


# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

# Title
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="QA Interview Prep Guide", ln=True, align='C')
pdf.ln(10)

# Section: Mock Interview Script
pdf.set_font("Arial", 'B', 12)
pdf.cell(200, 10, txt="QA Mock Interview Script", ln=True)
pdf.set_font("Arial", size=12)

qa_pairs = [
    ("What is the difference between QA and QC?",
     "QA (Quality Assurance) is process-oriented; it ensures that the right methods and processes are followed. QC (Quality Control) is product-oriented; it verifies that the actual product meets requirements through testing and inspections."),
    ("Explain the software testing life cycle (STLC).",
     "The STLC includes: Requirement Analysis, Test Planning, Test Case Design, Test Environment Setup, Test Execution, and Test Closure."),
    ("What is regression testing?",
     "Regression testing ensures recent code changes haven’t broken existing functionality. It's often automated."),
    ("Explain boundary value analysis with an example.",
     "For input 1–100, test 0, 1, 2, 99, 100, and 101 – values at and around the boundaries."),
    ("Give an example of high severity but low priority.",
     "A crash in a rarely used, legacy feature. Severe but not urgent to fix."),
    ("Tell me about a challenging bug you encountered.",
     "A crash occurred only on Safari/iOS when the keyboard opened. We had to debug on real devices and use browser-specific handling."),
    ("How do you handle testing in an Agile environment?",
     "Join sprint planning, write test cases during development, perform continuous testing, and automate regressions.")
]

for question, answer in qa_pairs:
    pdf.set_font("Arial", 'B', 12)
    pdf.multi_cell(0, 10, f"Q: {clean(question)}")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"A: {clean(answer)}")
    pdf.ln(2)

# Section: Flashcards
pdf.add_page()
pdf.set_font("Arial", 'B', 12)
pdf.cell(200, 10, txt="QA Flashcard Set", ln=True)
pdf.set_font("Arial", size=12)

flashcards = [
    ("What does the 'pesticide paradox' mean?", "Repeating the same test cases won’t find new bugs."),
    ("What is system testing?", "Testing the complete, integrated system against requirements."),
    ("What is smoke testing?", "A basic set of tests to ensure critical functionalities work."),
    ("Explain equivalence partitioning.", "Divide input data into valid and invalid partitions and test one from each."),
    ("How is testing different in Agile?", "It's continuous, collaborative, and integrated into development cycles."),
    ("What’s low severity but high priority?", "A typo in the company’s name on the homepage."),
    ("What is defect clustering?", "Most defects occur in a few modules. Focus testing accordingly."),
    ("Who performs User Acceptance Testing?", "Business users or clients."),
    ("When do we perform regression testing?", "After changes to verify no existing functionality is broken.")
]

for q, a in flashcards:
    pdf.set_font("Arial", 'B', 12)
    pdf.multi_cell(0, 10, f"Q: {clean(q)}")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"A: {clean(a)}")
    pdf.ln(2)

# Save PDF
pdf.output("QA_Interview_Prep_Guide.pdf")
