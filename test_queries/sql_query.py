
QUERY = """SELECT distinct card.titolo collate "C"
                FROM media.mav_spes as spes
                left join media.mav_internal_card
                as card on (spes.id = card.id_spes) 
                WHERE spes.description = 'Federico II - Università dell''arte'
                order by card.titolo collate "C" """
