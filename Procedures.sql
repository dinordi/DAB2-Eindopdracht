DROP PROCEDURE IF EXISTS spVoegRaceToe;
DROP PROCEDURE IF EXISTS spVoegResultaatToe;
DROP PROCEDURE IF EXISTS spGetCoureurData;
DROP PROCEDURE IF EXISTS spGetTeamData;
DROP PROCEDURE IF EXISTS spGetCoureurJaar;
DROP PROCEDURE IF EXISTS spGetTeamJaar;

DELIMITER $$
CREATE PROCEDURE spVoegRaceToe(
    IN PTrack INT,
    IN PSeizoen INT,
    IN PDatum DATE,
    IN PRonde INT,
    IN PNaam VARCHAR(100)
)
    BEGIN
        INSERT INTO tblrace (IDTrack, intSeizoen, dtDatum, intRonde, strNaam)
        VALUES (PTrack, PSeizoen, PDatum, PRonde, PNaam);
    END$$

CREATE PROCEDURE spVoegResultaatToe(
    IN PRace INT,
    IN PCoureur INT,
    IN PPositie INT,
    IN PPolPos INT,
    IN PPunten INT
)
    BEGIN
        INSERT INTO tblracecoureur (IDRace, IDCoureur, intPositie, intPolPos, intPunten)
        VALUES (PRace, PCoureur, PPositie, PPolPos, PPunten);
    END$$

CREATE PROCEDURE spGetCoureurData(
    IN PDrivernaam VARCHAR(100),
    IN PJaar INT
)
    BEGIN
        SELECT DISTINCT coureurnaam, strland, teamnaam, intracenummer, blfoto FROM coureurdata 
        WHERE coureurnaam = PDrivernaam AND intLastyear >= PJaar AND intfirstyear <= PJaar;
    END$$

CREATE PROCEDURE spGetTeamData(
    IN PTeamnaam VARCHAR(100),
    IN PJaar INT
)
    BEGIN
        SELECT DISTINCT coureurnaam FROM coureurdata WHERE teamnaam = PTeamnaam AND PJaar BETWEEN intFirstYear AND intLastYear;
    END$$

CREATE PROCEDURE spGetCoureurJaar(
    IN PJaar INT
)
    BEGIN
        SELECT DISTINCT coureurnaam FROM coureurdata 
        WHERE PJaar BETWEEN intFirstyear AND intlastyear;
    END$$

CREATE PROCEDURE spGetTeamJaar(
    IN PJaar INT
)
    BEGIN
        SELECT DISTINCT teamnaam FROM coureurdata 
        WHERE PJaar BETWEEN intFirstyear AND intlastyear;
    END$$