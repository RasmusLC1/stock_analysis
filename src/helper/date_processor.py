from datetime import date

class Date_Processor:
  @staticmethod
  def process_date(start_date: date) -> str:
    return start_date.isoformat()  # "2026-10-01"