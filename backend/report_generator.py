import datetime
from typing import List

class ReportGenerator:
    @staticmethod
    def generate_markdown(date: datetime.date, analysis_results: List[dict]) -> str:
        report = f"# 커뮤니티 동향 리포트 ({date.strftime('%Y-%m-%d')})\n\n"

        for res in analysis_results:
            report += f"## {res['platform']} - {res['channel']}\n"
            report += f"{res['analysis']}\n\n"

        report += "---\n*본 리포트는 AI에 의해 자동 생성되었습니다.*"
        return report

    @staticmethod
    def save_to_file(content: str, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
