from pathlib import Path
import re

class Template:
    def __init__(self, htmlFile: Path) -> None:
        # Ouvre le fichier HTML et lit son contenu
        with open(htmlFile, "r", encoding="utf-8") as f:
            self.content = f.read()

    def fillOut(self, fieldsValue: dict[str, str]) -> str:
        """
        Remplace les champs dans le contenu HTML par les valeurs fournies.
        """
        # Fonction interne pour remplacer les champs trouvés par leur valeur
        def replacer(match):
            field_name = match.group(1)
            # Retourne la valeur du champ si elle existe, sinon laisse le champ inchangé
            return fieldsValue.get(field_name, match.group(0))

        # Expression régulière pour trouver les champs à remplacer du type [---nom---]
        pattern = re.compile(r'\[---(.*?)---\]')

        # Remplace tous les champs trouvés dans le contenu
        return pattern.sub(replacer, self.content)
