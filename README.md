# informatiCup 2021 - Team Chillow

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

Zur Verwendung dieses Projektes muss es lokal heruntergeladen werden, entweder durch Klonen des Repositorys oder durch
einen Download als ZIP-Datei.
Das Projekt kann unter folgendem Link eingesehen werden:
[https://github.com/jonashellmann/informaticup21-team-chillow](https://github.com/jonashellmann/informaticup21-team-chillow)

### Docker

Falls Sie Docker auf Ihrem Rechner installiert haben, lässt sich für das Projekt aufgrund des vorhandenen `Dockerfile`s
mit folgendem Befehl ein neuer Container erstellen:

`docker build -t informaticup21-team-chillow .`

Dieser Container kann mit folgendem Befehl gestartet werden, wobei die URL zum spe_ed-Server und der API-Key
entsprechend angepasst werden müssen:

`docker run -e URL=SERVER_URL -e KEY=API_KEY informaticup21-team-chillow`

In der Konsole des Docker-Containers lässt sich dann der Spiel-Verlauf nachvollziehen.

### Manuelle Installation

Neben der Docker-Installation kann das Projekt auch eigenständig gebaut werden.
Dafür ist erforderlich, dass neben Python in der Version 3.8 auch [Poetry](https://python-poetry.org/) als Build-Tool
installiert ist.

Die erforderlichen Abhängigkeiten lassen sich anschließend mittels `poetry install` installieren.

Um ein Spiel mit einer simplen grafischen Oberfläche zu starten, in dem gegen die implementierte KI gespielt werden
kann, genügt der Befehl `python ./main.py`.
Wenn gegen eine andere KI gespielt werden soll als die, für die wir uns am Ende entschieden haben, muss dies im
`OfflineController` bei der Erstellung des initialen Spiels manuell angepasst werden.

Um ein Online-Spiel der KI auf dem Server zu starten, müssen folgende Umgebungsvariablen verwendet werden, die im
Docker-Container automatisch gesetzt bzw. als Parameter übergeben werden:
- `PLAY_ONLINE=TRUE`
- `URL=[SERVER_URL]`
- `KEY=[API_KEY]`

Mittels der Umgebungsvariable `DEACTIVATE_PYGAME` kann entschieden werden, ob eine grafische Oberfläche benutzt werden
soll oder die Ausgabe wie im Docker-Container über die Konsole erfolgt.

## Benutzung

Wenn das Programm im Online-Modus gestartet wird, ist keine weitere Eingabe des Benutzers zu tätigen.
Sobald der Server das Spiel startet, kann entweder auf der Konsole oder in der grafischen Oberfläche der Spielverlauf
nachvollzogen werden.

Bei einer Ausführung im Offline-Modus wird - je nach manueller Anpassung im `OfflineController` - auf eine
Eingabe von einem oder mehreren Spielern gewartet, bis die nächste Runde des Spiels gestartet wird.
Der Tabelle kann entnommen werden, mit welchen Eingaben eine Aktion ausgeführt werden kann.

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

## Contribution

Um das Projekt weiterzuentwickeln, können neue Issues geöffnet werden oder Pull Requests gegen den `main`-Branch zum
Review geöffnet werden. Durch das Öffnen eines Pull Requests wird automatisch eine Code- und Test-Analyse mittels
Github Actions durchgeführt.

## Lizenz

Das Projekt unterliegt der [MIT Lizenz](https://github.com/jonashellmann/informaticup21-team-chillow/blob/master/LICENSE).