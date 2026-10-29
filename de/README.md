# Autonomes Fahren: KI-Sicherheit und Security – Deutsche Ausgabe

Diese Ausgabe enthält die sechs Kern-Notebooks des offenen Kurses [*Autonomous Driving: AI Safety and Security*](../README.md) in deutscher Sprache. Sie folgen einem durchgehenden Beispiel, dem **Notbremsassistenten (AEB)**, von der Einordnung in SAE-Stufen und Betriebsbereich (ODD) über Gefährdungsanalyse, SOTIF, TARA und KI-Sicherheit bis zur Freigabeentscheidung. Zielgruppe sind Studierende sowie Ingenieurinnen und Ingenieure bei OEMs und Zulieferern.

**Autor:** Milin Patel · Hochschule Kempten · MIT-Lizenz

## Übersetzte Notebooks

Empfohlene Reihenfolge; jedes Notebook verlinkt sein englisches Original sowie das vorherige und nächste Notebook dieser Ausgabe.

| # | Notebook (deutsch) | Inhalt | Englisches Original |
|---|---|---|---|
| 1 | [SAE-Automatisierungsstufen und Betriebsbereich (ODD)](01_Perception/01_sae_levels_and_odd.ipynb) | Rollen nach SAE J3016, ODD und seine Überwachung zur Laufzeit, Abgrenzung ISO 26262 / ISO 21448 / ISO/PAS 8800 | [01-01](../01_Perception/01_sae_levels_and_odd.ipynb) |
| 2 | [Gefährdungsanalyse und Risikobewertung (G&R, engl. HARA)](03_Functional_Safety_ISO26262/02_hara.ipynb) | Betrachtungseinheit, S/E/C, ASIL, Sicherheitsziele mit FTTI, ASIL-Dekomposition | [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb) |
| 3 | [ISO 21448: Sicherheit der Sollfunktion (SOTIF)](04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb) | Auslösende Bedingungen, funktionale Unzulänglichkeiten, Area 1–4, Akzeptanzkriterien und Validierungsziele | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb) |
| 4 | [Bedrohungsanalyse und Risikobewertung (TARA)](05_Cybersecurity_ISO21434/02_tara.ipynb) | Die sieben Schritte nach ISO/SAE 21434, Angriffspotenzial, CAL, Restrisiko, Safety-Security-Co-Engineering | [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb) |
| 5 | [KI-Sicherheitsnormen: ISO/PAS 8800 und verwandte Normen](06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb) | Normenlandschaft, Aufbau der ISO/PAS 8800, Datensatzanforderungen, Überwachung im Betrieb, KI-Verordnung der EU | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb) |
| 6 | [Abschlussprojekt: Fußgänger-AEB von der Anforderung bis zur Freigabe](08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb) | Wahrnehmungsanforderung, gemessen auf realen KITTI-Bildern; Kalibrierung, Conformal Prediction, TARA, Validierungsziel, GSN, Freigabe-Checkliste | [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb) |

Die Fachbegriffe sind über alle sechs Notebooks einheitlich übersetzt; das [Glossar](GLOSSAR.md) stellt sie den englischen Begriffen der Normen gegenüber.

## Nutzung

- **Im Browser:** Öffnen Sie ein Notebook und klicken Sie auf das Colab-Badge im Kopf. Das Kurs-Toolkit `avsafety` wird bei Bedarf automatisch installiert. Das Abschlussprojekt lädt KITTI-Bilder und vortrainierte Detektorgewichte aus dem Internet (einige Minuten auf CPU).
- **Lokal:** Klonen Sie das Repository, installieren Sie die Abhängigkeiten mit `pip install -r requirements.txt` und das Toolkit mit `pip install -e ".[data]"` und öffnen Sie die Notebooks aus dem Ordner `de/` mit Jupyter.
- **Code und Ausgaben bleiben englisch.** Der Programmcode jedes Notebooks ist byteweise identisch mit dem englischen Original. So lässt sich automatisch prüfen, dass beide Fassungen nicht auseinanderlaufen; Diagramme, Tabellen, Textausgaben und die Rückmeldungen der automatisch geprüften Übungen erscheinen deshalb auf Englisch. Übersetzt sind alle erklärenden Texte, Übungsaufgaben, Selbsttests und Musterlösungen.
- **Literatur** wird in der Originalsprache zitiert. Links auf Notebooks, die (noch) nicht übersetzt sind, führen zum englischen Kurs und sind mit „(engl.)“ gekennzeichnet.

## Der vollständige Kurs

Der englische Kurs umfasst acht Module mit allen Notebooks, Vorlagen (G&R, SOTIF-Analyse, TARA), interaktiven Werkzeugen und einem getesteten Toolkit:

- Kursübersicht im Repository: [README](../README.md)
- Website: https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/

## Für Mitwirkende

`python scripts/check_translations.py` prüft jedes Notebook in `de/` gegen sein englisches Original: identische Codezellen in gleicher Reihenfolge, gleiche Zahl der Markdown-Zellen, deutsches Kopf- und Fußformat, funktionierende relative Links. Ändert sich der Code des Originals, meldet die Prüfung die betroffene Zelle; übernehmen Sie dann die Änderung, passen Sie den Text an und führen Sie das Notebook mit `python scripts/execute_notebooks.py --write de/<Pfad>` erneut aus.
