#Importe de libreria y paquetes necesarios para las funcionalidades
import json, requests, boto3, uuid, math, time, base64, calendar, math
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from docassemble.webapp.users.models import Calendar, DniGroups, DniTypess, DniTypeGroup, Cities
from sqlalchemy import or_, and_
from num2words import num2words
import xml.etree.ElementTree as ElementTree
from docassemble.base.util import *
from docassemble.base.util import ensure_definition
import sentry_sdk
import numpy as np
import numpy_financial as npf
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
#API Token de Sengrid
sentry_sdk.init("https://5837dc5eaba34b9c9c74f4205fa1e7b2@o414462.ingest.sentry.io/5304049")
#API Token de Universial Tutorial para obtener paises, departamentos-estados, ciudades-municipios
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJfZW1haWwiOiJhbmRyZXMuZ3V0aWVycmV6QGp1enRvLmNvIiwiYXBpX3Rva2VuIjoiLVg4TVpneFZSeERBeW9WdHJGRUlFMmlzS2dJcE9pWWdIMEM3X0cwaFpvMW5pNnlfLVBtM21iT1RNRkY5VVYxaTM2VSJ9LCJleHAiOjE1ODM2MDAyMDJ9.ePFg1Oca7Ls-SGml-V1cXNVM506nVBnsUc_WrU0TiUs"
#Headers necesarias para las peticiones via API
api_url_base = "https://www.universal-tutorial.com/api/"
headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+api_token}
#Variables globales para la conexión y peticiones al API de PayU
country = "Colombia"
api_url_payu = "https://api.payulatam.com/payments-api/4.0/service.cgi"
api_key_payu = "k1N7I8MBo0nriGVIemBTg59Hn2"
api_login_payu = "cgAsZN16FsTwwme"
#Variables globales para definir valores de salarios deben actualizarse el 01 de enero de cada año
#Anual [start]
z_minimum_salary = 1160000 
z_minimum_hour_salary = 4833
z_transport_aid = 140606
z_integral_salary = 15080000
#Anual [End]
#Variable global de texto por defecto usado en las entrevistas versión 1
z_text_final_screen = "Ahora que tenemos tus datos, ¿estás de acuerdo con su uso para generar el documento?"
#Variable tipo lista de las tasas de interes por mes del año vigente
listInterest = [0,0.1906,0.1895,0.1895,0.1869,0.1819,0.1812,0.1812,0.1829,0.1835,0.1835,0.2676,0.2619]
#TEA = listInterest[today(format='M')]
# Mensual [Start] Interés Bancario Cte. (Consumo y Ordinario) - Tasa de usura
TEA=0.2649
# Mensaul [End]

#Metodo que utiliza el API de universal totorial para traer los paises
def get_states( _country_ = False ):
  q = _country_ if _country_ else country
  api_url = api_url_base+'states/'+q
  response = requests.get(api_url, headers=headers)
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8'))
  else:
    return None

#Metodo que utiliza el API de universal tutorial que trae las ciudades de un paìs especifico
def get_cities_by_state( _state_ ):
  api_url = api_url_base+'cities/'+_state_
  response = requests.get(api_url, headers=headers)
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8'))
  else:
    return None

#Metodo que utiliza el model cities para traer la ciudades almacenadas en la tabla cities
#al resultado de la query sqlalchemy se apendizan las ciudades principales de Colombia

def get_cities():
  result = Cities.query.with_entities(Cities.name).order_by(Cities.name).all()
  principal = ["Bogotá","Medellín","Cali","Bucaramanga","Cartagena","Barranquilla","Pasto","Cúcuta"]
  rlist = []
  for item in result:
    rlist.append(list(item)[0])
  for x in principal:
    if not x in rlist:
        rlist.append(x)
  return rlist

def fix_secretaria(secretaria):
  if('__a' in secretaria):
    secretaria = secretaria.replace('__a','á')
  if('__e' in secretaria):
    secretaria = secretaria.replace('__e','é')
  if('__i' in secretaria):
    secretaria = secretaria.replace('__i','í')
  if('__o' in secretaria):
    secretaria = secretaria.replace('__o','ó')
  if('__u' in secretaria):
    secretaria = secretaria.replace('__u','ú')
  if('__A' in secretaria):
    secretaria = secretaria.replace('__A','Á')
  if('__E' in secretaria):
    secretaria = secretaria.replace('__E','É')
  if('__I' in secretaria):
    secretaria = secretaria.replace('__I','Í')
  if('__O' in secretaria):
    secretaria = secretaria.replace('__O','Ó')
  if('__U' in secretaria):
    secretaria = secretaria.replace('__U','Ú')
  if('__ñ' in secretaria):
    secretaria = secretaria.replace('__ñ','ñ')
  if('__Ñ' in secretaria):
    secretaria = secretaria.replace('__Ñ','Ñ')
  return secretaria

#Inicia con otras
def get_cities2():
  result = Cities.query.with_entities(Cities.name).order_by(Cities.name).all()
  rlist = []
  for item in result:
    rlist.append(list(item)[0])
  if 'Bogotá D.C' in rlist:
    rlist.remove('Bogotá D.C')
  principal = ["Bogotá","Medellín","Cali","Barranquilla"]
  for x in principal:
    if x in rlist:
        rlist.remove(x)
  return principal + rlist

#Metodo para obtener la ciudades entregadas deste Datos GOV, se apendizan las ciudades principales al resultado
def get_cities_old():
  response = requests.get("https://www.datos.gov.co/resource/xdk5-pm3f.json")
  if response.status_code == 200:
    data = json.loads(response.content.decode('utf-8'))
    cities = []
    i = 0
    for row in data:
      cities.insert(i, row['municipio'])
      i = i+1
    city = sorted(cities)  
    principal = ["Bogotá","Medellín","Cali","Bucaramanga","Cartagena","Barranquilla","Pasto","Cúcuta"]
    return principal + city
  else:
    return None

#Metodo que retorna la cantidad de dìas que estan entre dos fechas que llegan como parametros
def difference_date(idate, fdate):
  result = Calendar.query.filter(
    and_(Calendar.date.between(idate, fdate),
         Calendar.enable == 1
        )).all()
  return len(result)

#Metodo que utiliza el paquete num2words para convertir una cantidad.moneda a texto
#El metodo evalua si la cantidad es superior a un millón de pesos para pasar uno a un y concatenar el conector de
def number_to_string(number):
  is_million = number%1000000
  txt = num2words(number, lang='es_CO')    
  if is_million == 0:
    txt = txt+" de"
  return txt.replace("uno", "un")

#Metodo que utiliza el API de PayU para obtener la lista de bancos vigentes en Colombia
def get_list_banks_payu():
  payu_json = {"language": "es","command": "GET_BANKS_LIST","merchant": {"apiLogin": api_login_payu,"apiKey": api_key_payu},"test": False,"bankListInformation": {"paymentMethod": "PSE","paymentCountry": "CO"}}
  response = requests.post(api_url_payu, json=payu_json)
  if response.status_code == 200:
    arr = []
    i = 0
    res = ElementTree.fromstring(response.content)
    for bank in res.findall('.//bank'):
      if bank.find("description").text == 'A continuación seleccione su banco':
        continue
      arr.insert(i, bank.find("description").text)
      i = i+1
    return arr
  else:
    return None

#Metodo que retorna los tipos de documentos segun sea el caso mayor de edad, menor de edad
#Este metodo usa el modelo DniTypeGroup por medio de query sqlalchemy
def get_list_dni( code ):
  dnis=[]
  for dni in DniTypess.query.with_entities(DniTypess.code, DniTypess.name, DniTypess.name+" - ("+DniTypess.code+") ").join(DniTypeGroup, DniTypeGroup.typedni == DniTypess.id).join(DniGroups, DniGroups.id == DniTypeGroup.groupdni).filter(DniGroups.code == code).all():
    if not dni[1] in dnis:
      dnis.append(dni[1])
  return dnis
  #result = DniTypess.query.with_entities(DniTypess.code, DniTypess.name+" - ("+DniTypess.code+") ").join(DniTypeGroup, DniTypeGroup.typedni == DniTypess.id).join(DniGroups, DniGroups.id == DniTypeGroup.groupdni).filter(DniGroups.code == code).all()
  #return result

#Metodo que retorna un diccionario de datos de los tipos de documentos utiliza el metodo get_list_dni para
#pasar el resultado a un diccionario
def get_dict_dni( code ):
  result = get_list_dni(code)
  return dict(result)

#Metodo que recibe una lista del tipo DAList y retorna la posición correspondiente al valor analizado
def which_value( vallist ):
  docnumber = 0
  for v in vallist:
    if v is not 0:
      docnumber = v
  return docnumber 

def generate_nit(nit):
  data = (str(nit).replace('.', '')).replace('-','')
  number = data.rjust(15,'0')
  secuentias = [3,7,13,17,19,23,29,37,41,43,47,53,59,67,71]
  aritmethic = sum(int(number[14 - i]) * secuentias[i] for i in range(14)) % 11
  dv = 0
  if aritmethic > 1:
    sub = 11-aritmethic
    dv = sub
  else:
    dv = aritmethic
  return str(nit) +'-'+ repr(dv)
#Metodo usado en los templates-docx para retornar el NIT en el formato 000.000.000-0 validando tambien el digito de verificaciòn
def generateNit(nit):
  data = str(nit).replace('.', '')
  number = data.rjust(15,'0')
  secuentias = [3,7,13,17,19,23,29,37,41,43,47,53,59,67,71]
  aritmethic = sum(int(number[14 - i]) * secuentias[i] for i in range(14)) % 11
  dv = 0
  if aritmethic > 1:
    sub = 11-aritmethic
    dv = sub
  else:
    dv = aritmethic
  return str(nit) +'-'+ repr(dv)
# Metodo para dar formato a una fecha dentro de una entrevista en caso de que no salga formateada
def date_format(date):
  date = date.strftime('%Y-%m-%d')
  date = date.replace('/', '-')
  date = datetime.strptime(date,'%Y-%m-%d')
  months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
  day = date.day
  month = months[date.month - 1]
  year = date.year
  date_format = "{} de {} de {}".format(day, month, year)
  return date_format
# Metodo para saber que tipo de caducidad tiene una infracción por fotocomparendo
# Los argumentos son: first_date fecha bandera de evaluación si hay caducidad, inf_date fecha de la infración, res_date fecha de la resolucion sancionatoria
# returno si existe caducidad y si se le aplica primer o segundo vencimiento
def get_caducidad(first_date, inf_date, res_date=None):
  
  inf_date = inf_date.strftime('%Y-%m-%d')
  
  dates = None
  first_caducidad = False
  second_caducidad = False
    
  first_date = datetime.strptime(first_date, '%Y-%m-%d')
  inf_date = datetime.strptime(inf_date, '%Y-%m-%d')
  if inf_date <= first_date:
    dates = True
  else:
    dates = False

  if res_date is not None:
    res_date = res_date.strftime('%Y-%m-%d')
    res_date = datetime.strptime(res_date, '%Y-%m-%d')
    if res_date >= (inf_date + relativedelta(months=6)):
      first_caducidad = True
    if res_date >= (inf_date + relativedelta(months=12)):
      second_caducidad = True
        
  return dates, first_caducidad, second_caducidad

# Metodo para saber que tipo de caducidad tiene una infracción por fotocomparendo y para usar en la entrevista NO por API en el CRM
# Los argumentos son: first_date fecha bandera de evaluación si hay caducidad, inf_date fecha de la infración, res_date fecha de la resolucion sancionatoria
# returno si existe caducidad y si se le aplica primer o segundo vencimiento
def get_caducidad_interview(first_date, inf_date, res_date=None):
  
  dates = None
  first_caducidad = False
  second_caducidad = False
    
  first_date = datetime.strptime(first_date, '%d/%m/%Y')
  inf_date = datetime.strptime(inf_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
  if inf_date <= first_date:
    dates = True
  else:
    dates = False

  if res_date is not None:
    res_date = datetime.strptime(res_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
    if res_date >= (inf_date + relativedelta(months=6)):
      first_caducidad = True
    if res_date >= (inf_date + relativedelta(months=12)):
      second_caducidad = True
        
  return dates, first_caducidad, second_caducidad
#Metodo que recibe una cantidad en formato moneda $0.000.000 y retorna solo el valor nùmerico
def get_only_number( amount ):
  if isinstance(amount, float):
    amount = int(amount)
  _value = str(amount)
  return int(_value.replace('.', ''))

#Metodo que recibe una lista de valores y retorna la cantidad de valores
def get_list_arguments(list_arguments):
  counter = 0
  for x, y in enumerate(list_arguments):
    if y == True:
      counter = counter + 1
  return counter

#Metodo usado en el final screen de la entrevista de diagnostico para su correspondiente almacenamiento en AWS S3
def save_specific_file(the_document, filename, hashda, tipo):
  if hashda == False:
    _gen = uuid.uuid4().hex[:16].upper()
  else:
    _gen = hashda
  _name = _gen+'_'+filename
  _folder = 'documentos/diagnostico/'
  s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AKIAW4FCIUSGWGSJOTCM', aws_secret_access_key='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')
  if tipo == 'pdf':
    s3.upload_file(the_document.pdf.path(), 'juzto', _folder+_name+'.pdf')
  if tipo == 'docx':
    s3.upload_file(the_document.docx.path(), 'juzto', _folder+_name+'.docx')
  return _folder+_name+'.'+tipo

#Metodo usado por las entrevistas para almacenar los docx y pdf en AWS S3
def save_files(the_document, filename, production = False, hashda = False):
  if production:
    _subfolder = 'produccion/'
  else:
    _subfolder = 'gratis/'
  if hashda == False:
    _gen = uuid.uuid4().hex[:16].upper()
  else:
    _gen = hashda
  _name = _gen+'_'+filename
  _folder = 'documentos/'+_subfolder
  #s3 = boto3.client('s3', region_name='sa-east-1', aws_access_key_id='AKIAW4FCIUSGTGOG5HT4', aws_secret_access_key='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')
  s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AKIAW4FCIUSGWGSJOTCM', aws_secret_access_key='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')
#  s3.upload_file(the_document.pdf.path(), 'documentoslegales.co', _folder+_name+'.pdf')
#  s3.upload_file(the_document.docx.path(), 'documentoslegales.co', _folder+_name+'.docx')
  s3.upload_file(the_document.pdf.path(), 'juzto', _folder+_name+'.pdf')
  s3.upload_file(the_document.docx.path(), 'juzto', _folder+_name+'.docx')
  return _gen

#Metodo que retorna valores globales ya definidos o consulta en Datos GOV el TRM
def global_value( value ):
  if value == 'minimum':
    return z_minimum_salary
  if value == 'transport':
    return z_transport_aid
  if value == 'integral':
    return z_integral_salary
  if value == 'trm':
    response = requests.get("https://www.datos.gov.co/resource/32sa-8pi3.json")
    if response.status_code == 200:
      data = json.loads(response.content.decode('utf-8'))
      return math.ceil(float(data[0]['valor']))

#Metodo usado para el final screen de las entrevistas el cual se usa en las entrevistas V1
#Evalua si en la URL viene el ID de empleado y asi mostrar botones de descarga
#Si es un cliente muestra el boton de confirmar y pagar
def  get_callback_final_screen_new(price, identifier, name, production = False):
  if 'employee' not in value('url_args'):
    return '<button class="btn add_da_to_cart btn btn-lg btn-block btn-success" data-id="'+identifier+'" data-name="'+name+'">CONFIRMAR Y PAGAR</button>'
  else:
    _urlS3 = 'https://juzto.s3.amazonaws.com/documentos/produccion/'+identifier+'_'+name
    btnPDF = '<a href="'+_urlS3+'.pdf" class="btn btn-md btn-block btn-primary btn-da-pdf" target="_blank" download="" style="background: #002888 !important; color: #fff !important;" data-id="'+identifier+'" data-name="'+name+'"><i class="far fa-file-pdf"></i> PDF</a>'
    btnDOCX= '<br><a href="'+_urlS3+'.docx" class="btn btn-md btn-block btn-primary btn-da-pdf" target="_blank" download="" style="background: #002888 !important; color: #fff !important;" data-id="'+identifier+'" data-name="'+name+'"><i class="far fa-file-word"></i> DOCX</a>'
    _html = btnPDF
    if 'employee' in value('url_args'):
      _html += btnDOCX
    return _html

#Metodo usado para el final screen de las entrevistas el cual se usa en las entrevistas V1
#Evalua si en la URL viene el ID de empleado y asi mostrar botones de descarga
#Si es un cliente muestra el boton de confirmar y pagar    
def  get_callback_final_screen(price, identifier, name, production = False):
  if production and 'employee' not in value('url_args'):
    return '<b>Precio del documento: </b><b class="da-price text-left">'+price+'</b><br><br><button class="btn add_da_to_cart btn btn-lg btn-block btn-success" data-id="'+identifier+'" data-name="'+name+'">CONFIRMAR Y PAGAR</button>'
  else:
    if production:
      _urlS3 = 'https://juzto.s3.amazonaws.com/documentos/produccion/'+identifier+'_'+name
    else:
      _urlS3 = 'https://juzto.s3.amazonaws.com/documentos/gratis/'+identifier+'_'+name
    btnPDF = '<a href="'+_urlS3+'.pdf" class="btn btn-md btn-block btn-primary btn-da-pdf" target="_blank" download="" style="background: #002888 !important; color: #fff !important;" data-id="'+identifier+'" data-name="'+name+'"><i class="far fa-file-pdf"></i> PDF</a>'   
    btnDocx = '<a href="'+_urlS3+'.docx" class="btn btn-md btn-block btn-primary btn-da-docx" target="_blank" download="" style="background: #002888 !important; color: #fff !important;" data-id="'+identifier+'" data-name="'+name+'"><i class="far fa-file-word"></i> DOCX</a>'      
    _html = '<div class="row"><div class="col-md-12">'+btnPDF+'para imprimir; requiere Adobe Reader o una aplicación similar</div></div>'
    if 'employee' in value('url_args'):
      _html += '<div class="col-md-12"><hr>'+btnDocx+'Para editar; requiere Microsoft Word o una aplicación compatible</div></div>'
    return _html

#Metodo usado en el final screen cuando la entrevista es gratuita
def get_text_final_screen_free(name):
  return 'Hemos generado tu <b class="da-price">'+name.capitalize()+'</b>. Para verlo, descárgalo en cualquiera de los siguientes formatos:'
#  return 'Hemos generado tu <b class="da-price">'+name.capitalize()+'</b> y el documento esta disponible en los siguientes formatos.'

#Metodo que retorna en formato texto el valor-number recibido en cantidad de días años meses
def get_period_format(number, text):
  _data = {'days':'días', 'months': 'meses', 'years':'años', 'day':'día', 'month': 'mes', 'year':'año'}
  num = number
  if isinstance(number, float):
    num = int(number)
  elif isinstance(number, str):
    num = int(number)
  if num <= 1:
    return _data[text[:-1]]
  else:
    return _data[text]

#Metodo usado para reemplacer el metodo nativo de Jquery val, no se usa
def validateConditional(variable, compare, _type):
  if _type == 'in':
    return variale in compare
  elif _type == 'equal':
    return variable == compare
  elif _type == 'lambda':
    if filter(lambda x: variable in x, compare):
      return True
    else:
      return False

#Metodo usado para pasar horas del formato 24 a 12
def get_12hour(ymlhour):
  _time = ymlhour.strftime("%H:%M")
  ymlhour.strftime("%H:%M:%S")
  t = time.strptime(_time, "%H:%M")
  timevalue_12hour = time.strftime( "%I:%M %p", t )
  return timevalue_12hour

#Metodo utilizado para formatear un número-i en miles 1000 pasa a 1.000
def validationMilles(i):
  s=str(i)
  str1=""
  s1=[elm for elm in s]
  if len(s1)%3==0:
    for i in range(0,len(s1)-3,3):
      str1+=s1[i]+s1[i+1]+s1[i+2]+"."
      str1+=s1[i]+s1[i+1]+s1[i+2]
      return str1  
  else:
    rem=len(s1)%3
    for i in range(rem):
      str1+=s1[i]
    for i in range(rem,len(s1)-1,3):
      str1+="."+s1[i]+s1[i+1]+s1[i+2]
    return str1

#Metodo usado para pasar un nùmero-value a formato moneda 1000 pasa a $1.000
def juztoThousand(value, sign = False):
  ensure_definition(value)
  value = get_only_number(value)
  if sign == True:
    _value = '${:,.0f}'.format(value)
  else:
    _value = '{:,.0f}'.format(value)
  return str(_value).replace(',', '.')

#Metodo usado para pasar la parte decimal de un número-num
def half_plus_one(num):
  divide = num/2
  roundNum = math.ceil(divide)
  return roundNum

#Metodo que se usaba para enviar el correo en el final screen por medio de SendGrid
def send_email_juzto(data, to, emailtype):
  message = Mail(
        subject='Aquí ésta el enlace en el que puedes continuar tu entrevista '+data['interview'],
        from_email='info@juzto.co',
        to_emails=[(to)])
  message.dynamic_template_data = data
  if emailtype == 'leave':
    message.template_id = 'd-c26a86527c064f7ea996a34ba2ba9121'
  else:
    return False
  sg = SendGridAPIClient('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')
  response = sg.send(message)  
  return str(response.status_code)

#Metodo usado para obtener la cantidad meses que faltan de un año
def monthRange(_year, _months):
    monthRanges = calendar.monthrange(_year,_months)
    return monthRanges[1]

#Metodo que crea la tabla-html o lista-docx de intereses para el pagaré, esta tabla evalua el periodo, tiempo, dinero y TEA
def get_table_interest(money, period, _time, _date, _rate, _feeds = [], _template = False):
  _TEA = TEA
  _datainterest = []
  if _rate != 0:
    _TEA = _rate/100
  _incre = 1/12
  if period == 'Cada 2 meses':
    _incre = 1/6   
  elif period == 'Cada 3 meses':  
    _incre = 1/4
  elif period == 'Cada 6 meses':  
    _incre = 1/2  
  elif period == 'Cada año':
    _incre = 1
  TEM = ((pow((1+_TEA), _incre))-1)
  qty = get_times(period, _time)
  pv = npf.pv(TEM, len(qty), -1)
  _html = '<table class="table table-responsive table-striped table-hover '+repr(_TEA)+' '+repr(_rate)+'"><thead><tr><th># Cuota</th><th>Fecha</th><th>Valor</th><th>Interes</th><th>Total</th></tr></thead><tbody>'  
  _quote = money
  if len(_feeds) == 0:
    i = 0
    _x = 1
    _feed = money/len(qty)
    for item in qty:
      if _x != 1:
        _date = _date + date_interval(months=int(item))
      _price = round((money/pv),2)
      _interest = _quote * TEM
      _quote = _quote - _feed 
      _real = _feed + _interest
  #    _html += '<tr><td>'+repr(i)+'</td><td>'+_date.format('d/MM/YYYY')+'</td><td>'+currency(_price)+'</td><td class="text-danger">'+currency(_interest)+'</td><td class="text-success">'+currency(_real)+'</td></tr>'
      _datainterest.insert(i, [_date.format('d/MM/YYYY'), currency(_feed), currency(_interest), currency(_real)])
      _html += '<tr class="tbl-a"><td>'+repr(_x)+'</td><td>'+_date.format('d/MM/YYYY')+'</td><td class="text-success">'+currency(_feed)+'</td><td class="text-danger">'+currency(_interest)+'</td><td>'+currency(_real)+'</td></tr>'
      i = i+1
      _x = _x+1
  else:
    j = 0
    for item in _feeds:
      if j != 0:
        _date = _date + date_interval(months=int(qty[j]))
      _price = round((money/pv),2)
      _interest = _quote * TEM
      _xprice = get_only_number(item.price_x_fee)
      _quote = _quote - _xprice
      _real = _xprice + _interest
      _html += '<tr class="tbl-b"><td>'+repr(j+1)+'</td><td>'+_date.format('d/MM/YYYY')+'</td><td class="text-success">'+currency(_xprice)+'</td><td class="text-danger">'+currency(_interest)+'</td><td>'+currency(_real)+'</td></tr>'
      _datainterest.insert(j, [_date.format('d/MM/YYYY'), currency(_xprice), currency(_interest), currency(_real)])
      j = j+1
  _html += '</tbody></table>'
  if _template:
    return _datainterest
  else:  
    return _html

#Metodo que evalue la cantidad de cuotas para el pagaré, evalua el periodo y tiempo
#Tiene en cuenta si la cantidad de cuotas no caben en el tiempo, agrega una cuota màs
#En el tiempo disponible sin superar el tiempo
def get_times(period, _time):
  _incre = 1
  if period == 'Cada 2 meses':
    _incre = 2    
  elif period == 'Cada 3 meses':  
    _incre = 3
  elif period == 'Cada 6 meses':  
    _incre = 6  
  elif period == 'Cada año':
    _incre = 12
  _last = _time/_incre
  _odd = False
  dec = str(_last).split('.')
  if isinstance(_last, float) and int(dec[1]) != 0:
    _time = math.ceil(_last)
    _odd = True
  else:    
    _time = int(_last)
  _times = []  
  for item in range(0, _time):    
    if _odd and item == _time - 1:
      _times.insert(item, 1)
    else:
      _times.insert(item, _incre)
  return _times    

#Metodo que calcula fecha de pago de una cuota
def get_calculate_date(_date, _times, position):
  _pos = position+1
  for i in range(0, _pos):
    if i != 0:
      _date = _date + date_interval(months=int(_times[i]))
  return _date

#Metodo que crea la tabla-html o lista-docx de cuotas para el pagaré, esta tabla evalua el periodo, tiempo, dinero
def get_table_fees(total, period, first_date, _time, template = False):  
  _incre = 1
  _data = []
  if period == 'Cada 2 meses':
    _incre = 2    
  elif period == 'Cada 3 meses':  
    _incre = 3
  elif period == 'Cada 6 meses':  
    _incre = 6  
  elif period == 'Cada año':
    _incre = 12
  _last = _time/_incre
  _odd = False
  dec = str(_last).split('.')
  if isinstance(_last, float) and int(dec[1]) != 0:
    _time = math.ceil(_last)
    _odd = True
  else:    
    _time = int(_last)
  price = juztoThousand(total/_time, 1)    
  _html = '<table class="table table-responsive table-striped table-hover '+repr(_time)+'"><thead><tr><th># Cuota</th><th>Fecha</th><th>Valor</th></tr></thead><tbody>'
  _date = first_date
  for item in range(0, _time):
    if _odd and item == _time - 1:
      _date = _date + date_interval(months=int(1))
    elif item != 0:
      _date = _date + date_interval(months=int(_incre))
    _html += '<tr><td>'+repr(item+1)+'</td><td>'+_date+'</td><td>'+price+'</td></tr>'
    _data.insert(item, [_date, price])
  _html += '</tbody></table>'
  if template:
    return _data
  else:
    return _html

#Metodo que retorna si una lista en su totalidad de valores es plural o singular
def pluralValue(_list, _conector, _word):
  if len(_list) > 1:
    return _conector+'s '+_word+'s'
  else:
    return _conector+' '+_word

#Metodo que retorna documento para persona natural con formato de miles 
def get_dni_formated(dni):
  if not '.' in dni: 
    r1 = re.match(r"[a-zA-Z][a-zA-Z]\d+",dni)
    if r1:
      if r1.span()[0]==0 and r1.span()[1]==len(dni):
        output = dni
      else: 
        output = format(int(dni), "8,d").replace(',', '.')
    else:
      output = format(int(dni), "8,d").replace(',', '.')
  else:
    output = dni
  return output

#Metodo para la nueva revocatoria directa 
def before_fecha_revocatoria(resolution_date):
  if isinstance(resolution_date, str):
    fecha1 = date(2020, 2, 6)
    fecha2 = datetime.strptime(resolution_date, '%Y-%m-%d').date()
    if fecha2 >= fecha1:
        return True
    else:
        return False
  else:
    #2020, 2, 6
    fecha = as_datetime('2/6/2020')
    #fecha2 = datetime.strptime(resolution_date, '%Y-%m-%d').date()
    if resolution_date >= fecha:
      return True
    else:
      return False