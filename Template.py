from pathlib import Path
import re
from typing import List


class Template:
    def __init__(self, htmlFile: Path) -> None:
        # Lit le contenu du fichier HTML et le stocke dans l'attribut _content
        self._content = htmlFile.read_text(encoding='utf-8')
        # Compile l'expression régulière pour trouver les champs à remplacer du type [---nom---]
        self.fieldPattern = re.compile(r'\[---(.*?)---\]')
        # Extrait les noms de champs du contenu HTML
        self.fieldNamesSet = set(self.fieldPattern.findall(self._content))

    def validateFieldNames(self, fieldNames: List[str]) -> None:
        """
        Vérifie que tous les champs du modèle sont présents dans la liste fournie.
        :param fieldNames: Liste des noms de champs à valider
        :raise ValueError: si tous les champs du modèle ne sont pas dans la liste fieldNames
        """
        # Vérifie que tous les champs du modèle sont présents dans la liste fournie
        missingFields = self.fieldNamesSet - set(fieldNames)
        if len(missingFields) > 0:
            raise ValueError(f"Les champs suivants sont manquants : {', '.join(missingFields)}")

    def fillOut__withRegex(self, fieldsValue: dict[str, str]) -> str:
        """
        Remplace les champs dans le contenu HTML par les valeurs fournies avec la regex précompilée.
        """

        def replacer(match: re.Match) -> str:
            """
            Fonction interne pour remplacer les champs trouvés par leur valeur
            """
            field_name: str = match.group(1)
            # Retourne la valeur du champ si elle existe, sinon laisse le champ inchangé
            return fieldsValue.get(field_name, match.group(0))

        # Remplace tous les champs trouvés dans le contenu
        return self.fieldPattern.sub(replacer, self._content)

    def fillOut__withoutRegex(self, fieldsValue: dict[str, str]) -> str:
        """
        Remplace les champs dans le contenu HTML par les valeurs fournies, sans regex.
        """
        result = self._content
        for key, value in fieldsValue.items():
            placeholder = f"[---{key}---]"
            result = result.replace(placeholder, value)
        return result


def _main():
    import timeit

    # Exemple d'utilisation de la classe Template
    template = Template(Path('simple_template.html'))
    fieldsValue = {
        'CHAMP1': 'VALEUR CHAMP1',
        'CHAMP2': 'VALEUR CHAMP2',
        'CHAMP3': 'VALEUR CHAMP3'
    }

    # Vérifie que les champs du modèle sont présents dans le dictionnaire fieldsValue
    template.validateFieldNames(list(fieldsValue.keys()))

    executionCount = 1 #0000000
    # # Mesure du temps pour fillOut__withRegex
    # executionTime = timeit.timeit(
    #     lambda: template.fillOut__withRegex(fieldsValue),
    #     number=executionCount
    # )
    # print(f"fillOut__withRegex : {executionTime:.6f} secondes pour 10 000 exécutions")

    # Mesure du temps pour fillOut__withoutRegex
    executionTime = timeit.timeit(
        lambda: template.fillOut__withoutRegex(fieldsValue),
        number=executionCount
    )
    print(f"fillOut__withoutRegex : {executionTime:.6f} secondes pour 10 000 exécutions")

if __name__ == '__main__':
    _main()