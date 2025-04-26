# Mise en œuvre optimisée de rechercher/remplacer multiples dans du texte

from pathlib import Path
from Mailer import Mailer
from Template import Template
from MailingData import MailingData
import time


def test_fillOut__withReplace(htmlOutputFile: Path, template: Template, data: MailingData) -> None:
    start = time.perf_counter()
    mailer = Mailer(htmlOutputFile)

    for fieldValues in data.nextFieldValuesAsDict():
        # Remplace les variables dans le template par les valeurs de la ligne de données
        formattedContent = template.fillOut__withReplace(fieldValues)
        # Ajoute le contenu formaté au mailing
        mailer.addMailing(formattedContent)
    end = time.perf_counter()
    print(f"Durée d'exécution de test_fillOut__withReplace : {end - start:.4f} secondes")


def test_fillOut__withSegmentationAndDict(htmlOutputFile: Path, template: Template, data: MailingData) -> None:
    start = time.perf_counter()
    mailer = Mailer(htmlOutputFile)

    for fieldValues in data.nextFieldValuesAsDict():
        # Remplace les variables dans le template par les valeurs de la ligne de données
        formattedContent = template.fillOut__withSegmentationAndDict(fieldValues)
        # Ajoute le contenu formaté au mailing
        mailer.addMailing(formattedContent)
    end = time.perf_counter()
    print(f"Durée d'exécution de test_fillOut__withSegmentationAndDict : {end - start:.4f} secondes")


def test_fillOut__withSegmentationAndList(htmlOutputFile: Path, template: Template, data: MailingData) -> None:
    start = time.perf_counter()
    mailer = Mailer(htmlOutputFile)

    for fieldValues in data.nextFieldsValueAsList():
        # Remplace les variables dans le template par les valeurs de la ligne de données
        formattedContent = template.fillOut__withSegmentationAndList(fieldValues)
        # Ajoute le contenu formaté au mailing
        mailer.addMailing(formattedContent)
    end = time.perf_counter()
    print(f"Durée d'exécution de fillOut__withSegmentationAndList : {end - start:.4f} secondes")


def main() -> None:
    """
    Fonction principale pour exécuter le script de génération de mailing.
    Crée un objet Mailer, génère des contenus formatés et les ajoute au fichier HTML.
    """
    templateFile = Path('simple_template.html')
    dataFile = Path('simple_data.xlsx')
    # templateFile = Path('template_1381.html')
    # dataFile = Path('template_1381.xlsx')

    data = MailingData(dataFile)
    template = Template(htmlFile=templateFile, providedFieldNames=data.fieldNames)

    test_fillOut__withReplace(Path('output__withReplace.html'), template, data)
    test_fillOut__withSegmentationAndDict(Path('output__withSegmentationAndDict.html'), template, data)
    test_fillOut__withSegmentationAndList(Path('output__withSegmentationAndList.html'), template, data)


if __name__ == "__main__":
    main()
