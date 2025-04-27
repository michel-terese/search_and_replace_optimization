# Version finale de la classe Template sans les méthodes non optimales

from pathlib import Path
import re
from typing import List


class TemplateManager:
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

    def fillOut(self, fieldValues: List[str]) -> str:
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
def _main():
    # Exemple de liste de noms de champs
    fieldNames = ['CHAMP1', 'CHAMP2', 'CHAMP3']
    # Exemple de liste de valeurs pour les champs
    fieldValues = ['VALEUR CHAMP1', 'VALEUR CHAMP2', 'VALEUR CHAMP3']

    templateManager = TemplateManager(htmlFile=Path('simple_template.html'),
                                      providedFieldNames=fieldNames)

    # Remplace les champs dans le contenu HTML par les valeurs fournies
    filledTemplate = templateManager.fillOut(fieldValues)
    print(filledTemplate)


if __name__ == '__main__':
    _main()
