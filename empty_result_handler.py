class EmptyResultHandler:
    """
    Handles cases where no schemes match the user's query.
    """

    CATEGORY_SUGGESTIONS = {
        "education": {
            "hi": "शिक्षा से जुड़ी योजनाएँ",
            "en": "education-related schemes"
        },
        "healthcare": {
            "hi": "स्वास्थ्य से जुड़ी योजनाएँ",
            "en": "healthcare-related schemes"
        },
        "financial_aid": {
            "hi": "वित्तीय सहायता योजनाएँ",
            "en": "financial aid schemes"
        }
    }

    CLARIFYING_QUESTIONS = {
        "category": {
            "hi": "क्या आप शिक्षा, स्वास्थ्य या वित्तीय सहायता से जुड़ी योजना ढूंढ रहे हैं?",
            "en": "Are you looking for education, healthcare, or financial aid schemes?"
        },
        "demographic": {
            "hi": "यह योजना किसके लिए है? (छात्र, किसान, महिला, वरिष्ठ नागरिक)",
            "en": "Who is this scheme for? (student, farmer, women, senior citizen)"
        }
    }

    def handle(self, entities: dict = None, lang: str = "hi") -> dict:
        """
        Generate fallback response when no schemes are found.
        """
        entities = entities or {}

        suggestions = []
        for key, value in self.CATEGORY_SUGGESTIONS.items():
            suggestions.append(value[lang])

        questions = []

        if not entities.get("category"):
            questions.append(self.CLARIFYING_QUESTIONS["category"][lang])

        if not entities.get("demographic"):
            questions.append(self.CLARIFYING_QUESTIONS["demographic"][lang])

        return {
            "message": self._build_message(suggestions, questions, lang),
            "suggested_categories": list(self.CATEGORY_SUGGESTIONS.keys()),
            "clarifying_questions": questions
        }

    def _build_message(self, suggestions, questions, lang):
        if lang == "hi":
            msg = "माफ़ कीजिए, आपकी खोज से कोई योजना नहीं मिली।\n"
            msg += "आप इन श्रेणियों की योजनाएँ देख सकते हैं:\n"
        else:
            msg = "Sorry, no schemes matched your query.\n"
            msg += "You may explore schemes in these categories:\n"

        for s in suggestions:
            msg += f"- {s}\n"

        if questions:
            msg += "\n"
            for q in questions:
                msg += f"{q}\n"

        return msg.strip()
