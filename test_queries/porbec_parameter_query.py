TEST_OWL_FILE = "ontology_folder\def_porbec.owl"

dict_sql_queries_for_parameters = {"spes": """SELECT spes.description collate "C" FROM media.mav_spes as spes ORDER BY spes.description collate "C" """ , 
                               "collection": """SELECT collection.title collate "C"  FROM media.mav_collection as collection ORDER BY collection.title collate "C" """ , 
                               "card": """SELECT card.titolo collate "C"  FROM media.mav_internal_card as card ORDER BY card.titolo collate "C" """ , 
                               "author": """SELECT author.nome collate "C"  FROM media.mav_internal_autore as author ORDER BY author.nome collate "C" """ , 
                               "materia": """SELECT distinct materia_tecnica.materia collate "C" FROM media.mav_materia_tecnica as materia_tecnica WHERE materia_tecnica.materia!='' ORDER BY materia_tecnica.materia collate "C" """,
                               "tecnica": """SELECT distinct materia_tecnica.tecnica collate "C" FROM media.mav_materia_tecnica as materia_tecnica  WHERE materia_tecnica.tecnica!='' ORDER BY materia_tecnica.tecnica collate "C" """,
                               "materia_tecnica": """SELECT materia_tecnica.materia collate "C", materia_tecnica.tecnica FROM media.mav_materia_tecnica as materia_tecnica WHERE materia_tecnica.materia!='' or materia_tecnica.tecnica!='' ORDER BY materia_tecnica.materia collate "C" """}

queries = {"spes": [{"name_query": "What are the contacts of a SPES X?", 
"sql_query" : """SELECT contatti.active_fruition, contatti.address,
	   contatti.elenco_sponsor, contatti.email, contatti.fax, contatti.header_light, 
	   contatti.is_freeze, contatti.last_edit, contatti.latitude, contatti.link_museo, 
	   contatti.link_official_site, contatti.link_visita_virtuale, 
	   contatti.longitude, contatti.nome_museo, contatti.nomi_curatori, 
	   contatti.numero_pagine_pdf, contatti.numero_visite, contatti.orari,
	   contatti.path_video_museo, contatti.pdf_path, contatti.pec, contatti.telephone
FROM media.mav_spes as spes left 
join media.mav_contatti as contatti 
on (spes.id = contatti.id) WHERE spes.description = '{}' """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT ?fruition ?address 
	   ?elenco_sponsor ?email ?fax ?header_light 
	   ?is_freeze ?last_edit ?latitude ?link_museo 
	   ?link_official_site ?link_visita_virtuale 
	   ?longitude ?nome_museo ?nomi_curatori 
	   ?numero_pagine_pdf ?numero_visite ?orari
	   ?path_video_museo ?pdf_path ?pec ?telephone
WHERE {{?spes porbec:description_of_mav_spes "{}"^^xsd:string. 
       ?contatti porbec:mav_contatti_has_a_mav_spes ?spes.
 	OPTIONAL{{?contatti porbec:active_fruition_of_mav_contatti ?fruition.}}
	OPTIONAL{{?contatti porbec:address_of_mav_contatti ?address.}}
	OPTIONAL{{?contatti porbec:elenco_sponsor_of_mav_contatti ?elenco_sponsor.}}
	OPTIONAL{{?contatti porbec:email_of_mav_contatti ?email.}}
	OPTIONAL{{?contatti porbec:fax_of_mav_contatti ?fax.}}  
    OPTIONAL{{?contatti porbec:header_light_of_mav_contatti ?header_light.}}  
    OPTIONAL{{?contatti porbec:is_freeze_of_mav_contatti ?is_freeze.}}
    OPTIONAL{{?contatti porbec:last_edit_of_mav_contatti ?last_edit.}}  
    OPTIONAL{{?contatti porbec:latitude_of_mav_contatti ?latitude.}} 
    OPTIONAL{{?contatti porbec:link_museo_of_mav_contatti ?link_museo.}}  
    OPTIONAL{{?contatti porbec:link_official_site_of_mav_contatti ?link_official_site.}}
    OPTIONAL{{?contatti porbec:link_visita_virtuale_of_mav_contatti ?link_visita_virtuale.}}  
    OPTIONAL{{?contatti porbec:longitude_of_mav_contatti ?longitude.}}
    OPTIONAL{{?contatti porbec:nome_museo_of_mav_contatti ?nome_museo.}}  
    OPTIONAL{{?contatti porbec:nomi_curatori_of_mav_contatti ?nomi_curatori.}}  
    OPTIONAL{{?contatti porbec:numero_pagine_pdf_of_mav_contatti ?numero_pagine_pdf.}}
    OPTIONAL{{?contatti porbec:numero_visite_of_mav_contatti ?numero_visite.}} 
    OPTIONAL{{?contatti porbec:orari_of_mav_contatti ?orari.}} 
    OPTIONAL{{?contatti porbec:path_video_museo_of_mav_contatti ?path_video_museo.}}  
    OPTIONAL{{?contatti porbec:pdf_path_of_mav_contatti ?pdf_path.}}
    OPTIONAL{{?contatti porbec:pec_of_mav_contatti ?pec.}} 
    OPTIONAL{{?contatti porbec:telephone_of_mav_contatti ?telephone.}}
    OPTIONAL{{?spes porbec:description_of_mav_spes ?spes_description.}}                       
}}"""
}, {"name_query": "What are the contacts descriptions of a SPES X?", 
"sql_query" : """SELECT description.text_description, description.language
            FROM media.mav_spes as spes
            left join media.mav_contatti
            as contatti on (spes.id = contatti.id) 
            left join media.mav_description
            as description on (contatti.id = description.id_contact)
            WHERE spes.description = '{}'
            ORDER BY description.language ASC""",
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT ?text_description ?language 
WHERE {{?spes porbec:description_of_mav_spes "{}"^^xsd:string.
       ?contatti porbec:mav_contatti_has_a_mav_spes ?spes.
       ?description porbec:mav_description_has_a_mav_contatti ?contatti
       OPTIONAL{{?description porbec:text_description_of_mav_description ?text_description.}}
       OPTIONAL{{?description porbec:language_of_mav_description ?language.}}
       OPTIONAL{{?spes porbec:description_of_mav_spes ?spes_description.}}
       
}}ORDER BY ASC(?language)"""
}, {"name_query": "What are the works in a SPES X?", 
"sql_query" : """SELECT distinct card.titolo collate "C"
                FROM media.mav_spes as spes
                left join media.mav_internal_card
                as card on (spes.id = card.id_spes) 
                WHERE spes.description = '{}'
                order by card.titolo collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: 
<http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT DISTINCT ?titolo
WHERE {{?spes porbec:description_of_mav_spes "{}"^^xsd:string.
?card porbec:mav_internal_card_has_a_mav_spes ?spes.
?description porbec:mav_description_has_a_mav_contatti ?contatti.
OPTIONAL{{
     ?card porbec:titolo_of_mav_internal_card ?titolo.
    }}
}} order by ?titolo"""
}, {"name_query": "What are the authors in a SPES X?", 
"sql_query" : """SELECT distinct autore.nome collate "C"
                FROM media.mav_spes as spes
                left join media.mav_internal_card
                as card on (spes.id = card.id_spes) 
                left join media.mav_card_internal_autore
                as card_autore on (card.id = card_autore.id_card)
                left join media.mav_internal_autore
                as autore on (card_autore.id_internal_autore = autore.id)
                WHERE spes.description = '{}'
                and autore.nome != 'null'
                order by autore.nome collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT DISTINCT ?nome
WHERE {{?spes porbec:description_of_mav_spes "{}"^^xsd:string.
       ?card porbec:mav_internal_card_has_a_mav_spes ?spes.
       ?card porbec:mav_card_internal_autore ?autore
       OPTIONAL{{?autore porbec:nome_of_mav_internal_autore ?nome.}}
}} order by ?nome"""
}, {"name_query": "What are the collections in a SPES X?", 
                    "sql_query" : """SELECT  coll.title collate "C"
                    FROM media.mav_spes as spes
                    left join media.mav_collection as coll
                    on (spes.id = coll.id_spes)
                    WHERE spes.description = '{}'
                    order by coll.title collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT DISTINCT ?collection_title
WHERE {{?spes porbec:description_of_mav_spes "{}"^^xsd:string.
      ?collection porbec:mav_collection_has_a_mav_spes ?spes
      OPTIONAL{{?collection porbec:title_of_mav_collection ?collection_title}}
}} order by ?collection_title"""
}
], "collection": [
    {"name_query": "What work are parts of the collection X?", 
"sql_query" : """SELECT DISTINCT card.titolo collate "C"
                FROM media.mav_collection as collection
	            left join media.mav_artworks_collection
	            as artwork on (collection.id = artwork.id_collection) 
	            left join media.mav_internal_card as card
	            on (artwork.id_card = card.id)
                WHERE collection.title = '{}'
                order by card.titolo collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT DISTINCT ?titolo
WHERE {{?collection porbec:title_of_mav_collection "{}"^^xsd:string.
        ?coll_art porbec:mav_artworks_collection_has_a_mav_collection ?collection.
        ?coll_art porbec:mav_artworks_collection_has_a_mav_internal_card ?card.
        OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo.}}
}} order by ?titolo"""
}, {"name_query": "What is the SPES in which there is the collection X?", 
"sql_query" : """SELECT spes.description collate "C"
                FROM media.mav_spes as spes
                left join media.mav_collection as coll
                on (spes.id = coll.id_spes)
                WHERE coll.title = '{}'
                order by spes.description collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT DISTINCT ?spes_description
WHERE {{?collection porbec:title_of_mav_collection "{}"^^xsd:string.
	   ?collection porbec:mav_collection_has_a_mav_spes ?spes.
	   OPTIONAL{{?spes porbec:description_of_mav_spes ?spes_description.}}
}} order by ?spes_description"""
}, 
{"name_query": "What are the authors of the works in a collection X?", 
"sql_query" : """SELECT distinct autore.nome collate "C" 
                FROM media.mav_collection as collection
                left join media.mav_artworks_collection
                as art_coll on 
                (collection.id = art_coll.id_collection) 
                left join media.mav_internal_card
                as card on (card.id = art_coll.id_card)
                left join media.mav_card_internal_autore
                as card_autore on 
                (card_autore.id_card = art_coll.id_card)
                left join media.mav_internal_autore
                as autore on 
                (autore.id = card_autore.id_internal_autore)
                WHERE collection.title = '{}'
                and autore.nome != 'null'
                order by autore.nome collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: 
<http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT DISTINCT ?nome
WHERE {{?collection porbec:title_of_mav_collection "{}"^^xsd:string.
?art_coll porbec:mav_artworks_collection_has_a_mav_collection ?collection.
?art_coll porbec:mav_artworks_collection_has_a_mav_internal_card ?card.
?card porbec:mav_card_internal_autore ?autore.
OPTIONAL{{
    ?autore porbec:nome_of_mav_internal_autore ?nome.
    }}
}} order by ?nome"""

}], "card": [{"name_query": "What are the author and the period of creation of the work X?", 
"sql_query" : """SELECT distinct author.nome collate "C", card.cronologia collate "C"
                FROM ((media.mav_internal_card as card
                left join media.mav_card_internal_autore
                as card_author on (card.id = card_author.id_card)) 
                left join media.mav_internal_autore as author
                on (card_author.id_internal_autore = author.id))
                WHERE card.titolo = '{}' 
                order by author.nome collate "C", card.cronologia collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT distinct ?nome_autore ?cronologia
WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
	   OPTIONAL{{?card porbec:mav_card_internal_autore ?autore.
                 ?autore porbec:nome_of_mav_internal_autore ?nome_autore.}}
       OPTIONAL{{?card porbec:cronologia_of_mav_internal_card ?cronologia.}}
	   	
}} order by ?nome_autore ?cronologia"""
}, {"name_query": "What are the bibliographical references concerning a work X?", 
"sql_query" : """SELECT card.titolo collate "C", card.note collate "C"
                FROM media.mav_internal_card as card
                WHERE card.titolo = '{}'
                order by card.titolo collate "C",  card.note collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT ?titolo ?note
WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
        OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo.}}
	    OPTIONAL{{?card porbec:note_of_mav_internal_card ?note.}}
       }}
       order by ?note"""
}, {"name_query": "What are the collections of a work X?", 
"sql_query" : """SELECT  card.titolo collate "C", coll.title collate "C"
                FROM ((media.mav_internal_card as card
                left join media.mav_artworks_collection
                as art_coll on (card.id = art_coll.id_card)) 
                left join media.mav_collection as coll
                on (art_coll.id_collection = coll.id))
                WHERE card.titolo = '{}'
                order by coll.title collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT ?titolo ?title
WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
       ?card porbec:titolo_of_mav_internal_card ?titolo.
	   OPTIONAL{{?art_coll porbec:mav_artworks_collection_has_a_mav_internal_card ?card. 
	   ?art_coll porbec:mav_artworks_collection_has_a_mav_collection ?coll.
	   ?coll porbec:title_of_mav_collection ?title.}}
	   }}
    order by (!bound(?title)) ?title"""
}, {"name_query": "What are the materials and techniques of a work X?", 
"sql_query" : """SELECT  card.titolo, mattec.materia, mattec.tecnica
    FROM ((media.mav_internal_card as card
    left join media.mav_internal_card_materia_tecnica
    as card_mattec on (card.id = card_mattec.id_card)) 
    left join media.mav_materia_tecnica as mattec
    on (card_mattec.id_internal_materia_tecnica = mattec.id))
    WHERE card.titolo = '{}' and (mattec.materia!='null' and mattec.tecnica!='null')
    order by card.titolo collate "C", mattec.materia collate "C", mattec.tecnica collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
    SELECT ?titolo ?materia ?tecnica
    WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
                ?card porbec:mav_internal_card_materia_tecnica ?mattec.
                OPTIONAL{{?mattec porbec:materia_of_mav_materia_tecnica ?materia.}}
                OPTIONAL{{?mattec porbec:tecnica_of_mav_materia_tecnica ?tecnica.}}
                ?card porbec:titolo_of_mav_internal_card ?titolo.}}
    ORDER BY ?titolo ?materia ?tecnica"""
}, {"name_query": "When was realized the work X?", 
"sql_query" : """SELECT card.titolo collate "C", card.cronologia collate "C"
                FROM media.mav_internal_card as card
                WHERE card.titolo = 'Gesù nel tempio'
                order by card.titolo collate "C", card.cronologia collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT ?titolo ?cronologia
            WHERE {{?card porbec:titolo_of_mav_internal_card "Gesù nel tempio"^^xsd:string.
            OPTIONAL{{?card porbec:cronologia_of_mav_internal_card ?cronologia.}}
            OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo.}}
            }} order by ?titolo ?cronologia"""
}, {"name_query": "What is the location of the signature of the work X?", 
"sql_query" : """SELECT card.titolo, card.firma
            FROM media.mav_internal_card as card
            WHERE card.titolo = '{}'
            order by case when (card.firma='' or card.firma=' ') then 1 else 0 end,  card.titolo collate "C", card.firma collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
                SELECT ?titolo ?firma
                WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
                    OPTIONAL{{?card porbec:firma_of_mav_internal_card ?firma.}}
                    OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo}}
                }} order by (!bound(?firma)) ?titolo ?firma"""
}, {"name_query": "What are the dimensions of a work X?", 
"sql_query" : """SELECT card.titolo, card.larghezza, 
            card.altezza, card.profondita, card.diametro
            FROM media.mav_internal_card as card
            WHERE card.titolo = '{}'
            order by card.titolo collate "C", card.larghezza, 
            card.altezza, card.profondita, card.diametro""",
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT ?titolo ?larghezza ?altezza ?profondità ?diametro
            WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
                OPTIONAL{{?card porbec:larghezza_of_mav_internal_card ?larghezza.}}
                OPTIONAL{{?card porbec:altezza_of_mav_internal_card ?altezza.}}
                OPTIONAL{{?card porbec:profondita_of_mav_internal_card ?profondità.}}
                OPTIONAL{{?card porbec:diametro_of_mav_internal_card ?diametro.}}
                OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo}}
            }} order by (!bound(?larghezza)) (!bound(?altezza)) ?titolo ?larghezza ?altezza ?profondità ?diametro"""
}, {"name_query": "What are the tales of a work X?", 
"sql_query" : """SELECT card.titolo, racconto.descrizione, racconto.lingua
            FROM media.mav_internal_card as card
            left join media.mav_internal_racconto
            as racconto on (card.id = racconto.id_card) 
            WHERE card.titolo = '{}'
            order by racconto.descrizione collate "C", racconto.lingua collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
                SELECT ?titolo ?descrizione ?lingua
                WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
                        ?racconto porbec:mav_internal_racconto_has_a_mav_internal_card ?card
                        OPTIONAL{{?racconto porbec:descrizione_of_mav_internal_racconto ?descrizione.}}
                        OPTIONAL{{?racconto porbec:lingua_of_mav_internal_racconto ?lingua.}}
                        OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo}}
                }} order by ?descrizione ?lingua"""
}, {"name_query": "What are the abstracts of a work X?", 
"sql_query" : """SELECT abstract.descrizione, abstract.lingua
            FROM media.mav_internal_card as card
            left join media.mav_internal_abstract
            as abstract on (card.id = abstract.id_card) 
            WHERE card.titolo = '{}' and (abstract.descrizione!='' or abstract.lingua!='')
            order by abstract.descrizione collate "C", abstract.lingua collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
                SELECT ?descrizione ?lingua
                WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
                    OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo.}}
                    ?abstract porbec:mav_internal_abstract_has_a_mav_internal_card ?card.
                    OPTIONAL{{?abstract porbec:descrizione_of_mav_internal_abstract ?descrizione.}}
                    OPTIONAL{{?abstract porbec:lingua_of_mav_internal_abstract ?lingua.}}
                    
                }} order by ?descrizione ?lingua"""
}, {"name_query": "In which SPES is a work?", 
"sql_query" : """SELECT card.titolo, spes.description
                FROM media.mav_spes as spes
                left join media.mav_internal_card as card
                on (spes.id = card.id_spes)
                WHERE card.titolo = '{}'
                order by card.titolo collate "C", spes.description collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
                SELECT ?card_titolo ?spes_description
                WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
                    ?card porbec:mav_internal_card_has_a_mav_spes ?spes.
                    OPTIONAL{{?spes porbec:description_of_mav_spes ?spes_description.}}
                    OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?card_titolo.}}
                }} order by ?card_titolo ?spes_description"""
}, {"name_query": "In which Collections is a work?", 
"sql_query" : """SELECT distinct coll.title collate "C"
                FROM media.mav_collection as coll
                left join media.mav_artworks_collection as art_coll
                on (coll.id = art_coll.id_collection)
                left join media.mav_internal_card as card
                on (card.id = art_coll.id_card)
                WHERE card.titolo = '{}'
                order by coll.title collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
                SELECT DISTINCT ?collection_title
                WHERE {{?card porbec:titolo_of_mav_internal_card "{}"^^xsd:string.
                    ?art_coll porbec:mav_artworks_collection_has_a_mav_collection ?collection.
                    ?art_coll porbec:mav_artworks_collection_has_a_mav_internal_card ?card.
                    OPTIONAL{{?collection porbec:title_of_mav_collection ?collection_title.}}
                }} order by ?collection_title"""
}
], "author": [{"name_query": "What are the works of Author X?", 
"sql_query" : """SELECT card.titolo collate "C" 
            FROM ((media.mav_internal_autore as author
            left join media.mav_card_internal_autore
            as card_author on (author.id = card_author.id_internal_autore)) 
            left join media.mav_internal_card as card
            on (card_author.id_card = card.id))
            WHERE author.nome = '{}'
            ORDER BY card.titolo collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT ?titolo
            WHERE {{?autore porbec:nome_of_mav_internal_autore "{}"^^xsd:string.
                    ?card porbec:mav_card_internal_autore ?autore.
                    OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo.}}
                }}
            ORDER BY ?titolo"""
}, {"name_query": "What are the biographical data of an Author X?", 
"sql_query" : """SELECT author.nome, author.dati_anagrafici
            FROM media.mav_internal_autore as author
            WHERE author.nome = '{}'
            order by author.nome collate "C", author.dati_anagrafici collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT ?nome ?biographical_data
            WHERE {{?autore porbec:nome_of_mav_internal_autore "{}"^^xsd:string.
                OPTIONAL{{?autore porbec:dati_anagrafici_of_mav_internal_autore ?biographical_data.}}
                OPTIONAL{{?autore porbec:nome_of_mav_internal_autore ?nome.}}
                }}
                order by ?nome ?biographical_data"""
}, {"name_query": "What are the SPESs with work of an Author?", 
"sql_query" : """SELECT spes.description collate "C"
            FROM media.mav_internal_autore as author
                left join media.mav_card_internal_autore
                as card_author 
                on (author.id = card_author.id_internal_autore)
                left join media.mav_internal_card as card
                on (card_author.id_card = card.id)
                left join media.mav_spes as spes
                on (spes.id = card.id_spes)
            WHERE author.nome = '{}'
            order by spes.description collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT ?description
            WHERE {{?autore porbec:nome_of_mav_internal_autore "{}"^^xsd:string.
                ?card porbec:mav_card_internal_autore ?autore.
                ?card porbec:mav_internal_card_has_a_mav_spes ?spes.
                OPTIONAL{{?spes porbec:description_of_mav_spes ?description.}}
                }}
                order by ?nome ?description"""
}, {"name_query": "What are the collections with work of an Author X?", 
"sql_query" : """SELECT distinct collection.title collate "C"
            FROM media.mav_collection as collection
            left join media.mav_artworks_collection as art_coll on (collection.id = art_coll.id_collection) 
            left join media.mav_internal_card as card on (card.id = art_coll.id_card)
            left join media.mav_card_internal_autore as card_autore on (card_autore.id_card = art_coll.id_card)
            left join media.mav_internal_autore as autore on (autore.id = card_autore.id_internal_autore)
            WHERE autore.nome = '{}'
            order by collection.title collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT DISTINCT ?collection_titolo
            WHERE {{?autore porbec:nome_of_mav_internal_autore "{}"^^xsd:string.
            ?card porbec:mav_card_internal_autore ?autore.
            ?art_coll porbec:mav_artworks_collection_has_a_mav_internal_card ?card.
            ?art_coll porbec:mav_artworks_collection_has_a_mav_collection ?collection.
            OPTIONAL{{
                ?collection porbec:title_of_mav_collection ?collection_titolo.
                }}
            }} order by ?collection_titolo"""
}
], "materia": [{"name_query": "What are the work constructed from a given material X?", 
"sql_query" : """SELECT  card.titolo collate "C", mattec.materia collate "C", mattec.tecnica collate "C"
        FROM media.mav_internal_card as card
        left join media.mav_internal_card_materia_tecnica
        as card_mattec on (card.id = card_mattec.id_card) 
        left join media.mav_materia_tecnica as mattec
        on (mattec.id = card_mattec.id_internal_materia_tecnica)
        WHERE mattec.materia = '{}'
        order by card.titolo collate "C", mattec.materia collate "C", mattec.tecnica collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT ?titolo ?materia ?tecnica
            WHERE {{?mattec porbec:materia_of_mav_materia_tecnica "{}"^^xsd:string.
                ?card porbec:mav_internal_card_materia_tecnica ?mattec.
                OPTIONAL{{?card porbec:titolo_of_mav_internal_card ?titolo.}}
                OPTIONAL{{?mattec porbec:materia_of_mav_materia_tecnica ?materia.}}
                OPTIONAL{{?mattec porbec:tecnica_of_mav_materia_tecnica ?tecnica}}             
            }} order by ?titolo ?materia ?tecnica"""
}
], "tecnica": [{"name_query": "What are the work of a given technique X?", 
"sql_query" : """SELECT  card.titolo collate "C", mattec.materia collate "C", mattec.tecnica collate "C"
            FROM media.mav_internal_card as card
                left join media.mav_internal_card_materia_tecnica
                as card_mattec on (card.id = card_mattec.id_card) 
                left join media.mav_materia_tecnica as mattec
                on (mattec.id = card_mattec.id_internal_materia_tecnica)
            WHERE mattec.tecnica = '{}'
            order by card.titolo collate "C", mattec.materia collate "C", mattec.tecnica collate "C" """,
"sparql_query" : """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT  ?titolo ?materia ?tecnica
            WHERE {{?mattec porbec:tecnica_of_mav_materia_tecnica "{}"^^xsd:string.
                            ?card porbec:mav_internal_card_materia_tecnica ?mattec.
                            ?card porbec:titolo_of_mav_internal_card ?titolo
                            OPTIONAL{{?mattec porbec:materia_of_mav_materia_tecnica ?materia.}}
                            OPTIONAL{{?mattec porbec:tecnica_of_mav_materia_tecnica ?tecnica}}             
            }}order by ?titolo ?materia ?tecnica"""
}
], "materia_tecnica": [{"name_query": "What are the works constructed with material and technique?", 
"sql_query" : """SELECT card.titolo, mattec.materia, mattec.tecnica
            FROM media.mav_internal_card as card
            left join media.mav_internal_card_materia_tecnica
            as card_mattec on (card.id = card_mattec.id_card) 
            left join media.mav_materia_tecnica as mattec
            on (mattec.id = card_mattec.id_internal_materia_tecnica)
            WHERE mattec.materia = '{0}' and mattec.tecnica = '{1}'
            order by card.titolo collate "C", mattec.materia collate "C", mattec.tecnica collate "C" """,
"sparql_query" : """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX porbec: <http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
            SELECT  ?titolo ?materia ?tecnica
            WHERE {{?mattec porbec:materia_of_mav_materia_tecnica "{0}"^^xsd:string.
            {1}
            ?card porbec:mav_internal_card_materia_tecnica ?mattec.
            ?card porbec:titolo_of_mav_internal_card ?titolo
            OPTIONAL{{?mattec porbec:materia_of_mav_materia_tecnica ?materia.}}
            OPTIONAL{{?mattec porbec:tecnica_of_mav_materia_tecnica ?tecnica.}}             
            }} order by ?titolo ?materia ?tecnica"""
}
]}
