class BurnoutAnalyzer:
    """Calculates burnout risk and productivity from study lifestyle data."""

    @staticmethod
    def calculate_burnout_score(sleep_hours, study_hours, stress_level, mood_level, breaks_count):
        score = 0
        if sleep_hours < 6:
            score += 25
        elif sleep_hours < 7:
            score += 12

        if study_hours > 8:
            score += 25
        elif study_hours > 6:
            score += 12

        score += int(stress_level) * 4
        score += max(0, 10 - int(mood_level)) * 3

        if breaks_count == 0:
            score += 15
        elif breaks_count < 3:
            score += 7

        return max(0, min(score, 100))

    @staticmethod
    def get_risk_level(score):
        if score >= 70:
            return "High"
        if score >= 40:
            return "Medium"
        return "Low"

    @staticmethod
    def calculate_productivity_score(sleep_hours, study_hours, stress_level, mood_level, breaks_count):
        score = 100
        score -= abs(8 - float(sleep_hours)) * 5
        score -= max(0, float(study_hours) - 7) * 6
        score -= int(stress_level) * 3
        score += int(mood_level) * 2
        score += min(int(breaks_count), 5) * 3
        return max(0, min(int(score), 100))

    @staticmethod
    def get_advice(risk_level):
        if risk_level == "High":
            return "High burnout risk. Reduce study load, sleep more, take breaks, and talk to a trusted person if stress feels overwhelming."
        if risk_level == "Medium":
            return "Medium risk. Try a balanced study schedule, short breaks, and better sleep routine."
        return "Low risk. Keep your current healthy routine and track your progress weekly."
