from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.cell.cell import Cell, MergedCell
from openpyxl.worksheet.worksheet import Worksheet

from pathlib import Path

from typing import cast

from uik_info.protocol import LABELS
from uik_info.uik import Uik
from uik_info.uiks import Uiks

from party_color import PARTY_COLOR


class Table:
    PROTOCOL_START_ROW = 3
    PROTOCOL_ROWS = 13
    TURNOUT_ROW = 15
    CANDIDATES_START_ROW = 16

    def __init__(self, district: int):
        self.percent_mode : bool = False
        self.uiks = None
        self.workbook : Workbook = Workbook()
        self.sheet : Worksheet = cast(Worksheet, self.workbook.active)
        self.sheet.title = "Одномандатники"
        self.district : int = district

    def paint(self):
        if self.uiks is None:
            raise RuntimeError("UIKs not set. Call setUiks() first.")
        self.first_column()
        self.second_column()
        self.other_columns()
        self.settings()

    def create_sheet(self, name: str):
        self.sheet = self.workbook.create_sheet(name)

    def set_percent_mode(self, percent_mode):
        self.percent_mode = percent_mode

    def get_percent_mode(self):
        return self.percent_mode

    def set_uiks(self, uiks: Uiks):
        self.uiks = uiks

    def set_height(self):
        self.sheet.sheet_format.defaultRowHeight = 50

    def dump(self):
        root = Path(__file__).resolve().parent.parent
        path = root / f"tables/gosduma2026_district_{self.district}.xlsx"

        self.workbook.save(path)


    def first_column(self):
        self.sheet.cell(row=1, column=1, value="УИК")
        self.sheet.cell(row=2, column=1, value="Район")
        for i in range(0, self.PROTOCOL_ROWS):
            self.sheet.cell(row=self.PROTOCOL_START_ROW + i, column=1, value=LABELS[i])

        candidates = self.uiks.get_list_uiks()[0].get_candidates().get_candidate_list()

        for i, candidate in enumerate(candidates):
            cell = self.sheet.cell(row=self.CANDIDATES_START_ROW + i, column=1)
            cell.value = candidate.get_name()
            color = PARTY_COLOR[candidate.get_party()]
            Table.paint_cell(cell, color)

    def second_column(self):
        self.sheet.cell(row=1, column=2, value="Все")
        sum_protocol = self.uiks.get_sum_protocol().get_data()
        candidates = self.uiks.get_list_uiks()[0].get_candidates().get_candidate_list()

        for i in range(0, self.PROTOCOL_ROWS):
            self.sheet.cell(row=self.PROTOCOL_START_ROW + i, column=2, value=sum_protocol[i])

        cell_turnout = self.sheet.cell(row=self.TURNOUT_ROW, column=2)
        Table._setting_turnout_cell(cell_turnout, sum_protocol[self.PROTOCOL_ROWS-1])

        all_votes = self.uiks.get_sum_all_votes()

        for i, candidate in enumerate(candidates):
            cell = self.sheet.cell(row=self.CANDIDATES_START_ROW + i, column=2)
            votes = self.uiks.get_candidates_full()[candidate.get_name()]
            Table.paint_cell_gradient(cell, PARTY_COLOR[candidate.get_party()], votes / all_votes, 0.4)
            if self.get_percent_mode():
                cell.number_format = "0.00%"
                cell.value = votes / all_votes
            else:
                cell.value = votes

    def other_columns(self):
        for _idx, uik in enumerate(self.uiks.get_list_uiks()):
            column = 3+_idx
            protocol = uik.get_protocol().get_data()
            candidates = uik.get_candidates().get_candidate_list()

            self.sheet.cell(row=1, column=column, value=f"УИК {uik.get_id()}")
            self.sheet.cell(row=2, column=column, value=uik.get_tik())

            for i in range(0, self.PROTOCOL_ROWS):
                self.sheet.cell(row=self.PROTOCOL_START_ROW+i, column=column, value=protocol[i])

            cell_turnout = self.sheet.cell(row=self.TURNOUT_ROW, column=column)
            Table._setting_turnout_cell(cell_turnout, protocol[self.PROTOCOL_ROWS-1])

            for i, candidate in enumerate(candidates):
                cell = self.sheet.cell(row=self.CANDIDATES_START_ROW + i, column=column)
                if self.get_percent_mode():
                    cell.number_format = "0.00%"
                    cell.value = candidate.get_percent()
                else:
                    cell.value = candidate.get_votes()

                Table.paint_cell_gradient(cell, PARTY_COLOR[candidate.get_party()], candidate.get_percent(), 0.4)

    @staticmethod
    def _setting_turnout_cell(cell: Cell | MergedCell, percent_turnout: float):
        cell.number_format = "0.0%"
        Table.paint_cell_gradient(cell, '000000', percent_turnout, 1)
        cell.font = Font(color="FF69B4")

    @staticmethod
    def _fill_candidate():
        ...

    @staticmethod
    def paint_cell(cell: Cell | MergedCell, color: str):
        fill = PatternFill(
            start_color=color,
            end_color=color,
            fill_type="solid"
        )
        cell.fill = fill

    @staticmethod
    def paint_cell_gradient(cell: Cell | MergedCell, color: str, intensity: float, coefficient: float):
        intensity = max(0.0, min(1.0, intensity)) ** coefficient

        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        r = int(255 + (r - 255) * intensity)
        g = int(255 + (g - 255) * intensity)
        b = int(255 + (b - 255) * intensity)

        result_color = f"{r:02X}{g:02X}{b:02X}"

        fill = PatternFill(
            start_color=result_color,
            end_color=result_color,
            fill_type="solid"
        )
        cell.fill = fill

    def settings(
        self,
        first_column_width: int = 30,
        other_columns_width: int = 24
    ):

        thin = Side(style="thin", color="000000")

        border = Border(
            left=thin,
            right=thin,
            top=thin,
            bottom=thin
        )

        for row in self.sheet.iter_rows():
            for cell in row:
                cell.border = border

        # Ширина первого столбца
        self.sheet.column_dimensions["A"].width = first_column_width

        # Ширина всех остальных столбцов
        for column in range(2, self.sheet.max_column + 1):
            letter = get_column_letter(column)
            self.sheet.column_dimensions[letter].width = other_columns_width

        # Автоматический перенос текста
        for row in self.sheet.iter_rows():
            for cell in row:
                cell.alignment = Alignment(
                    wrap_text=True,
                    vertical="center",
                    horizontal="center"
                )

        thick = Side(
            style="thick",
            color="000000"
        )

        for row in self.sheet.iter_rows():
            # граница между A и B
            row[0].border = Border(
                right=thick,
                left=row[0].border.left,
                top=row[0].border.top,
                bottom=row[0].border.bottom
            )

            # граница между C и D
            row[1].border = Border(
                right=thick,
                left=row[1].border.left,
                top=row[1].border.top,
                bottom=row[1].border.bottom
            )

            for row in self.sheet.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(
                        wrap_text=True,
                        vertical="center",
                        horizontal="center"
                    )

            for column in range(2, self.sheet.max_column + 1):
                letter = get_column_letter(column)
                self.sheet.column_dimensions[letter].width = 20

            for row in range(1, self.sheet.max_row + 1):
                # Смотрим, есть ли в строке длинный текст
                max_len = 0
                for cell in self.sheet[row]:
                    if cell.value and isinstance(cell.value, str):
                        max_len = max(max_len, len(cell.value))