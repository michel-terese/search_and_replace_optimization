from pathlib import Path
import re
from typing import List


class Template:
    def __init__(self, htmlFile: Path, providedFieldNames: List[str]) -> None:
        """
        Initialise la classe Template avec le contenu d'un fichier HTML et les noms de champs fournis.
        Vérifie que tous les champs du modèle sont présents dans la liste fournie.
        :param htmlFile: Fichier contenant le modèle HTML avec des champs à remplacer de la forme [---nom---]
        :param providedFieldNames: Liste de champs qui seront utilisés pour remplir le modèle
        """
        # Lit le contenu du fichier HTML et le stocke dans l'attribut _content
        self._content = htmlFile.read_text(encoding='utf-8')

        # Compile l'expression régulière pour trouver les champs à remplacer du type [---nom---]
        self._fieldPattern = re.compile(r'\[---(.*?)---\]')

        # Extrait les noms des champs du contenu HTML
        self.templateFieldNames = self._fieldPattern.findall(self._content)

        # Vérifie que les champs du modèle sont présents dans providedFieldNames
        self._validateFieldNames(providedFieldNames)

        # Découpe le contenu HTML au niveau des champs pour créer une liste de segments de contenu.
        # Par exemple, si le contenu est "Bonjour [---nom---], comment ça va en ce [---jour---] ?",
        # les segments seront ['Bonjour ', '[---nom---]', ', comment ça va en ce ', '[---jour---]', ' ?']
        self._contentSegments = self._fieldPattern.split(self._content)

        # Indices des champs dans les segments de contenu
        # On commence à 1 et on saute deux en deux pour obtenir les indices des champs
        # Par exemple, pour le contenu ci-dessus, les indices seront [1, 3]
        self._contentSegmentsFieldIndices = [i for i in range(1, len(self._contentSegments), 2)]

        # Liste des indices des valeurs des champs à utiliser lors du remplissage par segmentation et liste
        self._contentSegmentsFieldValuesIndices = self._computeFieldValuesIndices(providedFieldNames)

    def fillOut__withRegex(self, fieldValues: dict[str, str]) -> str:
        """
        Remplace les champs dans le contenu HTML par les valeurs fournies avec la regex précompilée.
        """

        def replacer(match: re.Match) -> str:
            """
            Fonction interne pour remplacer les champs trouvés par leur valeur
            """
            field_name: str = match.group(1)
            # Retourne la valeur du champ si elle existe, sinon laisse le champ inchangé
            return fieldValues.get(field_name, match.group(0))

        # Remplace tous les champs trouvés dans le contenu
        return self._fieldPattern.sub(replacer, self._content)

    def fillOut__withReplace(self, fieldValues: dict[str, str]) -> str:
        """
        Remplace les champs dans le contenu HTML par les valeurs fournies, sans regex.
        """
        result = self._content
        for key, value in fieldValues.items():
            placeholder = f"[---{key}---]"
            result = result.replace(placeholder, value)
        return result

    def fillOut__withSegmentationAndDict(self, fieldValues: dict[str, str]) -> str:
        """
        Remplace les champs dans le contenu HTML par les valeurs fournies en utilisant le découpage
        du modèle en segments effectué dans le constructeur.
        """
        # Remplace la valeur des champs dans la liste des segments
        for fieldName, fieldIndex in zip(self.templateFieldNames, self._contentSegmentsFieldIndices):
            self._contentSegments[fieldIndex] = fieldValues[fieldName]
        return ''.join(self._contentSegments)

    def fillOut__withSegmentationAndList(self, fieldValues: List[str]) -> str:
        """
        Remplace les champs dans le contenu HTML par les valeurs fournies en utilisant le découpage
        du modèle en segments effectué dans le constructeur.
        """
        # Remplace la valeur des champs dans la liste des segments
        for fieldValueIndex, fieldIndex in zip(self._contentSegmentsFieldValuesIndices, self._contentSegmentsFieldIndices):
            self._contentSegments[fieldIndex] = fieldValues[fieldValueIndex]
        return ''.join(self._contentSegments)

    def _validateFieldNames(self, providedFieldNames: List[str]) -> None:
        """
        Vérifie que tous les champs du modèle sont présents dans la liste fournie.
        :param providedFieldNames: Liste des noms de champs à valider
        :raise ValueError: si tous les champs du modèle ne sont pas dans la liste providedFieldNames
        """
        # Vérifie que tous les champs du modèle sont présents dans la liste fournie
        missingFields = set(self.templateFieldNames) - set(providedFieldNames)
        if len(missingFields) > 0:
            raise ValueError(f"Les champs suivants sont manquants : {', '.join(missingFields)}")

    def _computeFieldValuesIndices(self, providedFieldNames: List[str]) -> List[int]:
        """
        Calcule les indices des valeurs des champs à utiliser lors du remplissage par segmentation et
        les stocke dans l'attribut _contentSegmentsFieldValuesIndices.
        :param providedFieldNames: Liste des noms de champs dans l'ordre dans lequel ils seront passés à fillOut__withSegmentationAndList()
        :return: Liste des indices des valeurs des champs
        """
        # Dictionnaire des indices des noms des champs tels qu'ils seront fournis à fillOut__withSegmentationAndList()
        fieldValuesIndices = {fieldName: i for i, fieldName in enumerate(providedFieldNames)}

        contentSegmentsFieldValuesIndices = []
        # Initialise la liste d'indices pour les valeurs des champs dans la liste des segments
        for segmentFieldName in self.templateFieldNames:
            # Trouve l'indice du champ dans le contenu
            fieldIndex = fieldValuesIndices[segmentFieldName]
            contentSegmentsFieldValuesIndices.append(fieldIndex)

        return contentSegmentsFieldValuesIndices

#=====================================================================================
# Tests de la classe Template
#=====================================================================================
import timeit

def _test_fillOut__withRegex(executionCount: int) -> None:
    """
    Test de la méthode fillOut__withRegex
    """
    # Exemple de dictionnaire de valeurs pour les champs
    fieldValues = {
        'CHAMP1': 'VALEUR CHAMP1',
        'CHAMP2': 'VALEUR CHAMP2',
        'CHAMP3': 'VALEUR CHAMP3'
    }

    template = Template(htmlFile=Path('simple_template.html'),
                        providedFieldNames=list(fieldValues.keys()))

    # Remplace les champs dans le contenu HTML par les valeurs fournies
    filledTemplate = template.fillOut__withRegex(fieldValues)
    print(filledTemplate)

    # Profilage de l'exécution
    executionTime = timeit.timeit(
        lambda: template.fillOut__withRegex(fieldValues),
        number=executionCount
    )
    executionCountStr = f"{executionCount:,}".replace(',', ' ')
    print(f"fillOut__withRegex: {executionTime:.6f} secondes pour {executionCountStr} exécutions")
    print('-' * 80)


def _test_fillOut__withReplace(executionCount: int) -> None:
    """
    Test de la méthode fillOut__withReplace
    """
    # Exemple de dictionnaire de valeurs pour les champs
    fieldValues = {
        'CHAMP1': 'VALEUR CHAMP1',
        'CHAMP2': 'VALEUR CHAMP2',
        'CHAMP3': 'VALEUR CHAMP3'
    }

    template = Template(htmlFile=Path('simple_template.html'),
                        providedFieldNames=list(fieldValues.keys()))

    # Remplace les champs dans le contenu HTML par les valeurs fournies
    filledTemplate = template.fillOut__withReplace(fieldValues)
    print(filledTemplate)

    # Profilage de l'exécution
    executionTime = timeit.timeit(
        lambda: template.fillOut__withReplace(fieldValues),
        number=executionCount
    )
    executionCountStr = f"{executionCount:,}".replace(',', ' ')
    print(f"fillOut__withReplace: {executionTime:.6f} secondes pour {executionCountStr} exécutions")
    print('-' * 80)


def _test_fillOut__withSegmentationAndDict(executionCount: int) -> None:
    """
    Test de la méthode fillOut__withSegmentationAndDict
    """
    # Exemple de dictionnaire de valeurs pour les champs
    fieldValues = {
        'CHAMP1': 'VALEUR CHAMP1',
        'CHAMP2': 'VALEUR CHAMP2',
        'CHAMP3': 'VALEUR CHAMP3'
    }

    template = Template(htmlFile=Path('simple_template.html'),
                        providedFieldNames=list(fieldValues.keys()))
    
    # Remplace les champs dans le contenu HTML par les valeurs fournies
    filledTemplate = template.fillOut__withSegmentationAndDict(fieldValues)
    print(filledTemplate)

    # Profilage de l'exécution
    executionTime = timeit.timeit(
        lambda: template.fillOut__withSegmentationAndDict(fieldValues),
        number=executionCount
    )
    executionCountStr = f"{executionCount:,}".replace(',', ' ')
    print(f"fillOut__withSegmentationAndDict: {executionTime:.6f} secondes pour {executionCountStr} exécutions")
    print('-' * 80)


def _test_fillOut__withSegmentationAndList(executionCount: int) -> None:
    """
    Test de la méthode fillOut__withSegmentationAndList
    """
    # Exemple de liste de noms de champs
    fieldNames = ['CHAMP1', 'CHAMP2', 'CHAMP3']
    # Exemple de liste de valeurs pour les champs
    fieldValues = ['VALEUR CHAMP1', 'VALEUR CHAMP2', 'VALEUR CHAMP3']

    template = Template(htmlFile=Path('simple_template.html'),
                        providedFieldNames=fieldNames)
    
    # Remplace les champs dans le contenu HTML par les valeurs fournies
    filledTemplate = template.fillOut__withSegmentationAndList(fieldValues)
    print(filledTemplate)

    # Profilage de l'exécution
    executionTime = timeit.timeit(
        lambda: template.fillOut__withSegmentationAndList(fieldValues),
        number=executionCount
    )
    executionCountStr = f"{executionCount:,}".replace(',', ' ')
    print(f"fillOut__withSegmentationAndList: {executionTime:.6f} secondes pour {executionCountStr} exécutions")
    print('-' * 80)


def _main():
    executionCount = 10000000  # Nombre d'exécutions pour le profilage

    # _test_fillOut__withRegex(executionCount)
    _test_fillOut__withReplace(executionCount)
    _test_fillOut__withSegmentationAndDict(executionCount)
    _test_fillOut__withSegmentationAndList(executionCount)


if __name__ == '__main__':
    _main()
