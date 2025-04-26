from pathlib import Path


class Mailer:
    """
    Classe pour gérer la génération d'un fichier HTML à partir de contenus formatés.
    """

    def __init__(self, htmlOutputFile: Path) -> None:
        """
        Initialise le Mailer avec un fichier de sortie HTML.
        et écrit l'entête HTML5 dans le fichier de sortie.
        """
        self.htmlOutputFile = open(htmlOutputFile, 'w', encoding='utf-8')
        self.htmlOutputFile.write(
"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Mailing</title>
</head>
<body>
"""
        )

    def __del__(self):
        """
        Destructeur qui ferme proprement le fichier de sortie HTML.
        """
        self._closeOutputFile()

    def addMailing(self, formattedContent: str) -> None:
        """
        Ajoute un contenu formaté dans le fichier HTML de sortie.
        :param formattedContent: Contenu HTML à ajouter.
        """
        self.htmlOutputFile.write(formattedContent + '<hr>\n')

    def _closeOutputFile(self) -> None:
        """
        Écrit les balises fermantes du HTML5 et ferme le fichier de sortie.
        """
        self.htmlOutputFile.write("</body>\n</html>\n")
        self.htmlOutputFile.close()

