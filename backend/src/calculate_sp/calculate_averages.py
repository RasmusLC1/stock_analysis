from dataclasses import fields
from statistics import mean
from backend.src.info.info_config import InfoConfig


class CalculateAverages:

    @staticmethod
    def calculate_averages(data_list: list[InfoConfig]) -> dict:

        if not data_list:
            return {}

        averages = {}

        for field in fields(InfoConfig):
            field_name = field.name

            values = CalculateAverages._extract_values(
                field_name, data_list
            )

            numeric_values = CalculateAverages._find_numeric_values(
                values
            )

            if numeric_values:
                averages[field_name] = mean(numeric_values)

        return averages

    @staticmethod
    def _find_numeric_values(values):
        return [
            value for value in values
            if isinstance(value, (int, float))
            and not isinstance(value, bool)
        ]

    @staticmethod
    def _extract_values(field_name, data_list):
        return [
            getattr(item, field_name)
            for item in data_list
        ]