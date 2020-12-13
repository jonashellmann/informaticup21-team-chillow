SELECT
    class as "Klasse",
    info as "Info",
    Gewonnene_Spiele as "Gewonnene Spiele",
    Gespielte_Spiele as "Gespielte Spiele",
    ROUND((CAST(Gewonnene_Spiele as double) * 100 /
           CAST(Gespielte_Spiele as double)), 2) as "Gewinnrate (%)",
    Max_Ausfuerungszeit_in_Sek as "Max Zeit (Sek)",
    Avg_Ausfuerungszeit_in_Sek as "Avg Zeit (Sek)",
    (SELECT ROUND(AVG(execution), 4)
        FROM execution_times e
        JOIN players ssp ON ssp.id = e.player_id
        WHERE ssp.class = result.class
        AND execution < 60) as "Avg Zeit oD (Sek)",
    ROUND((CAST(Anzahl_Deadline_nicht_ueberschritten as double) * 100 /
           CAST(Anzahl_Executions as double)), 2) as "Deadline eingehalten (%)"
FROM (
    SELECT
        class,
        info,
        (SELECT COUNT(winner_id)
            FROM games g
            JOIN players ssp ON ssp.id = g.winner_id
            WHERE ssp.info = p.info) as Gewonnene_Spiele,
        (SELECT COUNT(info)
            FROM participants pp
            JOIN players ssp ON ssp.id = pp.player_id
            WHERE ssp.info = p.info) as Gespielte_Spiele,
        (SELECT ROUND(MAX(execution), 4)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info) as Max_Ausfuerungszeit_in_Sek,
        (SELECT ROUND(AVG(execution), 4)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info) as Avg_Ausfuerungszeit_in_Sek,
        (SELECT COUNT(class)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info) as Anzahl_Executions,
        (SELECT COUNT(class)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info
            AND execution < 60) as Anzahl_Deadline_nicht_ueberschritten
    FROM players p
    Group BY p.info
) as result
ORDER BY "Gewinnrate in %" DESC