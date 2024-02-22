/*Archivo JavaScript encargado de realizar operaciones en el cliente-navegador de formato, validación y peticiones AJAX*/
/*Variables globales de tipo texto, para determinar cada uno de los tipos de documentos que tipo de valor es text, number, patterns de contenido, el tipo de formato que se aplicara y tamaños para cada uno de ellos*/
_types = {'CC':'text','CE':'number','PA':'text','TI':'text','NUIP':'text','RC':'number','NIT':'text','PEP':'number', 'CASH':'text'};
_patterns = {'CC':'[0-9.]+','CE':'[0-9]+','PA':'[A-Za-z0-9]+','TI':'[0-9.]+','NUIP':'[0-9.]+','RC':'[0-9]+','NIT':'[0-9.]+','PEP':'[0-9]+', 'CASH':'[0-9.]+'};
_formats = {'CC':'point','CE':'number','PA':'text','TI':'point','NUIP':'point','RC':'number','NIT':'nit','PEP':'number', 'CASH':'point'};
_sizes = {'CC':15,'CE':6,'PA':10,'TI':15,'NUIP':15,'RC':15,'NIT':11,'PEP':15};
//variable global que contiene estructura HTML para la validación de error y formato para los campos NIT
var _html_nit = '<span class="caret-nit">_</span><input type="number" class="inp-verificode form-control" placeholder="#" disabled="disabled" class="form-control"><span class="nit-error text-warning"></span><small class="info-nit">*Ingresar sin puntos ni espacios.<br>**El sistema calcula automáticamente el dígito de verificación.</small>';
//var params = window.location.search.substring(1).split("&").map(v => v.split("=")).reduce((map, [key, value]) => map.set(key, decodeURIComponent(value)), new Map());
//Variable que separa la URL por el valor que se decida y asi crea una lista con asiganación key => value
var params = window.location.href.split('&').map(v => v.split("=")).reduce((map, [key, value]) => map.set(key, decodeURIComponent(value)), new Map());
//Variables globales para los sitios de producción y desarrollo
var urlWP = 'https://juzto.co';
var urlDev = 'https://dev.documentoslegales.co';
$(document).ready(function(){
  checkSection();
  //Se oculta el loader por defecto de DA
  $('.daloaderjuzto').hide();
  //Se ajustan clases de los contenedores de cada pantalla de la entrevista, se usa la convención de grillas de BootStrap
  if($('.danavdiv').length){
    $('.danavdiv').removeClass('col-xl-2 col-lg-3 col-md-3').addClass('col-xl-3 col-lg-4 col-md-4');
  }
  if($('#daquestion').length){
    $('#daquestion').removeClass('col-xl-6 col-lg-6 col-md-9').addClass('col-xl-7 col-lg-7 col-md-7');
  }
  if($('.visually-hidden').length){
    $('.visually-hidden').removeClass('visually-hidden').addClass('sr-only');
  }
});
//Evento que se ejecuta cada vez que se carga una pantalla de entrevista
$(document).on('daPageLoad', function(){
  //Se cambia el texto que contiene el mensaje de ayuda de los contenedores para firmar
  $('div.file-drop-zone-title').text('Arrastra y suelta aquí los archivos ...');
  //Funcionalidades JS para la paginación, estructura HTNL y estilos del preview para las entrevistas V2 que lo tengan asignado
  if($('.dawideimage').length){
    _total = $('.dawideimage').length;
    _num = 20*_total;
    _percen = Math.floor(100/_num);
    _percen = (_percen < 3 && _percen > 1)?_percen:3;
    $('.dawideimage').hide();
    $('.dawideimage:eq(0)').show();
    $('.dawideimage').each(function(i, e){
      if(i >= _percen){
          $(e).css({'-webkit-filter':'blur(5px)', 'filter':'blur(5px)', 'display':'none'});
      }else{
         $('.back_page').html('');
      }
    });
    $('.back_page, .next_page').click(function(){
      if($(this).html().length){
      _num = parseInt($('.number_page:eq(0)').text());
      _pos = ($(this).hasClass('back_page'))?_num-1:_num+1;
      if(_pos > 1)
        $('.back_page').html('<i class="fa fa-chevron-left" aria-hidden="true">');
      else
        $('.back_page').html('');
      if(_pos == 1)
        $('.next_page').html('<i class="fa fa-chevron-right" aria-hidden="true">');
      else if(_num == $('.dawideimage').length - 1)
        $('.next_page').html('');
      else
        $('.next_page').html('<i class="fa fa-chevron-right" aria-hidden="true">');
      console.log(_num, $('.dawideimage').length - 1, _pos);
      if(_num >= 1 && _num <= $('.dawideimage').length){
        $('.dawideimage').hide();        
        if(_pos > 0){
          $('.dawideimage:eq('+(_pos-1)+')').removeClass('hide').show();
          $('.number_page').text(_pos);
        }
      }
      }
    });
    
  }
  //Volvemos a ocultar el loader de DA ya que se habilita por cada evento click, change, blur etc en las pantallas
  $('.daloaderjuzto').hide();
  //Agrega clase para estilos del ancla en la parte de abajo de las entrevistas para reset de la entrevista
  $('.daundertext').find('a:eq(1)').addClass('destroy-interview');
  //Se fuerzan clases y cambios de CSS a algunos componentes de DA
  if(jQuery(".progress").length)
    jQuery('html, body').animate({scrollTop: $(".progress").offset().top - 200 });
  if(jQuery('.page-id-44388').length){
    jQuery('#daquestion').prop('style', 'margin-left: 12% !important');
    jQuery('.mt-2').prop('style', 'width: 140% !important');
    jQuery('#daform').prop('style', 'width: 140% !important');
    //jQuery('.da-page-header').prop('style', 'width: 140% !important');
  }       
  //Script de validación de la existencia y carga de imagenes de las entrevistas, sino cargan se remueven
  //Para no mostrar imagenes rotas
  if($('#dablock img').length){
    $('#dablock img').each(function(i, e){
      if($(e).prop('src').indexOf('https://doc.juzto.co/') < 0)
        $(e).prop('src', 'https://doc.juzto.co/'+$(e).attr('src'));
    });
  }
  checkSection();
  //Se ajustan clases de los contenedores de cada pantalla de la entrevista, se usa la convención de grillas de BootStrap
  if($('.danavdiv').length){
    $('.danavdiv').removeClass('col-xl-2 col-lg-3 col-md-3').addClass('col-xl-3 col-lg-4 col-md-4');
  }
  if($('#daquestion').length){
    $('#daquestion').removeClass('col-xl-6 col-lg-6 col-md-9').addClass('col-xl-7 col-lg-7 col-md-7');
  } 
  if($('.visually-hidden').length){
    $('.visually-hidden').removeClass('visually-hidden').addClass('sr-only');
  }
 
  //Script que valida si la entrevista ha llegado al final screen y asi crear un arreglo
  //Que se compone de datos importantes para el corrector almacenamiento del documento por sesión WP y DA
  if($('.add_da_to_cart').length || $('.btn-da-pdf').length || $('.btn-da-docx').length){
    console.log('[ FINAL SCREEN ]');
    $('.add_da_to_cart, .btn-da-pdf, .btn-da-docx').click(function(){
      _sku = ($('#dablock').length)?$('#dablock').data('sku'):params.get('sku');
      _id_product = ($('#dablock').length)?$('#dablock').data('product'):params.get('product');
      _free = 1;
      if($('#dablock').length){
        if($('#dablock').data('price') != 0){
          _free = 0;
        }
      }
      _data = {
        'action': 'insertdawpregister',
        'callback': 'jQuery331012076964487862507_1587513268325',
        'hash_wp':_sku,
        'id_product':_id_product,
        'hash_da':$(this).data('id'),
        'name':$(this).data('name'),
        'free':_free,
        'customer': $('#dablock').data('customer')
      };
      console.log(_data, urlWP+'/wp-admin/admin-ajax.php');
      sendRequestAjax(urlWP+'/wp-admin/admin-ajax.php', _data, 'GET', 'json');            
    });    
  }
});

//Metodo encargado de las peticiones AJAX y comunicación entre WP y DA
function sendRequestAjax(_url,_data, _type, _dataType){
  $.ajax({
    url: _url,
    crossOrigin: true,  
    crossDomain: true, 
    data: _data,
    type: _type,
    headers: {'Accept': 'application/json'},
    //contentType: 'application/json',
    dataType: _dataType,
    //headers: {'Access-Control-Allow-Origin': '*'},
    //async: false,
    beforeSend: function( d ) {
      console.log( 'AJAX Before send', d );
    }}).done(function( response, textStatus, jqXHR ){
      console.log( 'AJAX done', _data, textStatus, jqXHR, jqXHR.getAllResponseHeaders() );      
    }).fail(function( jqXHR, textStatus, errorThrown ){
      console.log( 'AJAX failed', jqXHR.getAllResponseHeaders(), textStatus, errorThrown );
      console.log('Lo sentimos, algo ha fallado, por favor intentalo mas tarde.');
    }).then(function( jqXHR, textStatus, errorThrown ){
      console.log( 'AJAX after', jqXHR, textStatus, errorThrown );      
    //if(_data['free'] == 0){
      $('.add_da_to_cart').html('<i class="fa fa-circle-o-notch fa-spin fa-2x fa-fw"></i><span class="sr-only">Loading...</span>').attr('disabled', 'disabled');    
      parent.postMessage("myevent", "*");
    //}
  });      
}

//Metodo que se ejecuta en cada carga de pantalla de las entrevistas
//Este se encarga de dar formato y cambio a los inputs que tengan el placeholder DNI
//Asigna un nuevo placeholder, pattern de contenido, tamaño, tipo de contenido
//y asigan el evneto para ir a la correspondiente validación
function checkSection() {
  console.log('[ START ] in check section');
  //if($('.question-blockglobal').length){
    $('input').each(function(inx, elem){
      //console.log($(elem).attr('type'));
      if($(elem).attr('type') == 'text'){
      switch($(elem).attr('placeholder')){
        case 'dni':
          _inp = $(elem);
          console.log('[ BLOCK ] DNI');          
          _con = _inp.parents('.form-group');
          if(_con.parent().attr('class') == 'form-horizontal')
            _sel = _con.prev().find('select'); 
          else
            _sel = _con.parent().prev().find('select');
          if($(elem).val() == '')
            _con.hide();
          _sel.on('change', {inp:_inp}, validateDni);
          _inp.on('keyup', {pos:0}, formatDniVal);
          _inp.css('text-transform', 'uppercase');
          break;
        case 'nit':
          _inp = $(elem);
          console.log('[ BLOCK ] NIT');
          _con = _inp.parents('.form-group')
          _pos = 'NIT';
          _inp.attr('placeholder', 'Ingrese Número de indentificación tributaria (NIT)');
          _inp.attr('type', _types[_pos]);
          _inp.attr('maxlength', _sizes[_pos]);
          _inp.attr('minlength', _sizes[_pos]);
          _inp.attr('pattern', _patterns[_pos]);
          _inp.addClass('inp-nit');
          _con.addClass('container-nit');
          _con.find('input').parent().append(_html_nit);
          _inp.on('keyup', {pos:'NIT'}, formatDniVal);
          _inp.css('text-transform', 'uppercase');
          break;
        case 'money':
          _inp = $(elem);
          console.log('[ BLOCK ] MONEY');
          _inp.removeAttr('step');
          _con = _inp.parents('.form-group')
          _pos = 'CASH';
          _inp.attr('placeholder', '0.000.000');
          _inp.attr('type', _types[_pos]);
          _inp.attr('maxlength', _sizes[_pos]);
          _inp.attr('pattern', _patterns[_pos]);
          _inp.on('keydown', {pos:'CASH'}, formatDniVal);
          _inp.on('keyup', {pos:'CASH'}, formatDniVal);
          _inp.css('text-transform', 'uppercase');
          break;
        default:          
          console.log('[ NO MATCH TO EVALUATE ]');
          //console.log('[ '+$(elem).attr('placeholder')+' ] NO MATCH TO EVALUATE');
          break;
      }
      }
    });
  //}
}

//Metodo encargado de dar formato de los tipos de documentos
//cada vez que se ingresa un valor en los inputs que tengan este evento
//Da formato a las cedulas,monedas separandolas por miles, y agrega el digito de verificación al NIT
function formatDniVal( e ){  
  if(e.data.pos != 0){
    _pos = e.data.pos;
  }else{
    if($(this).parents('.form-group').parent().attr('class') == 'form-horizontal')
       _pos = $(this).parents('.form-group').prev().find('select').val();
    else
       _pos = $(this).parents('.form-group').parent().prev().find('select').val();
  }
  console.log("[ DNI ] formatDniVal => "+_pos); 
  _val = $(this).val().split(' ').join('');
  _real_val = _val.split('.').join('');
  switch(_formats[_pos]){
    case 'point':                
      _real_val = (isNaN(_real_val))?'':Number(_real_val).toLocaleString('Es-co');
      $(this).val(_real_val);
      break;
    case 'nit':        
      _real_val = (isNaN(_real_val))?'':Number(_real_val).toLocaleString('Es-co');
      $(this).val(_real_val);
      if(_real_val.length == 11 ){
        $('.inp-verificode').val(generateVerificationCode( _real_val ))
      }else{
        $('.inp-verificode').val('');
        $('.nit-error').html('Ingresa los 9 digitos del NIT');
        setTimeout(function(){$('.nit-error').html('');},4000);
      }
      break;
    default:
      console.log('User input anything');
      break;
  }    
}
//Metodo encargado de la validación de los tipos de documentos
//Bloquea los campos para no superar el tamaño, evita el ingreso de digitos no permitidos
function validateDni( e ){  
  _pos = $(this).val();
  console.log("[ DNI ] validate >>> "+_pos);
  if(_pos != ''){
  _inp = e.data.inp;
    console.log(_inp.attr('id'));
  _con = _inp.parents('.form-group');
  //_inp.val('');  
  _place = 'Ingrese '+$(this).find('option:selected').text();
  _inp.attr('placeholder', _place);
  _inp.attr('style', 'max-width: 100%;');
  _con.find('.caret-nit').remove();
  _con.find('.inp-verificode').remove();
  _con.find('.info-nit').remove();
  _inp.attr('type', _types[_pos]);
  _inp.attr('maxlength', _sizes[_pos]);
  _inp.attr('pattern', _patterns[_pos]);
  _inp.parents().show();
  if(_pos == 'NIT'){
    _inp.addClass('inp-nit');
    _con.addClass('container-nit');   
    $('.container-nit .col').append(_html_nit);
  }else{
    _inp.removeClass('inp-nit');
    _con.removeClass('container-nit');
  } 
  _inp.focus();
  }
}
//Metodo encargado de validar y retornar el digito de verificaciòn de los NIT
function  generateVerificationCode( myNit )  {
    var vpri,x,y,z;
    myNit = myNit.replace ( /\s/g, "" ) ; // Espacios
    myNit = myNit.replace ( /,/g,  "" ) ; // Comas
    myNit = myNit.replace ( /\./g, "" ) ; // Puntos
    myNit = myNit.replace ( /-/g,  "" ) ; // Guiones

    if  ( isNaN ( myNit ) )
        return "" ;

    vpri = new Array(16) ;
    z = myNit.length ;

    vpri[1]  =  3 ;
    vpri[2]  =  7 ;
    vpri[3]  = 13 ;
    vpri[4]  = 17 ;
    vpri[5]  = 19 ;
    vpri[6]  = 23 ;
    vpri[7]  = 29 ;
    vpri[8]  = 37 ;
    vpri[9]  = 41 ;
    vpri[10] = 43 ;
    vpri[11] = 47 ;
    vpri[12] = 53 ;
    vpri[13] = 59 ;
    vpri[14] = 67 ;
    vpri[15] = 71 ;

    x = 0 ;
    y = 0 ;
    for  ( var i = 0; i < z; i++ )  {
        y = ( myNit.substr (i, 1 ) ) ;
        x += ( y * vpri [z-i] ) ;
    }
    y = x % 11 ;

    return ( y > 1 ) ? 11 - y : y ;
}

//Metodo de validación creado para reemplazar el metodo por defecto de Jquey val, no se usa
function compareJuzto(_var, _compare, _type){
  console.log(_var, _compare, _type);
  switch(_type){
      case 'in':
        return _compare.includes(_var);
      break;
    case 'or':
        if (Array.isArray(_compare) && _compare.length) 
          return true; 
        else
          return _var == false || _var == true
      break;
    case 'and':
        return _var[0] == _compare[0] && _var[1] == _compare[1]
      break;  
    default:
        return false;
      break;
  }
}