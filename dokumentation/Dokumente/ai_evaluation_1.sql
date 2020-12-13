SELECT
    class as Klasse,
    Gewonnene_Spiele as "Gewonnene Spiele",
    Gespielte_Spiele as "Gespielte Spiele",
    ROUND((CAST(Gewonnene_Spiele as double) * 100 /
           CAST(Gespielte_Spiele as double)), 2) as "Gewinnrate (%)",
    Max_Ausfuerungszeit_in_Sek as "Max Zeit (Sek)",
    Avg_Ausfuerungszeit_in_Sek as "Avg Zeit (Sek)",
    Avg_Ausfuerungszeit_in_Sek_ohne_deadline "Avg Zeit oD (Sek)",
    ROUND((CAST(Anzahl_Deadline_nicht_ueberschritten as double) * 100 /
           CAST(Anzahl_Executions as double)), 2) as "Deadline eingehalten (%)"
FROM (
    SELECT
        class,
        (SELECT COUNT(winner_id)
            FROM games g
            JOIN players ssp ON ssp.id = g.winner_id
            WHERE ssp.class = p.class) as Gewonnene_Spiele,
        (SELECT COUNT(class)
            FROM participants pp
            JOIN players ssp ON ssp.id = pp.player_id
            WHERE ssp.class = p.class) as Gespielte_Spiele,
        (SELECT ROUND(MAX(execution), 4)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.class = p.class) as Max_Ausfuerungszeit_in_Sek,
        (SELECT ROUND(AVG(execution), 4)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.class = p.class) as Avg_Ausfuerungszeit_in_Sek,
        (SELECT ROUND(AVG(execution), 4)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.class = p.class AND execution < 60) as Avg_Ausfuerungszeit_in_Sek_ohne_deadline,
        (SELECT COUNT(class)
            FROM execution_times e
            JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.class = p.class) as Anzahl_Executions,
        (SELECT COUNT(class)
            FROM execution_times e JOIN players ssp ON ssp.id = e.player_id
            WHERE ssp.class = p.class
            AND execution < 60) as Anzahl_Deadline_nicht_ueberschritten
    FROM players p
    Group BY p.class
) as result
ORDER BY "Gewinnrate in %" DESC