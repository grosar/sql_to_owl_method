--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2023-02-27 15:13:49

--
-- TOC entry 4 (class 2615 OID 50758)
-- Name: media; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA media;



ALTER SCHEMA media OWNER TO postgres;



--
-- TOC entry 201 (class 1259 OID 50759)
-- Name: mav_artworks_collection; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_artworks_collection (
    id_collection bigint NOT NULL,
    id_card bigint NOT NULL,
    progressive_room bigint
);


ALTER TABLE media.mav_artworks_collection OWNER TO postgres;



CREATE TABLE media.mav_background (
    id bigint NOT NULL,
    background character varying(10000),
    type character varying(255),
    id_contact bigint
);


ALTER TABLE media.mav_background OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 50777)
-- Name: mav_building; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 205 (class 1259 OID 50785)
-- Name: mav_card_internal_autore; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_card_internal_autore (
    id_card bigint NOT NULL,
    id_internal_autore bigint NOT NULL
);


ALTER TABLE media.mav_card_internal_autore OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 50790)
-- Name: mav_collection; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_collection (
    id bigint NOT NULL,
    description character varying(1000),
    title character varying(1000),
    image character varying(10000),
    id_spes bigint,
    pubblicabile character varying(2),
    show_catalogue character varying DEFAULT 'Si'::character varying,
    show_app character varying(4),
    click_app bigint DEFAULT 0
);


ALTER TABLE media.mav_collection OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 50800)
-- Name: mav_contatti; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_contatti (
    address character varying(10000),
    link_official_site character varying(10000),
    telephone character varying(10000),
    fax character varying(10000),
    email character varying(10000),
    pec character varying(10000),
    orari character varying(10000),
    id bigint NOT NULL,
    link_visita_virtuale character varying(10000),
    nomi_curatori character varying(10000),
    elenco_sponsor character varying(10000),
    last_edit date,
    header_light boolean,
    nome_museo character varying(10000),
    path_video_museo text,
    pdf_path character varying(10000),
    link_museo character varying(10000),
    numero_pagine_pdf bigint,
    numero_visite bigint DEFAULT '0'::bigint,
    active_fruition boolean DEFAULT false,
    is_freeze boolean DEFAULT false,
    latitude numeric,
    longitude numeric
);


ALTER TABLE media.mav_contatti OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 50811)
-- Name: mav_dashboard; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 209 (class 1259 OID 50819)
-- Name: mav_description; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_description (
    id bigint NOT NULL,
    text_description character varying(10000),
    language character varying(255),
    id_contact bigint
);


ALTER TABLE media.mav_description OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 50827)
-- Name: mav_device; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 211 (class 1259 OID 50837)
-- Name: mav_floor; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 212 (class 1259 OID 50845)
-- Name: mav_font; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_font (
    id bigint NOT NULL,
    font character varying(10000),
    type character varying(255),
    id_contact bigint
);


ALTER TABLE media.mav_font OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 50853)
-- Name: mav_internal_abstract; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_internal_abstract (
    id bigint NOT NULL,
    descrizione character varying(10000),
    lingua character varying(5),
    id_card bigint
);




ALTER TABLE media.mav_internal_abstract OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 50861)
-- Name: mav_internal_autore; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_internal_autore (
    id bigint NOT NULL,
    nome character varying(10000),
    dati_anagrafici character varying(10000),
    descendant_of bigint 
);
ALTER TABLE ONLY media.mav_internal_autore
    ADD CONSTRAINT mav_internal_autore_pkey PRIMARY KEY (id);
ALTER TABLE ONLY media.mav_internal_autore
    ADD CONSTRAINT autore_internal_autore_fk FOREIGN KEY (descendant_of) REFERENCES media.mav_internal_autore(id) ON DELETE CASCADE;


ALTER TABLE media.mav_internal_autore OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 50869)
-- Name: mav_internal_card; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_internal_card (
    id bigint NOT NULL,
    titolo character varying(10000),
    note character varying(10000)[],
    tipologia character varying(10000),
    cronologia character varying(10000),
    main_photo character varying(10000),
    id_spes bigint,
    geolocalizzazione bigint,
    id_misura bigint,
    licenza character varying(100),
    firma character varying(2000),
    iscrizioni character varying(2000),
    autore_testi character varying(2000),
    numero_inventario character varying(1000),
    visibility character varying(100),
    path_video_tensorflow character varying(1000),
    showvideo boolean DEFAULT false NOT NULL,
    fv boolean DEFAULT false NOT NULL,
    larghezza numeric,
    altezza numeric,
    profondita numeric,
    diametro numeric
);


ALTER TABLE media.mav_internal_card OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 50879)
-- Name: mav_internal_card_materia_tecnica; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_internal_card_materia_tecnica (
    id_card bigint NOT NULL,
    id_internal_materia_tecnica bigint NOT NULL
);


ALTER TABLE media.mav_internal_card_materia_tecnica OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 50884)
-- Name: mav_internal_multimedia; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_internal_multimedia (
    id bigint NOT NULL,
    id_card bigint,
    path_to_file character varying(10000),
    language_audio character varying(10),
    type character varying(50),
    profilo character varying(250)
);


ALTER TABLE media.mav_internal_multimedia OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 50892)
-- Name: mav_internal_racconto; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_internal_racconto (
    id bigint NOT NULL,
    id_card bigint,
    descrizione character varying(10000),
    profilo character varying(100),
    lingua character varying(5)
);


ALTER TABLE media.mav_internal_racconto OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 50900)
-- Name: mav_interval_date; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 220 (class 1259 OID 50908)
-- Name: mav_interval_date_spes; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 221 (class 1259 OID 50913)
-- Name: mav_location; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 222 (class 1259 OID 50921)
-- Name: mav_location_dbanc_artwork; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 223 (class 1259 OID 50926)
-- Name: mav_materia_tecnica; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_materia_tecnica (
    materia character varying(255) NOT NULL,
    tecnica character varying(255) NOT NULL,
    id bigint NOT NULL
);


ALTER TABLE media.mav_materia_tecnica OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 50936)
-- Name: mav_news; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 225 (class 1259 OID 50944)
-- Name: mav_news_image; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 227 (class 1259 OID 50951)
-- Name: mav_newsletter; Type: TABLE; Schema: media; Owner: postgres
--






--
-- TOC entry 228 (class 1259 OID 50956)
-- Name: mav_opendata; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 229 (class 1259 OID 50964)
-- Name: mav_path; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 230 (class 1259 OID 50972)
-- Name: mav_reach; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_reach (
    id bigint NOT NULL,
    path_description character varying(10000),
    language character varying(255),
    id_contact bigint
);


ALTER TABLE media.mav_reach OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 50980)
-- Name: mav_role; Type: TABLE; Schema: media; Owner: postgres
--

-- CREATE TABLE media.mav_role (
--     id bigint NOT NULL,
--     description character varying(255)
-- );


-- ALTER TABLE media.mav_role OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 50985)
-- Name: mav_scheda_device; Type: TABLE; Schema: media; Owner: postgres
--



--
-- TOC entry 233 (class 1259 OID 50990)
-- Name: mav_spes; Type: TABLE; Schema: media; Owner: postgres
--

CREATE TABLE media.mav_spes (
    id bigint NOT NULL,
    domain character varying(50) NOT NULL,
    description character varying(10000),
    admin_usr character varying(50) NOT NULL,
    admin_pwd character varying(50) NOT NULL,
    path_image character varying(255),
    email character varying(255) NOT NULL,
    id_thingsboard character varying(255),
    path_banner character varying(255),
    header_light boolean,
    -- enter_at timestamp(6) with time zone,
    -- exit_at timestamp(6) with time zone,
    is_vetrina boolean,
    completo boolean DEFAULT true NOT NULL
);


ALTER TABLE media.mav_spes OWNER TO postgres;




--
-- TOC entry 3089 (class 2606 OID 50935)
-- Name: mav_materia_tecnica mat_tec_unique; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_materia_tecnica
    ADD CONSTRAINT mat_tec_unique UNIQUE (materia, tecnica);


--
-- TOC entry 3091 (class 2606 OID 50933)
-- Name: mav_materia_tecnica materia_tecninca_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_materia_tecnica
    ADD CONSTRAINT materia_tecninca_pkey PRIMARY KEY (id);


--
-- TOC entry 3043 (class 2606 OID 50763)
-- Name: mav_artworks_collection mav_artworks_collection_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_artworks_collection
    ADD CONSTRAINT mav_artworks_collection_pkey PRIMARY KEY (id_collection, id_card);




--
-- TOC entry 3047 (class 2606 OID 50776)
-- Name: mav_background mav_background_spes_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_background
    ADD CONSTRAINT mav_background_spes_pkey PRIMARY KEY (id);


--
-- TOC entry 3051 (class 2606 OID 50789)
-- Name: mav_card_internal_autore mav_card_internal_autore_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_card_internal_autore
    ADD CONSTRAINT mav_card_internal_autore_pkey PRIMARY KEY (id_card, id_internal_autore);


--
-- TOC entry 3053 (class 2606 OID 50799)
-- Name: mav_collection mav_collection_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_collection
    ADD CONSTRAINT mav_collection_pkey PRIMARY KEY (id);


--
-- TOC entry 3055 (class 2606 OID 50810)
-- Name: mav_contatti mav_contatti_spes_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_contatti
    ADD CONSTRAINT mav_contatti_spes_pkey PRIMARY KEY (id);


--
-- TOC entry 3059 (class 2606 OID 50826)
-- Name: mav_description mav_description_spes_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_description
    ADD CONSTRAINT mav_description_spes_pkey PRIMARY KEY (id);





--
-- TOC entry 3067 (class 2606 OID 50852)
-- Name: mav_font mav_font_spes_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_font
    ADD CONSTRAINT mav_font_spes_pkey PRIMARY KEY (id);


--
-- TOC entry 3069 (class 2606 OID 50860)
-- Name: mav_internal_abstract mav_internal abstract_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_abstract
    ADD CONSTRAINT mav_internal_abstract_pkey PRIMARY KEY (id);


--
-- TOC entry 3071 (class 2606 OID 50868)
-- Name: mav_internal_autore mav_internal_autore_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3075 (class 2606 OID 50883)
-- Name: mav_internal_card_materia_tecnica mav_internal_card_materia_tecnica_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_card_materia_tecnica
    ADD CONSTRAINT mav_internal_card_materia_tecnica_pkey PRIMARY KEY (id_card, id_internal_materia_tecnica);


--
-- TOC entry 3073 (class 2606 OID 50878)
-- Name: mav_internal_card mav_internal_card_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_card
    ADD CONSTRAINT mav_internal_card_pkey PRIMARY KEY (id);


--
-- TOC entry 3077 (class 2606 OID 50891)
-- Name: mav_internal_multimedia mav_internal_multimedia_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_multimedia
    ADD CONSTRAINT mav_internal_multimedia_pkey PRIMARY KEY (id);


--
-- TOC entry 3079 (class 2606 OID 50899)
-- Name: mav_internal_racconto mav_internal_racconto_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_racconto
    ADD CONSTRAINT mav_internal_racconto_pkey PRIMARY KEY (id);




--
-- TOC entry 3103 (class 2606 OID 50979)
-- Name: mav_reach mav_reach_spes_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_reach
    ADD CONSTRAINT mav_reach_spes_pkey PRIMARY KEY (id);





--
-- TOC entry 3109 (class 2606 OID 50998)
-- Name: mav_spes mav_spes_pkey; Type: CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_spes
    ADD CONSTRAINT mav_spes_pkey PRIMARY KEY (id);



--
-- TOC entry 3143 (class 2606 OID 51135)
-- Name: mav_internal_abstract abstract_internal_card_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_abstract
    ADD CONSTRAINT abstract_internal_card_fk FOREIGN KEY (id_card) REFERENCES media.mav_internal_card(id);


--
-- TOC entry 3130 (class 2606 OID 51070)
-- Name: mav_background background_fk_contact; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_background
    ADD CONSTRAINT background_fk_contact FOREIGN KEY (id_contact) REFERENCES media.mav_contatti(id);





--
-- TOC entry 3126 (class 2606 OID 51050)
-- Name: mav_artworks_collection collection_fk_copy_1; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_artworks_collection
    ADD CONSTRAINT collection_fk_copy_1 FOREIGN KEY (id_collection) REFERENCES media.mav_collection(id);


--
-- TOC entry 3137 (class 2606 OID 51105)
-- Name: mav_description description_fk_contact; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_description
    ADD CONSTRAINT description_fk_contact FOREIGN KEY (id_contact) REFERENCES media.mav_contatti(id);


--
-- TOC entry 3147 (class 2606 OID 51155)
-- Name: mav_internal_multimedia fk_card_to_multimedia; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_multimedia
    ADD CONSTRAINT fk_card_to_multimedia FOREIGN KEY (id_card) REFERENCES media.mav_internal_card(id);


--
-- TOC entry 3142 (class 2606 OID 51130)
-- Name: mav_font font_fk_contact; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_font
    ADD CONSTRAINT font_fk_contact FOREIGN KEY (id_contact) REFERENCES media.mav_contatti(id);


--
-- TOC entry 3132 (class 2606 OID 51080)
-- Name: mav_card_internal_autore id_autore_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_card_internal_autore
    ADD CONSTRAINT id_autore_fk FOREIGN KEY (id_internal_autore) REFERENCES media.mav_internal_autore(id);


--
-- TOC entry 3133 (class 2606 OID 51085)
-- Name: mav_card_internal_autore id_card_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_card_internal_autore
    ADD CONSTRAINT id_card_fk FOREIGN KEY (id_card) REFERENCES media.mav_internal_card(id);





--
-- TOC entry 3167 (class 2606 OID 51255)
-- Name: mav_user_spesrole id_spesrole_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

--
-- TOC entry 3145 (class 2606 OID 51145)
-- Name: mav_internal_card_materia_tecnica internal_card_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_card_materia_tecnica
    ADD CONSTRAINT internal_card_fk FOREIGN KEY (id_card) REFERENCES media.mav_internal_card(id);


--
-- TOC entry 3127 (class 2606 OID 51055)
-- Name: mav_artworks_collection internal_card_fk_copy_1; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_artworks_collection
    ADD CONSTRAINT internal_card_fk_copy_1 FOREIGN KEY (id_card) REFERENCES media.mav_internal_card(id);


--
-- TOC entry 3162 (class 2606 OID 51230)
-- Name: mav_scheda_device internal_card_fk_copy_2; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3146 (class 2606 OID 51150)
-- Name: mav_internal_card_materia_tecnica internal_materia_tecnica_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_card_materia_tecnica
    ADD CONSTRAINT internal_materia_tecnica_fk FOREIGN KEY (id_internal_materia_tecnica) REFERENCES media.mav_materia_tecnica(id);


--
-- TOC entry 3149 (class 2606 OID 51165)
-- Name: mav_interval_date_spes interval_date_fk_to_date; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3150 (class 2606 OID 51170)
-- Name: mav_interval_date_spes interval_date_spes; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3157 (class 2606 OID 51205)
-- Name: mav_newsletter mav_newsletter_id_spes_fkey; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3158 (class 2606 OID 51210)
-- Name: mav_opendata mav_opendata_id_spes_fkey; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3129 (class 2606 OID 51065)
-- Name: mav_artworks_path path_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3166 (class 2606 OID 51250)
-- Name: mav_translation_path path_fk_copy_1; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3148 (class 2606 OID 51160)
-- Name: mav_internal_racconto racconto_internal_card_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_racconto
    ADD CONSTRAINT racconto_internal_card_fk FOREIGN KEY (id_card) REFERENCES media.mav_internal_card(id);


--
-- TOC entry 3160 (class 2606 OID 51220)
-- Name: mav_reach reach_spes_fk_contatti; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_reach
    ADD CONSTRAINT reach_spes_fk_contatti FOREIGN KEY (id_contact) REFERENCES media.mav_contatti(id);


--
-- TOC entry 3134 (class 2606 OID 51090)
-- Name: mav_collection spes_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_collection
    ADD CONSTRAINT spes_fk FOREIGN KEY (id_spes) REFERENCES media.mav_spes(id);


--
-- TOC entry 3135 (class 2606 OID 51095)
-- Name: mav_contatti spes_fk_copy_1; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_contatti
    ADD CONSTRAINT spes_fk_copy_1 FOREIGN KEY (id) REFERENCES media.mav_spes(id);


--
-- TOC entry 3144 (class 2606 OID 51140)
-- Name: mav_internal_card spes_fk_copy_2; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--

ALTER TABLE ONLY media.mav_internal_card
    ADD CONSTRAINT spes_fk_copy_2 FOREIGN KEY (id_spes) REFERENCES media.mav_spes(id);


--
-- TOC entry 3159 (class 2606 OID 51215)
-- Name: mav_path spes_fk_copy_3; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




--
-- TOC entry 3169 (class 2606 OID 51265)
-- Name: mav_visite_aggregato visite_aggregato_spes_fk; Type: FK CONSTRAINT; Schema: media; Owner: postgres
--




-- Completed on 2023-02-27 15:13:49

--
-- PostgreSQL database dump complete
--

