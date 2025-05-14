from pathlib import Path
import pyexcel_xlsx
from typing import Iterator, List, Dict, Any, Generator


class MailingData:
    def __init__(self, excelFile: Path) -> None:
        # Ouvre le fichier xlsx
        data: dict = pyexcel_xlsx.get_data(str(excelFile))
        # Créé un itérateur sur la première feuille
        self._sheet: List[List[Any]] = next(iter(data.values()))
        # Vérifie que la feuille n'est pas vide
        if self._sheet is None or len(self._sheet) == 0:
            raise ValueError("La feuille est vide.")
        # Extrait les noms de colonnes
        self.header: List[str] = [str(col) for col in self._sheet[0]]
        # Vérifie que la feuille contient au moins les colonnes 'DESTINATAIRES' et 'DESTINATAIRES_COPIE'
        self.checkHeaderValidity(self.header)
        # Stocke les noms des autres colonnes dans self.fieldsName
        self.fieldNames = self.header[2:]

    def nextFieldValuesAsDict(self) -> Generator[dict[str, str], None, None]:
        """
        Retourne un itérateur sur les lignes de la 1ère feuille du fichier xlsx,
        en excluant la première ligne (en-tête) et les 2 premières colonnes.
        Chaque ligne est un dictionnaire avec les noms de colonnes comme clés
        et les valeurs sont converties en str si besoin.
        """
        for row in self._sheet[1:]:
            # Exclut les 2 premières colonnes
            rowDict = {self.header[i]: str(row[i]) for i in range(2, len(row))}
            yield rowDict

    def nextFieldsValueAsList(self) -> Generator[List[str], None, None]:
        """
        Retourne un itérateur sur les lignes de la 1ère feuille du fichier xlsx,
        en excluant la première ligne (en-tête) et les 2 premières colonnes.
        Chaque ligne est un dictionnaire avec les noms de colonnes comme clés
        et les valeurs sont converties en str si besoin.
        """
        for row in self._sheet[1:]:
            # Exclut les 2 premières colonnes
            rowList = [str(row[i]) for i in range(2, len(row))]
            yield rowList

    @staticmethod
    def checkHeaderValidity(header: List[str]) -> None:
        """
        :raise ValueError: si l'entête ne commence pas par les 2 colonnes 'DESTINATAIRES' et 'DESTINATAIRES_COPIE'
        """
        requiredFirstFields = ['DESTINATAIRES', 'DESTINATAIRES_COPIE']
        headerFirst2Cols = header[:2]
        if headerFirst2Cols != requiredFirstFields:
            raise ValueError(f"Le 2 première colonnes de l'entête doivent être {' et '.join(requiredFirstFields)}.")


def _main() -> None:
    """
    Fonction principale pour tester la classe MailingData.
    """
    try:
        # xlsxFile = Path('not_found.xlsx')
        # mailingData: MailingData = MailingData(Path(xlsxFile))

        # xlsxFile = Path('empty.xlsx')
        # mailingData: MailingData = MailingData(Path(xlsxFile))

        # xlsxFile = Path('invalid.xlsx')
        # mailingData: MailingData = MailingData(Path(xlsxFile))

        xlsxFile = Path('data/simple_data.xlsx')
        mailingData: MailingData = MailingData(Path(xlsxFile))

        print("Noms des colonnes :", mailingData.header)
        for row in mailingData.nextFieldValuesAsDict():
            print(row)

        for row in mailingData.nextFieldsValueAsList():
            print(row)

    except ValueError as e:
        print(f"Erreur : {e}")
    except FileNotFoundError as e:
        print(f"Erreur: fichier introuvable: {xlsxFile}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    _main()