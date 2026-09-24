from openpyxl import Workbook
from openpyxl.packaging import workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment

from pathlib import Path

from uik_info.protocol import LABELES
from uik_info.uiks import Uiks

from party_color import PARTY_COLOR
from get_requests.get_requests import Requests


class Table:

    def __init__(self, district: int):
        self.workbook : Workbook = Workbook()
        self.active_list = self.workbook.active
        self.active_list.title = "Одномандатники"
        self.district : int = district

    def paint(self):
        self.firstColumn()
        self.secondColumn()
        self.otherColumns()
        self.settings()

    def createList(self, name: str):
        self.active_list = self.workbook.create_sheet(name)

    def setUiks(self, uiks: Uiks):
        self.uiks = uiks

    def setHeight(self):
        self.active_list.sheet_format.defaultRowHeight = 50

    def dump(self):

        root = Path(__file__).resolve().parent.parent
        path = root / f"tables/gosduma2026_district_{self.district}.xlsx"

        self.workbook.save(path)


    def firstColumn(self):
        self.active_list["A1"] = "УИК"
        self.active_list["A2"] = "Район"
        for i in range(0, 13):
            self.active_list[f"A{3+i}"] = LABELES[i]

        candidates = self.uiks.getListUiks()[0].getCandidates().getCandidateList()

        for i, candidate in enumerate(candidates):
            cell = f"A{16 + i}"
            self.active_list[cell] = candidates[i].getName()
            color = PARTY_COLOR[candidates[i].getParty()]
            self.paintCell(cell, color)

    def secondColumn(self):
        self.active_list["B1"] = "Все"
        sum_protocol = self.uiks.getSumProtocol().get_protocol()
        candidates = self.uiks.getListUiks()[0].getCandidates().getCandidateList()

        for i in range(0, 13):
            self.active_list[f"B{3+i}"] = sum_protocol[i]

        self.active_list.cell(15, 2).number_format = "0.0%"
        self.paintCellGradient(15, 2, '000000', sum_protocol[12], 1)
        self.active_list.cell(15, 2).font = Font(color="FF69B4")

        candidates_full = self.uiks.getCandidatesFull()

        all_votes = sum([candidates_full[name] for name in candidates_full.keys()])

        for i, candidate in enumerate(candidates):
            cell = f"B{16+i}"
            votes = self.uiks.getCandidatesFull()[candidate.getName()]
            self.paintCellGradient(16+i, 2, PARTY_COLOR[candidate.getParty()], sum_protocol[12], 0.4)
            self.active_list[cell] = votes

    def otherColumns(self):
        for i, uik in enumerate(self.uiks.getListUiks()):
            column = 3+i
            protocol = uik.getProtocol().get_protocol()
            candidates = uik.getCandidates().getCandidateList()

            self.active_list.cell(row=1, column=column, value=f"УИК {uik.getId()}")
            self.active_list.cell(row=2, column=column, value=uik.getTik())

            for i in range(0, 13):
                self.active_list.cell(row=3+i, column=column, value=protocol[i])
            self.active_list.cell(15, column).number_format = "0.0%"
            self.paintCellGradient(15, column, '000000', protocol[12], 1)
            self.active_list.cell(15, column).font = Font(color="FF69B4")

            for i, candidate in enumerate(candidates):
                self.active_list.cell(row=16 + i, column=column, value=candidate.getVotes())
                self.paintCellGradient(16 + i, column, PARTY_COLOR[candidate.getParty()], candidate.getPercent(), 0.4)


    def paintCell(self, cell: str, color: str):
        fill = PatternFill(
            start_color=color,
            end_color=color,
            fill_type="solid"
        )
        self.active_list[cell].fill = fill

    def paintCellGradient(self, row: int, column: int, color: str, intensity: float, coeficent: float):
        intensity = max(0.0, min(1.0, intensity)) ** coeficent

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
        self.active_list.cell(row=row, column=column).fill = fill

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

        for row in self.active_list.iter_rows():
            for cell in row:
                cell.border = border

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
                    vertical="center",
                    horizontal="center"
                )

        thick = Side(
            style="thick",
            color="000000"
        )

        for row in self.active_list.iter_rows():
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

            for row in self.active_list.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(
                        wrap_text=True,
                        vertical="center",
                        horizontal="center"
                    )

            for column in range(2, self.active_list.max_column + 1):
                letter = get_column_letter(column)
                self.active_list.column_dimensions[letter].width = 20

            for row in range(1, self.active_list.max_row + 1):
                # Смотрим, есть ли в строке длинный текст
                max_len = 0
                for cell in self.active_list[row]:
                    if cell.value and isinstance(cell.value, str):
                        max_len = max(max_len, len(cell.value))