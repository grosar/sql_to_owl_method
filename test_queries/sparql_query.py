
QUERY = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX porbec: 
<http://www.semanticweb.org/rosar/ontologies/2023/0/porbec#>
SELECT DISTINCT ?titolo
WHERE {?spes porbec:description_of_mav_spes "Federico II - Università dell'arte"^^xsd:string.
?card porbec:mav_internal_card_has_a_mav_spes ?spes.
?description porbec:mav_description_has_a_mav_contatti ?contatti.
OPTIONAL{
     ?card porbec:titolo_of_mav_internal_card ?titolo.
    }
} order by ?titolo"""
