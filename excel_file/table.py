from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path

class Table:

    def __init__(self):
        self.workbook : Workbook = Workbook()
        self.active_list = self.workbook.active

        self.settings()

        self.active_list["A1"] = "asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdsdasdasdasdasdasdasdasdasdsfasdsad"
        self.active_list["A2"] = "asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdsdasdasdasdasdasdasdasdasdsfasdsad"

    def setHeight(self):
        self.active_list.sheet_format.defaultRowHeight = 50

    def dump(self):
        root = Path(__file__).resolve().parent.parent
        path = root / "table.xlsx"

        self.workbook.save(path)


    def settings(
        self,
        first_column_width: int = 30,
        other_columns_width: int = 15
    ):

        # Ширина первого столбца
        self.active_list.column_dimensions["A"].width = first_column_width

        # Ширина всех остальных столбцов
        for column in range(2, self.active_list.max_column + 1):
            letter = get_column_letter(column)
            self.active_list.column_dimensions[letter].width = other_columns_width

        # Автоматический перенос текста
        for row in self.active_list.iter_rows():
            for cell in row:
                cell.alignment = Alignment(
                    wrap_text=True,
                    vertical="center"
                )