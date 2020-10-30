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

### Docker

Falls Sie Docker auf Ihrem Rechner installiert haben, lässt sich für das Projekt aufgrund des vorhandenen `Dockerfile`s
mit folgendem Befehl ein neuer Container erstellen:

`docker build -t informaticup21-team-chillow .`

Dieser Container kann dann unter der Angabe der URL zum spe_ed-Server und dem API-Key gestartet werden:

`docker run -e URL=[SERVER_URL] -e KEY=[API_KEY] informaticup21-team-chillow`

In der Konsole des Docker-Containers lässt sich dann der Spiel-Verlauf nachvollziehen.

### Manuelle Installation

Neben der Docker-Installation kann das Projekt auch eigenständig gebaut werden.
Dafür ist erforderlich, dass sowohl Python in Version 3.8 [Poetry](https://python-poetry.org/) installiert ist, was
als Build-Tool eingesetzt wird.

Die erforderlichen Abhängigkeiten lassen sich anschließend mittels `poetry install` installieren.

Um ein Spiel zu starten, in dem in einer simplen grafischen Oberfläche gegen die implementierte KI gespielt werden kann,
genügt `python ./main.py`.

Um ein Online-Spiel der KI auf dem Server zu starten, müssen folgende Umgebungsvariablen verwendet werden, die im
Docker-Container automatisch gesetzt bzw. als Parameter übergeben werden:
- `PLAY_ONLINE=TRUE`
- `URL=[SERVER_URL]`
- `KEY=[API_KEY]`

Mittels der Umgebungsvariable `DEACTIVATE_PYGAME` kann entschieden werden, ob eine grafische Oberfläche benutzt werden
soll oder die Ausgabe wie im Docker-Container über die Konsole erfolgt.

## Contribution

Um das Projekt weiterzuentwickeln, können neue Issues geöffnet werden oder Pull Requests gegen den `main`-Branch zum
Review geöffnet werden. Durch das Öffnen eines Pull Requests wird automatisch eine Code- und Test-Analyse mittels
Github Actions durchgeführt.

## Lizenz

Das Projekt unterliegt der [MIT Lizenz](https://github.com/jonashellmann/informaticup21-team-chillow/blob/master/LICENSE).