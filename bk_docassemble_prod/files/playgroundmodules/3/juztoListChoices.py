import docassemble.base.functions
from docassemble.base.util import capitalize

lists = {
  "genders": {"Femenino","Masculino"},
  "person": {"Natural", "Jurídica"},
  "bankaccount": {"Cuenta de ahorros", "Cuenta corriente"},
  "type": {"Persona","Empresa"},
  "type_j": {"Persona Natural","Persona Jurídica"},
  "period":{"Días",  "Semana(s)",  "Mes(es)",  "Año(s)"},
  "termination": {"Ambas partes", "El que contrata el sevicio", "El que presta el servicio"},
  "cesion": {"El que presta el servicio", "El que recibe el servicio", "Ambos partes"},
  "clausula_penal": {"El que presta el servicio","El que recibe el servicio","La parte que incumple"},
  "banks": {'BANCO AGRARIO','BANCO AV VILLAS','BANCO BBVA COLOMBIA S.A.','BANCO CAJA SOCIAL','BANCO COOPERATIVO COOPCENTRAL','BANCO DAVIVIENDA','BANCO DE BOGOTA','BANCO DE OCCIDENTE','BANCO FALABELLA ','BANCO GNB SUDAMERIS','BANCO ITAU','BANCO PICHINCHA S.A.','BANCO POPULAR','BANCO PROCREDIT','BANCO SANTANDER COLOMBIA','BANCO SERFINANZA','BANCOLOMBIA','BANCOOMEVA S.A.','CFA COOPERATIVA FINANCIERA','CITIBANK ','CONFIAR COOPERATIVA FINANCIERA','DAVIPLATA','NEQUI','RAPPIPAY','SCOTIABANK COLPATRIA'},
  "arl": {"ARL Positiva.","Seguros Bolívar S.A.","Seguros de Vida Aurora S.A.","Liberty Seguros de Vida.","Mapfre Colombia Vida Seguros S.A.","Riesgos Laborales Colmena.","Seguros de Vida Alfa S.A.","Seguros de Vida Colpatria S.A.","Seguros de Vida la Equidad Organismo C.","Sura - Cia. Suramericana de Seguros de Vida."},
  "eps": {'EPS SURAMERICANA S.A','COMPENSAR EPS','EPS SANITAS S.A','EPS FAMISANAR','NUEVA EPS S.A','COOMEVA EPS S.A','CRUZ BLANCA EPS','MEDIMAS','SUBS COMFASUCRE EPS','EMPRESAS PUBLICAS DE MEDELLIN','FONDO DE PASIVO SOCIAL DE FERROCARRILES','ALIANSALUD EPS S.A','COMFENALCO VALLE E.P.S','S.O.S. E.P.S','SAVIA SALUD EPS','CAPITAL SALUD EPS','MBUQ ESSECOOPSOS EPS','ADRES','ADRES - RÉGIMEN EXCEPCIÓN','CAJA DE COMPENSACION FAMILIAR COMFAMILIAR CAMACOLCOMFAMILIAR CAMACOL','CAJA DE COMPENSACION FAMILIAR DE ANTIOQUIA COMFAMA','Caja de Compensación Familiar de Cartagena "COMFAMILIAR CARTAGENA"','Caja de Compensación Familiar de Boyacá COMFABOY','CAJA DE COMPENSACION FAMILIAR DE CORDOBA COMFACOR','CAJA DE COMPENSACION FAMILIAR CAFAM','Caja de Compensación Familiar de la Guajira','Caja de Compensación Familiar del Huila "COMFAMILIAR"','Caja de Compensación Familiar de Nariño "COMFAMILIAR NARIÑO"','Caja de Compensación Familiar de Fenalco "COMFENALCO QUINDIO"','Caja Santandereana de Subsidio Familiar "CAJASAN"','Caja de Compensación Familiar de Fenalco Seccional de Santander','Caja de Compensación Familiar de Sucre.','CAJA DE COMPENSACION FAMILIAR DE BARRANCABERMEJA CAFABA','CAJA DE COMPENSACION FAMILIAR DE FENALCO DE TOLIMA COMFENALCO','Caja de Compensación Familiar del Norte de Santander "COMFANORTE"','Caja de Compensación Familiar C.C.F. del Oriente Colombiano "COMFAORIENTE"','Caja de Compensación Familiar de Cundinamarca COMFACUNDI','CAJA DE DE COMPENSACION FAMILIAR CAJACOPI ATLANTICO','COLSUBSIDIO','Caja de Compensación Familiar del Chocó COMFACHOCO','Caja de Compensación Familiar del Caquetá – COMFACA','Caprecom EPS','EPS CONVIDA','CAPRESOCA EPS','CALISALUD E.P.S','E.P.S. CONDOR S.A','SELVASALUD S.A. E.P.S','Asociación Indígena del Cesar y la Guajira DUSAKAWI','MANEXKA EPS','Asociación Indígena del Cauca','ANASWAYUU','MALLAMAS','PIJAOS SALUD EPSI','Salud Total S.A. E.P.S','Cafesalud E.P.S. S.A','EPS Programa Comfenalco Antioquia','Humana Vivir S.A. E.P.S','SOLSALUD E.P.S. S.A','SALUDVIDA S.A .E.P.S','Empresa Mutual para el Desarrollo Integral DE LA SALUD E.S.S EMDISALUD ESS','Cooperativa de Salud y Desarrollo Integral Zona Sur Oriental de Cartagena Ltda. COOSALUD E.S.S','Asociación Mutual La Esperanza ASMET SALUD','Asociación Mutual Barrios Unidos de Quibdó E.S.S','Entidad Cooperativa Sol.de Salud del Norte de Soacha ECOOPSOS','Asociación Mutual Empresa Solidaria de Salud de Nariño E.S.S. EMSSANAR E.S.S','Cooperativa de Salud Comunitaria-COMPARTA','Asociación Mutual SER Empresa Solidaria de Salud ESS'},
    "connectors": {"el","la","lo","los","las","al","un","una","unos","unas","del","a","ante","bajo","cabe","con","contra","de","desde","durante","en","entre","hacia","hasta","mediante","para","por","según","sin","so","sobre","tras","versus","vía"},
  "entidades": {'Instituto Municipal de Transito y Transporte de Corozal',
'Secretaria de Transporte y Movilidad de Cundinamarca - Sibaté','Secretaria de Transporte y Movilidad de Cundinamarca - Cajicá','Secretaria Distrital de Movilidad de Bogotá','Secretaria de Movilidad de Cali','Instituto de Tránsito del Atlántico','Secretaria de Movilidad de Medellín','Departamento Administrativo de Tránsito y Transporte - Cartagena','Secretaría de Movilidad Multimodal y Sostenible del Distrito de Santa Marta','Instituto de Tránsito y Transporte de Cartago','Secretaría de Tránsito y Transporte de Turbaco','Secretaria de Tránsito y Transporte de Popayán','Secretaria de Transporte y Movilidad de Cundinamarca - Ricaurte','Instituto Municipal De Tránsito y Transporte De Ciénaga','Secretaria de Tránsito y Transporte de Puerto Colombia','Secretaría De Tránsito Y Transporte De Yotoco','Secretaría de Movilidad de Itagüí','Secretaría De Transporte Y Movilidad De Zipaquirá','Secretaría De Tránsito Y Seguridad Vial De Barranquilla','Secretaría De Movilidad De Bello','Secretaría de Tránsito y Transporte de Yumbo','Secretaría de Tránsito y Transporte Municipal de Popayan','Secretaria de Transporte y Movilidad de Cundinamarca - Chocontá','Instituto Departamental De Tránsito Del Cesar'},
  "countries": {'Afganistán','Albania','Alemania','Andorra','Angola','Anguila','Antártida','Antigua y Barbuda','Antillas Neerlandesas','Arabia Saudita','Argelia','Argentina','Armenia','Aruba','Australia','Austria','Azerbaiyán','Bahamas','Bahrein','Bangladesh','Barbados','Belarús','Bégica','Belice','Benin','Bermudas','Bhután','Birmania (Myanmar)','Bolivia','Bosnia y Herzegovina','Botswana','Brasil','British Indian Ocean Territory','Brunei','Bulgaria','Burkina Faso','Burundi','Cabo Verde','Caimán, Islas','Camboya','Camerún','Canadá','Chad','Chile','Chipre','Ciudad del Vaticano','Cocos (Keeling), Islas','Colombia','Comoras','Congo, Rep. Dem.','Congo, República','Cook, Islas','Corea del Sur','Costa de Marfil','Costa Rica','Croacia','Cuba','Dinamarca','Djibouti','Dominica','Ecuador','EE.UU.','Egipto','El Salvador','Emiratos Árabes Unidos','Eritrea','Eslovaquia','Eslovenia','España','Estonia','Etiopía','Fiji','Filipinas','Finlandia','Francés Guayana','Francia','Gabón','Gambia','Georgia','Georgia del Sur e Islas Sandwich del Sur','Ghana','Gibraltar','Granada','Grecia','Groenlandia','Guadalupe','Guam','Guatemala','Guernsey','Guinea','Guinea Ecuatorial','Guinea-Bissau','Guyana','Haití','Honduras','Hong Kong','Hungría','India','Indonesia','Irán','Iraq','Irlanda','Isla Bouvet','Islandia','Islas Áland','Islas Feroe','Islas Heard y McDonald Islas','Islas Malvinas','Islas Marianas del Norte','Islas Turcas y Caicos','Islas VÃrgenes (Británicas)','Islas Vírgenes (EE.UU.)','Israel','Italia','Jamaica','Japón','Jersey','Jordania','Kazajstán','Kenya','Kirguistán','Kiribati','KOREA, DEM. República de','Kuwait','Laos','Lesotho','Letonia','Líbano','Liberia','Libia','Liechtenstein','Lituania','Luxemburgo','Macao','Macedonia','Madagascar','Malasia','Malawi','Maldivas','Malí','Malta','Man, Isla','Marruecos','Marshall, Islas','Martinica','Mauricio','Mauritania','Mayotte','México','Micronesia','Moldavia','Mónaco','Mongolia','Montenegro','Montserrat','Mozambique','Namibia','Nauru','Navidad, Isla de','Nepal','Nicaragua','Níger','Nigeria','Niue','Norfolk Island','Noruega','Nueva Caledonia','Nueva Zelanda','Omán','Países Bajos','Pakistán','Palau','Panamá','Papua Nueva Guinea','Paraguay','Perú','Pitcairn','Polinesia francés','Polonia','Porcelana','Portugal','Puerto Rico','Qatar','Reino Unido','República Centroafricana','República Checa','República Dominicana','Reunión, Isla de la','Rumania','Rusia, Federación de','Rwanda','Sáhara Occidental','Saint Kitts y Nevis','Saint Martin','Salomón, Islas','Samoa','Samoa Americana','San Bartolomé','San Marino','San Pedro y Miquelón','San Vicente y las Granadinas','Santa Lucía','Santo Tomé y Príncipe','Senegal','Serbia','Seychelles','Sierra Leona','Singapur','Siria','Somalia','Sri Lanka','Sudáfrica','Sudán','Suecia','Suiza','Suriname','Svalbard y Jan Mayen','Swazilandia','Tailandia','Taiwán','Tanzania','Tayikistán','Territorios del sur francés','Territorios Palestinos','Timor Oriental','Togo','Tokelau','Tonga','Trinidad y Tobago','Túnez','Turkmenistán','Turquía','Tuvalu','Ucrania','Uganda','Uruguay','Uzbekistán','Vanuatu','Venezuela','Vietnam','Wallis y Futuna','Yemen','Zambia','Zimbabwe'}
}
es_ordinal_nums = {
"male":{ '0': 'cero', '1': 'primer', '2': 'segundo', '3': 'tercer', '4': 'cuarto', '5': 'quinto', '6': 'sexto', '7': 'séptimo', '8': 'octavo', '9': 'noveno', '10': 'décimo', '11': 'décimo primero', '12': 'décimo segundo', '13':'décimo tercero', '14':'décimo cuarto', '15':'décimo quinto', '16':'décimo sexto', '17':'décimo séptimo', '18':'décimo octavo', '19':'décimo noveno', '20':'vigésimo'},
"female": {'0': 'cero', '1': 'primera', '2': 'segunda', '3': 'tercera', '4': 'cuarta', '5': 'quinta', '6': 'sexta', '7': 'séptima', '8': 'octava', '9': 'novena', '10': 'décima', '11': 'décimo primera', '12': 'décimo segunda', '13':'décimo tercera', '14':'décimo cuarta', '15':'décimo quinta', '16':'décimo sexta', '17':'décimo séptima', '18':'décimo octava', '19':'décimo novena', '20':'vigésima'},
"male2":{ '0': 'cero', '1': 'primero', '2': 'segundo', '3': 'tercero', '4': 'cuarto', '5': 'quinto', '6': 'sexto', '7': 'séptimo', '8': 'octavo', '9': 'noveno', '10': 'décimo', '11': 'décimo primero', '12': 'décimo segundo', '13':'décimo tercero', '14':'décimo cuarto', '15':'décimo quinto', '16':'décimo sexto', '17':'décimo séptimo', '18':'décimo octavo', '19':'décimo noveno', '20':'vigésimo'},
}
emails = {'Instituto Municipal de Transito y Transporte de Corozal':{'contactenos@imtraccorozal.gov.co','sustanciadorcorozal@hotmail.com','transitodecorozalsucre@hotmail.com'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Sibaté':{'contactenos@cundinamarca.gov.co','notificaciones@cundinamarca.gov.co','sibate@siettcundinamarca.com.co','juridicasibate@siettcundinamarca.com.co'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Cajicá':{'contactenos@cundinamarca.gov.co','notificaciones@cundinamarca.gov.co','cajica@siettcundinamarca.com.co'},
'Secretaria Distrital de Movilidad de Bogotá':{'judicial@movilidadbogota.gov.co','agendamientovirtual@movilidadbogota.gov.co','contactociudadano@movilidadbogota.gov.co'},
'Secretaria de Movilidad de Cali':{'contactenos@cali.gov.co','notificacionesjudiciales@cali.gov.co'},
'Instituto de Tránsito del Atlántico':{'fiscalizacionatl@hotmail.com','juridica2@transitodelatlantico.gov.co'},
'Secretaria de Movilidad de Medellín':{'notimedellin.oralidad@medellin.gov.co','audienciavirtual.movilidad@medellin.gov.co','atencion.ciudadana@medellin.gov.co'},
'Departamento Administrativo de Tránsito y Transporte - Cartagena':{'info@transitocartagena.gov.co'},
'Secretaría de Movilidad Multimodal y Sostenible del Distrito de Santa Marta':{'transito@santamarta.gov.co','siettsantamarta@gmail.com'},
'Instituto de Tránsito y Transporte de Cartago':{'notificacionesjudiciales@cartago.gov.co'},
'Secretaría de Tránsito y Transporte de Turbaco':{'info@transitoturbaco.gov.co'},
'Secretaria de Tránsito y Transporte de Popayán':{'pqr@popayan.gov.co'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Ricaurte':{'ricaurte@siettcundinamarca.com.co','contactenos@cundinamarca.gov.co','notificaciones@cundinamarca.gov.co'},
'Instituto Municipal De Tránsito y Transporte De Ciénaga':{'intracienaga@cienaga-magdalena.gov.co'},
'Secretaria de Tránsito y Transporte de Puerto Colombia':{'tramitesstt@puertocolombia-atlantico.gov.co'},
'Secretaría De Tránsito Y Transporte De Yotoco':{'contactenos@yotoco-valle.gov.co','notificacionjudicial@yotoco-valle.gov.co','atencion01.yotoco@controlyseguridadvial.co','transitoyotoco@gmail.com'},
'Secretaría de Movilidad de Itagüí':{'contactenos@itagui.gov.co'},
'Secretaría De Transporte Y Movilidad De Zipaquirá':{'oficinaasesorajuridica@zipaquira-cundinamarca.gov.co'},
'Secretaría De Tránsito Y Seguridad Vial De Barranquilla':{'notijudiciales@barranquilla.gov.co'},
'Secretaría De Movilidad De Bello':{'notificaciones@bello.gov.co'},
'Secretaría de Tránsito y Transporte de Yumbo':{'contactenos@yumbo.gov.co'},
'Secretaría de Tránsito y Transporte Municipal de Popayan':{'transitopopayan@transitopopayan.com.co','pqr@popayan.gov.co'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Chocontá':{'choconta@siettcundinamarca.com.co','juridicachoconta@siettcundinamarca.com.co '},
'Instituto Departamental De Tránsito Del Cesar':{'institutodetransito@cesar.gov.co'}}

cities_entities = {'Instituto Municipal de Transito y Transporte de Corozal':{'Corozal'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Sibaté':{'Bogotá'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Cajicá':{'Bogotá'},
'Secretaria Distrital de Movilidad de Bogotá':{'Bogotá'},
'Secretaria de Movilidad de Cali':{'Cali'},
'Instituto de Tránsito del Atlántico':{'Barranquilla'},
'Secretaria de Movilidad de Medellín':{'Medellín'},
'Departamento Administrativo de Tránsito y Transporte - Cartagena':{'Cartagena'},
'Secretaría de Movilidad Multimodal y Sostenible del Distrito de Santa Marta':{'Santa Marta'},
'Instituto de Tránsito y Transporte de Cartago':{'Cartago'},
'Secretaría de Tránsito y Transporte de Turbaco':{'Turbaco'},
'Secretaria de Tránsito y Transporte de Popayán':{'Popayán'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Ricaurte':{'Bogotá'},
'Instituto Municipal De Tránsito y Transporte De Ciénaga':{'Ciénaga'},
'Secretaria de Tránsito y Transporte de Puerto Colombia':{'Puerto Colombia'},
'Secretaría De Tránsito Y Transporte De Yotoco':{'Yotoco'},
'Secretaría de Movilidad de Itagüí':{'Itagüí'},
'Secretaría De Transporte Y Movilidad De Zipaquirá':{'Zipaquirá'},
'Secretaría De Tránsito Y Seguridad Vial De Barranquilla':{'Barranquilla'},
'Secretaría De Movilidad De Bello':{'Bello'},
'Secretaría de Tránsito y Transporte de Yumbo':{'Yumbo'},
'Secretaría de Tránsito y Transporte Municipal de Popayan':{'Popayán'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Chocontá':{'Chocontá'},
'Instituto Departamental De Tránsito Del Cesar':{'Valledupar'}}

persona_empresa={'Persona':'Persona Natural','Empresa':'Persona Jurídica'}
                 
cities_entities_freedoc = {'Instituto Municipal de Transito y Transporte de Corozal':{'Corozal'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Sibaté':{'Sibate'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Cajicá':{'Cajicá'},
'Secretaria Distrital de Movilidad de Bogotá':{'Bogotá'},
'Secretaria de Movilidad de Cali':{'Cali'},
'Instituto de Tránsito del Atlántico':{'Barranquilla'},
'Secretaria de Movilidad de Medellín':{'Medellín'},
'Departamento Administrativo de Tránsito y Transporte - Cartagena':{'Cartagena'},
'Secretaría de Movilidad Multimodal y Sostenible del Distrito de Santa Marta':{'Santa Marta'},
'Instituto de Tránsito y Transporte de Cartago':{'Cartago'},
'Secretaría de Tránsito y Transporte de Turbaco':{'Turbaco'},
'Secretaria de Tránsito y Transporte de Popayán':{'Popayán'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Ricaurte':{'Ricaurte'},
'Instituto Municipal De Tránsito y Transporte De Ciénaga':{'Ciénaga'},
'Secretaria de Tránsito y Transporte de Puerto Colombia':{'Puerto Colombia'},
'Secretaría De Tránsito Y Transporte De Yotoco':{'Yotoco'},
'Secretaría de Movilidad de Itagüí':{'Itagüí'},
'Secretaría De Transporte Y Movilidad De Zipaquirá':{'Zipaquirá'},
'Secretaría De Tránsito Y Seguridad Vial De Barranquilla':{'Barranquilla'},
'Secretaría De Movilidad De Bello':{'Bello'},
'Secretaría de Tránsito y Transporte de Yumbo':{'Yumbo'},
'Secretaría de Tránsito y Transporte Municipal de Popayan':{'Popayán'},
'Secretaria de Transporte y Movilidad de Cundinamarca - Chocontá':{'Choconta'},
'Instituto Departamental De Tránsito Del Cesar':{'Valledupar'}}

entidades_habeasdata = {'Almacenes Éxito S.A': {'sclientee@grupo-exito.com', 'tarjetaexito@tarjetaexito.com.co'},
 'Arpesod Asociados S.A.S. (Electrocréditos)': {'contactenos@electrocreditosdelcauca.com'},
 'Avantel S.A.S.': {'notificacionesjudiciales@avantel.com.co'},
 'BBVA Banco Bilbao Vizcaya Argentaria Colombia S.A': {'defensoria.bbvacolombia@bbva.com.co', 'notifica.co@bbva.com'},
 'Backstartup S.A.S.': {'consulta@backstartup.com'},
 'Bancamía': {'defensoriabancamia@pgabogados.com', 'servicioalconsumidor@bancamia.com.co'},
 'Banco Av Villas': {'notificacionesjudiciales@bancoavvillas.com.co', 'notificacionescomerciales@bancoavvillas.com.co'},
 'Banco Caja Social': {'notificacionesjudiciales@fundaciongruposocial.co'},
 'Banco Davivienda': {'notificacionesjudiciales@davivienda.com'},
 'Banco Falabella S.A': {'datospersonales@bancofalabella.com.co'},
 'Banco Pichincha S.A.': {'clientes@pichincha.com.co'}, 'Banco Popular': {'servicioalclientebp@bancopopular.com.co'},
 'Banco Serfinanzas S.A': {'info@bancoserfinanza.com'},
 'Banco W': {'correspondenciabancow@bancow.com.co', 'sclientebancow@bancow.com.co'},
 'Banco de Bogotá': {'defensofiaconsumidorfinanciero@bancodebogota.com.co', 'rjudicial@bancodebogota.com.co'},
 'Cancillería de Colombia': {'contactenos@cancilleria.gov.co'},
 'Cifin': {'atencionaltitularcifin@transunion.com', 'notificaciones@transunion.com'},
 'Colombia Telecomunicaciones S.A. E.S.P. - Movistar': {'notificacionesjudiciales@telefonica.com'},
 'Comcel S.A. (CLARO)': {'notificacionesclaro@claro.com.co', 'solucionesclaro@claro.com.co'},
 'Compañía de Financiamiento Tuya S.A.': {'defensordelconsumidor@tuya.com.co'},
 'Cooperativa Multiactiva De Aporte Y Crédito Solidario': {'datos@cooperativasolidarios.com.co'},
 'Datacrédito': {'notificacionesjudiciales@experian.com'}, 'Direct TV Colombia Ltda': {'andsar@directvla.com.co'},
 'Directv Colombia LTDA': {'andsar@directvla.com.co'}, 'EPS Sanitas S.A.S.': {'notificajudiciales@keralty.com'},
 'ETB': {'etbprejuridico@serlefin.com', 'asuntos.contenciosos@etb.com.co'},
 'Embajada De Estados Unidos En Colombia': {'FBU.Santo.Domingo@ssa.gov'},
 'Fianzacrédito': {'info@fianzacredio.com', 'sugerenciasyreclamos@fianzacredito.com'},
 'Fiscalia': {'denunciaanonima@fiscalia.gov.co'},
 'GM Financial Colombia S.A. Compañía de Financiamiento': {'notificacionesjudicial@gmfinancial.com'},
 'Indagro S.A.': {'oficinabogota@indagro.com.co', 'gerencia.indagro@hotmail.com'},
 'Itau Corpbanca S.A.': {'servicioalcliente@itau.co'},
 'Krono Time SAS': {'contabilidad@kronotime.com.co', 'kronotime@hotmail.com'},
 'MERCADOLIBRE COLOMBIA LTDA': {'notijudicialmco@mercadolibre.com.co'},
 'MERCADOPAGO COLOMBIA LTDA': {'notijudicialmpo@mercadopago.com.co'},
 'Marketing Personal S.A': {'Informacion@marketingpersonal.com'},
 'Marval': {'protecciondatos@marval.com.co', 'servicioalcliente@marval.com.co'},
 'Muebles Jamar S.A': {'impuestoscorporativo@gmail.com', 'servicioweb@mueblesjamar.co.co'},
 'National Holding Services Empresa Asociativa De Trabajo': {'nationalholding@yahoo.com'},
 'Promociones y Cobranzas Beta S.A.': {'contactenos@cobranzasbeta.com.co'},
 'Promotora Inversiones y Cobranzas S.A.S.': {'notificaciones@promotoradeinversionesycobranzas.com'},
 'QNT S.A.S': {'contacto@qnt.com.co'}, 'RF ENCORE S A S': {'cvelasquez@refinancia.co'},
 'Redsuelva': {'laura.buendia@redsuelva.com'}, 'Refinancia': {'contactenos@refinancia.co'},
 'Reincar': {'contacto@reincar.com.co'},
 'Scotiabank - Colpatria': {'notificbancolpatria@scotiabankcolpatria.com', 'sac_ccfiducolpatria@colpatria.com'},
 'Smart Training Society S.A.S.': {'info@smart.edu.co'},
 'Superintendencia De Industria Y Comercio - SIC': {'contactenos@sic.gov.co'},
 'Yanbal de Colombia S.A.S.': {'yanbalrespondeco@yanbal.com', 'notificaciones@yanbal.com'}}

airlines_entities_data = {
  'Avianca S.A':['890100577 - 6','BARRANQUILLA'],
  'ABC AEROLINEAS S A DE C V SUCURSAL COLOMBIA - EN LIQUIDACIÓN JUDICIAL - Interjet':['900580599 - 1','BOGOTA, D.C.'],
  'Aegean Airlines S.A.':[],
  'Aero República S.A. / Compañía Panameña de Aviación S.A. - Copa Airlines Colombia':[],
  'Aeroméxico':['900254148-6','BOGOTA, D.C.'],
  'Aerorepublica S.A (WINGO)':['800185781 - 1','BOGOTA, D.C.'],
  'Aerovías de Integración Regional S.A. -LATAM Airlines':['8300191898','BOGOTA, D.C.'],
  'Air Canada Sucursal Colombia':['830141412 - 7','BOGOTA, D.C.'],
  'AIR EUROPA LINEAS AEREAS SOCIEDAD ANONIMA':['830111124 - 2','BOGOTA, D.C.'],
  'AMERICAN AIRLINES INC SUCURSAL COLOMBIANA':['800095254','BOGOTA, D.C.'],
  'Compañia Panameña de Aviación S.A.- Copa Airlines':['860025338 - 2','BOGOTA, D.C.'],
  'Deutsche Lufthansa Aktiengesellschaft':['8600053093','MEDELLIN'],
  'Easyfly S.A.':['900088915 - 7','BOGOTA, D.C.'],
  'Fast Colombia S.A.S. - Viva Air':['900313349','BOGOTA, D.C.'],
  'Gran Colombia De Aviacion S A S':['901107380 - 3','CALI'],
  'IBERIA LINEAS AEREAS DE ESPAÑA SOCIEDAD ANONIMA OPERADORA SUCURSAL COLOMBIANA -IBERIA LAE S.A.':['860005330','BOGOTA, D.C.'],
  'Jetblue Airways Corporation Sucursal Colombia':['900254399 - 8','BOGOTA, D.C.'],
  'JETSMART AIRLINES SA. SUCURSAL COLOMBIA':['901326843 - 0','BOGOTA, D.C.'],
  'PLUS ULTRA LINEAS AEREAS S.A. SUCURSAL COLOMBIA':[],
  'Royal Dutch Airlines KLM':['901447582 - 2','BARRANQUILLA'],
  'Satena S.A':[],
  'SERVICIOS AEREOS PANAMERICANOS S.A.S':['891201578 - 0','MEDELLIN'],
  'SOCIEDAD AIR FRANCE':['860007369 - 4','BOGOTA, D.C.'],
  'Spirit Airlines':['900212103 - 5','BOGOTA, D.C.'],
  'Turkish Airlines Inc. Sucursal Colombia':['900958911 - 1','BOGOTA, D.C.'],
  'Ultra Air SAS':['901428193 - 1','RIONEGRO']
}

travel_agency_data = {
  'Agencia de viajes Aviatur S.A.S':['860000018','BOGOTA, D.C.'],
  'Atrapalo Colombia SAS':['900413476 - 1','BOGOTA, D.C.'],
  'Despegar Colombia S.A.S':['900610518','BOGOTA, D.C.'],
  'Flight Network':[],
  'Empresa Aérea de Servicios y Facilitación Logística Integral S.A-Easyfly':[],
  'Grupo San German Express S.A.S':['900828380 - 3','MEDELLIN'],
  'Inversiones Viajes & Viajes S.A.S':['900041392 - 2','MEDELLIN'],
  'NEW TRIP AJR SAS':['900856350 - 1','MEDELLIN'],
}


tutela_list = {'Tutela derecho de petición comparendo', 'Tutela por no agendamiento'}
instancias = {'Primer juez', 'Segundo juez'}

def setOrdinal( gender ):
#  return es_ordinal_nums[gender]
  docassemble.base.functions.update_ordinal_numbers('es', es_ordinal_nums[gender])
  docassemble.base.functions.update_ordinal_function('es', es_ordinal_nums[gender])
  return True

def get_ordinal(gender, inx, transform = 'l'):
  pos = int(inx)+1
  if transform == 'c':
    return capitalize(es_ordinal_nums[gender][repr(pos)])
  elif transform == 'u':
    return es_ordinal_nums[gender][repr(pos)].upper()
  else:
    return es_ordinal_nums[gender][repr(pos)]
  
def get_list(pos):
  return sorted(lists[pos])

def get_data_entities(dict_entity,name_entity):
  return dict_entity[name_entity]

def get_tutela_type():
  return tutela_list

def get_judge_instances():
  return instancias

def get_list_unsort(pos):
  return lists[pos]

def get_genders():
  return {"femenino":"Femenino","masculino":"Masculino"}

def get_type_person():
  return {"N":"Natural", "J":"Juridica"}

def get_type_account():
  return {"A":"Ahorros", "C":"Corriente"}

def get_list_banks():
  return {'BANCO AGRARIO','BANCO AV VILLAS','BANCO BBVA COLOMBIA S.A.','BANCO CAJA SOCIAL','BANCO COOPERATIVO COOPCENTRAL','BANCO DAVIVIENDA','BANCO DE BOGOTA','BANCO DE OCCIDENTE','BANCO FALABELLA ','BANCO GNB SUDAMERIS','BANCO ITAU','BANCO PICHINCHA S.A.','BANCO POPULAR','BANCO PROCREDIT','BANCO SANTANDER COLOMBIA','BANCO SERFINANZA','BANCOLOMBIA','BANCOOMEVA S.A.','CFA COOPERATIVA FINANCIERA','CITIBANK ','CONFIAR COOPERATIVA FINANCIERA','DAVIPLATA','NEQUI','RAPPIPAY','SCOTIABANK COLPATRIA'}

def get_list_countries():
  _list = sorted(lists['countries'])  
  return ['Colombia'] + _list

def title_juzto(string_juzto):
  _str = string_juzto.split()
  _newstr = ''
  _len = len(_str) - 1
  _space = ''
  for i, word in enumerate(_str):
      if i < _len:
          _space = ' '
      if word in lists["connectors"]:
          _newstr += word.lower()+_space
      else:
          _newstr += word.lower().capitalize()+_space
  return _newstr

def getEntity(city):
  for f in cities_entities_freedoc:
    if city in cities_entities_freedoc[f]:
        return f
  return None

def get_entities_habeas():
  ans = list(entidades_habeasdata.keys())
  ans.append('Otro')
  return ans