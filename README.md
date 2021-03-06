# informatiCup 2021 - Team Chillow

<div>
    <a href="https://github.com/jonashellmann/informaticup21-team-chillow/actions?query=workflow%3A%22Python+Application%22">
        <img src="https://img.shields.io/github/workflow/status/jonashellmann/informaticup21-team-chillow/Python%20Application?label=GitHub%20Action" alt="Github Action Badge"/>
    </a>
    <img src="https://img.shields.io/tokei/lines/github/jonashellmann/informaticup21-team-chillow" alt="LoC Badge"/>
    <a href="https://github.com/jonashellmann/informaticup21-team-chillow/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/jonashellmann/informaticup21-team-chillow" alt="License Badge"/>
    </a>
    <a href="https://github.com/jonashellmann/informaticup21-team-chillow/commits/">
        <img src="https://img.shields.io/github/commit-activity/y/jonashellmann/informaticup21-team-chillow" alt="Commit Activity Badge"/>
    </a>
</div>

Dieses Repository beinhaltet den Beitrag von Team Chillow mit den Teammitgliedern
[@Florian3007](https://github.com/Florian3007) und [@jonashellmann](https://github.com/jonashellmann) von der
[Universität Oldenburg](https://uol.de) zum [informatiCup 2021](https://informaticup.github.io/).

Die gestellte Aufgabe mit dem Titel **spe_ed** kann in dem
[Repo zum informatiCup 2021](https://github.com/informatiCup/informatiCup2021) nachvollzogen werden.

<div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Carl_von_Ossietzky_Universit%C3%A4t_Oldenburg_logo.svg/1200px-Carl_von_Ossietzky_Universit%C3%A4t_Oldenburg_logo.svg.png" alt="Logo Uni Oldenburg" width="200" />
    <img src="https://informaticup.github.io/images/informaticup-logo.png" alt="Logo Uni Oldenburg" width="300" />
</div>

## Installation

Zur Verwendung muss das Projekt lokal heruntergeladen werden, entweder durch Klonen des Repositorys oder durch einen
Download als ZIP-Datei.
Das Projekt kann unter folgendem Link eingesehen werden:
[https://github.com/jonashellmann/informaticup21-team-chillow](https://github.com/jonashellmann/informaticup21-team-chillow)

### Docker

Falls Sie Docker auf Ihrem Rechner installiert haben, lässt sich für das Projekt aufgrund des vorhandenen `Dockerfile`s
mit folgendem Befehl ein neuer Container erstellen:

`docker build -t informaticup21-team-chillow .`

Dieser Container kann mit folgendem Befehl gestartet werden, bei dem die URL zum spe_ed-Server, der API-Key und die URL
zur Abfrage der Server-Zeit entsprechend angepasst werden müssen, wobei TIME_URL optional ist:

`docker run -e URL=SERVER_URL -e KEY=API_KEY -e TIME_URL=TIME_URL informaticup21-team-chillow`

In der Konsole des Docker-Containers lässt sich dann der Spiel-Verlauf nachvollziehen.

### Manuelle Installation

Neben der Docker-Installation kann das Projekt auch eigenständig gebaut werden.
Dafür ist erforderlich, dass neben Python in der Version >=3.8 auch [Poetry](https://python-poetry.org/) als Build-Tool
installiert ist.

Die erforderlichen Abhängigkeiten lassen sich anschließend mittels `poetry install` installieren.

Um ein Spiel mit einer simplen grafischen Oberfläche zu starten, in dem gegen die implementierten KIs gespielt werden
kann, genügt der Befehl `python ./main.py`.
Wenn gegen andere KI-Konstellationen gespielt werden soll, muss dies im `OfflineController` bei der Erstellung des
initialen Spiels manuell angepasst werden.

Um ein Online-Spiel der KI auf dem Server zu starten, müssen folgende Umgebungsvariablen verwendet werden, die im
Docker-Container automatisch gesetzt bzw. als Parameter übergeben werden:
- `URL=[SERVER_URL]`
- `KEY=[API_KEY]`
- `TIME_URL=[TIME_URL]` (optional)

Mittels dem Kommandozeilen-Parameter `--deactivate-pygame` kann entschieden werden, ob eine grafische Oberfläche benutzt
werden soll oder die Ausgabe wie im Docker-Container über die Konsole erfolgt.
Wenn die Python-Bibliothek PyGame nicht vorhanden ist, muss dieser Wert entweder auf `False` gesetzt werden oder
es ist eine manuelle Installation von PyGame bspw. mittels Pip notwendig.

## Benutzung

Wenn das Programm im Online-Modus gestartet wird, ist keine weitere Eingabe des Benutzers zu tätigen.
Sobald der Server das Spiel startet, kann entweder auf der Konsole oder in der grafischen Oberfläche der Spielverlauf
nachvollzogen werden.
Hier muss der Parameter `--play-online` auf `TRUE` gesetzt werden.

Bei einer Ausführung im Offline-Modus wird – je nach manueller Anpassung im `OfflineController` - auf eine
Eingabe von keinem, einem oder mehreren Spielern gewartet, bis die nächste Runde des Spiels gestartet wird.
Der Tabelle kann entnommen werden, mit welchen Eingaben eine Aktion ausgeführt werden kann.
Der Parameter `--play-online` muss für diesen Modus auf `FALSE` gesetzt werden.

<table>
    <tr>
        <th></th>
        <th>turn_right</th>
        <th>turn_left</th>
        <th>speed_up</th>
        <th>slow_down</th>
        <th>change_nothing</th>
    </tr>
    <tr>
        <th>Konsole</th>
        <td>r</td>
        <td>l</td>
        <td>u</td>
        <td>d</td>
        <td>n</td>
    </tr>
    <tr>
        <th>Grafische Oberfläche</th>
        <td>→</td>
        <td>←</td>
        <td>↑</td>
        <td>↓</td>
        <td>Leertaste</td>
    </tr>
</table>

Darüber hinaus ist eine Offline-Simulation mehrerer Spiele hintereinander möglich, in dem KIs mit zufälliger
Konfiguration auf einem Spielfeld mit zufälliger Größe gegeneinander antreten, um die bestmögliche KI zu ermitteln.
Dazu ist es notwendig, dass zusätzlich zum normalen Offline-Spiel den Parameter `--ai-eval-runs` auf eine Zahl größer
als Null gesetzt wird.
Mit dem Parameter `--ai-eval-db-path` kann statt dem Standardwert auch individuell der Pfad zu einer SQLite3-Datenbank
festgelegt werden.
Weiterhin steuert `--ai-eval-type`, welche Art der Evaluation ausgeführt werden soll.
Bei Wert 1 werden alle KIs betrachtet und jeweils maximal eine zufällige Konfiguration von einer Klasse zu einem
Spiel hinzugefügt.
Bei Wert 2 hingegen sind die nach unserer Evaluation aus dem ersten Lauf heraus ermittelten KI-Konfigurationen
hinterlegt und es werden nur aus diesen möglichen Konfigurationen KIs für ein Spiel ausgewählt.
Andere Werte als 1 und 2 sind für diesen Parameter ungültig.

## Contribution

Um das Projekt weiterzuentwickeln, können neue Issues geöffnet werden oder Pull Requests gegen den `main`-Branch zum
Review geöffnet werden. Durch das Öffnen eines Pull Requests wird automatisch eine Code- und Test-Analyse mittels
Github Actions durchgeführt.

## Lizenz

Das Projekt unterliegt der [MIT Lizenz](https://github.com/jonashellmann/informaticup21-team-chillow/blob/master/LICENSE).
