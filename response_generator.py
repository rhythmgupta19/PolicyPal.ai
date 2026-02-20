class ResponseGenerator:
    """
    Generates user-facing responses from scheme data.
    Hindi-first, plain-language, action-oriented.
    """

    def generate(self, schemes: list, lang: str = "hi") -> str:
        """
        Generate a complete response for matched schemes.
        """
        if not schemes:
            return ""

        responses = []
        for scheme in schemes:
            responses.append(self._format_scheme(scheme, lang))

        header = (
            "आपके लिए उपलब्ध योजनाएँ:\n\n"
            if lang == "hi"
            else "Available schemes for you:\n\n"
        )

        return header + "\n\n".join(responses)

    def simplify_text(self, text: str) -> str:
        """
        Simplify text for plain-language output.
        - Remove excessive whitespace
        - Shorten long sentences (basic heuristic)
        """
        if not text:
            return ""

        simplified = " ".join(text.strip().split())

        # Optional: truncate very long descriptions
        if len(simplified) > 300:
            simplified = simplified[:297] + "..."

        return simplified

    def format_action_steps(self, steps: list, lang: str = "hi") -> str:
        """
        Format action steps as numbered instructions.
        """
        if not steps:
            return ""

        lines = []
        for idx, step in enumerate(steps, start=1):
            lines.append(f"{idx}. {step}")

        title = (
            "\nआवेदन के चरण:\n"
            if lang == "hi"
            else "\nApplication steps:\n"
        )

        return title + "\n".join(lines)

    def _format_scheme(self, scheme: dict, lang: str) -> str:
        """
        Format a single scheme entry.
        """
        name = scheme.get(f"name_{lang}") or scheme.get("name_en", "")
        description = scheme.get(f"description_{lang}") or scheme.get("description_en", "")
        eligibility = scheme.get(f"eligibility_{lang}") or scheme.get("eligibility_en", "")
        benefits = scheme.get(f"benefits_{lang}") or scheme.get("benefits_en", "")

        description = self.simplify_text(description)
        eligibility = self.simplify_text(eligibility)
        benefits = self.simplify_text(benefits)

        output = f"🔹 {name}\n"
        output += f"विवरण: {description}\n" if lang == "hi" else f"Description: {description}\n"
        output += f"पात्रता: {eligibility}\n" if lang == "hi" else f"Eligibility: {eligibility}\n"
        output += f"लाभ: {benefits}" if lang == "hi" else f"Benefits: {benefits}"

        # Optional default action steps
        steps_hi = [
            "आधिकारिक वेबसाइट पर जाएँ",
            "आवेदन फॉर्म भरें",
            "आवश्यक दस्तावेज़ अपलोड करें"
        ]
        steps_en = [
            "Visit the official website",
            "Fill out the application form",
            "Upload required documents"
        ]

        output += self.format_action_steps(
            steps_hi if lang == "hi" else steps_en,
            lang
        )

        return output
