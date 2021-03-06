SELECT class AS "Klasse", info AS "Info",
    Gewonnene_Spiele AS "Wins",
    Gespielte_Spiele AS "Plays",
    ROUND((CAST(Gewonnene_Spiele AS DOUBLE) * 100 /
           CAST(Gespielte_Spiele AS DOUBLE)), 2) AS "Gewinnrate (%)",
    Max_Ausfuerungszeit_in_Sek AS "Max Zeit (Sek)",
    Avg_Ausfuerungszeit_in_Sek AS "Avg Zeit (Sek)",
    (SELECT ROUND(AVG(execution), 4) FROM execution_times e
        JOIN players ssp ON ssp.id = e.player_id
        WHERE ssp.class = result.class
        AND execution < 60) AS "Avg Zeit oD (Sek)",
    ROUND((CAST(Anzahl_Deadline_nicht_ueberschritten AS DOUBLE) * 100 /
           CAST(Anzahl_Executions AS DOUBLE)), 2) AS "Deadline eingehalten (%)"
FROM (
    SELECT p.class, p.info,
        (SELECT COUNT(winner_id) FROM games g
            JOIN players ssp ON ssp.id = g.winner_id
            WHERE ssp.info = p.info
            AND ssp.class = p.class) as Gewonnene_Spiele,
        (SELECT COUNT(info) FROM participants pp
            JOIN players ssp ON ssp.id = pp.player_id
            WHERE ssp.info = p.info
            AND ssp.class = p.class) AS Gespielte_Spiele,
        (SELECT ROUND(MAX(execution), 4) FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info
            AND ssp.class = p.class) AS Max_Ausfuerungszeit_in_Sek,
        (SELECT ROUND(AVG(execution), 4) FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info
            AND ssp.class = p.class) AS Avg_Ausfuerungszeit_in_Sek,
        (SELECT COUNT(class) FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info
            AND ssp.class = p.class) AS Anzahl_Executions,
        (SELECT COUNT(class) FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.info = p.info
            AND ssp.class = p.class
            AND execution < 60) AS Anzahl_Deadline_nicht_ueberschritten
    FROM players p
    GROUP BY p.class, p.info
) AS result
ORDER BY "Gewinnrate (%)" DESC