# -*- coding: utf-8 -*-
#
#Copyright (C) 2010-2012, Yader Velasquez
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sugar.activity import activity, widgets
import gtk
import logging
from gettext import gettext as _
from os.path import exists
from datetime import datetime
import os
import pickle
import utils
import pango

_logger = logging.getLogger('sindiente-activity')

class Sindiente(activity.Activity):

    def __init__(self, handle):
        super(Sindiente, self).__init__(handle)
        #ventana
        self.nivel = None
        self.set_title(_('Sin Dientes'))
        self.carpeta_imagen = 'resources/personaje_'
        self.sugar_data = self.get_activity_root() + '/data/'
        self.connect('key-press-event', self._key_press_cb)

        #Barra de herramientas sugar

        toolbox = widgets.ActivityToolbox(self)
        self.set_toolbar_box(toolbox)
        toolbox.show()
        
        #general
        self.comprobar_interfaz = False
        self.modificar_text = pango.FontDescription("Bold 10")
        self._archivo_sugar()

        #contenedores
        self.contenedor = gtk.VBox()
        self.contenedor_superior = gtk.HBox()
        self.contenedor_inferior= gtk.HBox()
        self.contenedor.pack_start(self.contenedor_superior)
        self.contenedor.pack_start(self.contenedor_inferior, expand=False)
        self.subcontenedor= gtk.VBox()
        self.contenedor_nivel = gtk.VBox()
        self.contenedor_nivel_1 = gtk.VBox()
        self.contenedor_nivel_2 = gtk.VBox()
        self.contenedor_instruc = gtk.VBox()
        self.contenedor_instruc_1 = gtk.HBox()
        self.contenedor_instruc_2 = gtk.HBox()
        self.contenedor_instruc_3 = gtk.HBox()
        self.contenedor_instruc_4 = gtk.HBox()
        self.contenedor_np_v = gtk.VBox()
        self.contenedor_np_1 = gtk.HBox()
        self.contenedor_np_2 = gtk.HBox()

        #Elegir personaje
        self.elegir_personaje_v = gtk.VBox()
        self.elegir_personaje_1 = gtk.HBox()
        self.elegir_personaje_2 = gtk.HBox()
        self.boton_personaje_1 = gtk.HBox()
        self.boton_personaje_2 = gtk.HBox()

        self.text_boton_nino = _('Elegir')
        self.btn_nino_1 = gtk.Button(self.text_boton_nino)
        self.btn_nino_2 = gtk.Button(self.text_boton_nino)
        self.btn_nino_3 = gtk.Button(self.text_boton_nino)
        self.btn_nina_1 = gtk.Button(self.text_boton_nino)
        self.btn_nina_2 = gtk.Button(self.text_boton_nino)
        self.btn_nina_3 = gtk.Button(self.text_boton_nino)
        self.btn_nino_1.connect('clicked', self._btn_nino_1_cb)   
        self.btn_nino_2.connect('clicked', self._btn_nino_2_cb)
        self.btn_nino_3.connect('clicked', self._btn_nino_3_cb)
        self.btn_nina_1.connect('clicked', self._btn_nina_1_cb) 
        self.btn_nina_2.connect('clicked', self._btn_nina_2_cb)
        self.btn_nina_3.connect('clicked', self._btn_nina_3_cb)

        #niños
        self.personaje_label = gtk.Label(_("Elige un personaje"))
        self.personaje_label.modify_font(self.modificar_text)
        self.nino_1 = gtk.Image()
        self.nino_1.set_from_file('resources/personaje_1/00.png')
        self.nino_2 = gtk.Image()
        self.nino_2.set_from_file('resources/personaje_2/00.png')
        self.nino_3 = gtk.Image()
        self.nino_3.set_from_file('resources/personaje_3/00.png')

        self.nina_1 = gtk.Image()
        self.nina_1.set_from_file('resources/personaje_4/00.png')
        self.nina_2 = gtk.Image()
        self.nina_2.set_from_file('resources/personaje_5/00.png')
        self.nina_3 = gtk.Image()
        self.nina_3.set_from_file('resources/personaje_6/00.png')

        self.boton_personaje_1.pack_start(self.btn_nino_1, True, False)
        self.boton_personaje_1.pack_start(self.btn_nino_2, True, False)
        self.boton_personaje_1.pack_start(self.btn_nino_3, True, False)
        self.boton_personaje_2.pack_start(self.btn_nina_1, True, False)
        self.boton_personaje_2.pack_start(self.btn_nina_2, True, False)
        self.boton_personaje_2.pack_start(self.btn_nina_3, True, False)

        self.elegir_personaje_1.pack_start(self.nino_1)
        self.elegir_personaje_1.pack_start(self.nino_2)
        self.elegir_personaje_1.pack_start(self.nino_3)
        self.elegir_personaje_2.pack_start(self.nina_1)
        self.elegir_personaje_2.pack_start(self.nina_2)
        self.elegir_personaje_2.pack_start(self.nina_3)

        self.elegir_personaje_v.pack_start(self.personaje_label)
        self.elegir_personaje_v.pack_start(self.elegir_personaje_1)
        self.elegir_personaje_v.pack_start(self.boton_personaje_1, False)
        self.elegir_personaje_v.pack_start(self.elegir_personaje_2)
        self.elegir_personaje_v.pack_start(self.boton_personaje_2, False)
        self.elegir_personaje_v.show_all()
        self.set_canvas(self.elegir_personaje_v)

        #interface menu 
        self.imagen_menu = gtk.Image()
        self.nivel_1 = gtk.Button(_('Animales'))
        self.nivel_1.connect('clicked', self._nivel_uno_cb, None)
        self.nivel_2 = gtk.Button(_('Plantas'))
        self.nivel_2.connect('clicked', self._nivel_dos_cb, None)
        self.nivel_3 = gtk.Button(_('Países'))
        self.nivel_3.connect('clicked', self._nivel_tres_cb, None)
        self.nivel_4 = gtk.Button(_('Sustantivos'))
        self.nivel_4.connect('clicked', self._nivel_cuatro_cb, None)
        self.nivel_5 = gtk.Button(_('Verbos'))
        self.nivel_5.connect('clicked', self._nivel_cinco_cb, None)
        self.nivel_6 = gtk.Button(_('Cosas'))
        self.nivel_6.connect('clicked', self._nivel_seis_cb, None)
        self.nivel_7 = gtk.Button(_('Valores Morales'))
        self.nivel_7.connect('clicked', self._nivel_siete_cb, None)
        self.importar_btn = gtk.Button(_('Agregar lista de palabra'))
        self.importar_btn.connect('clicked', self._importar_cb, None)
        self.instrucciones = gtk.Button(_('Instrucciones de juego'))
        self.instrucciones.connect('clicked', self._instrucciones_cb, None)
        self.nuevapalabra_btn = gtk.Button(_('Modo Versus'))
        self.nuevapalabra_btn.connect('clicked', self._nuevapalabra_cb, None)
        self.cambiar_personaje_btn = gtk.Button(_('Cambiar personaje'))
        self.cambiar_personaje_btn.connect('clicked', self._cambiar_personaje_cb)
        self.categoria_libre = gtk.Button(_('Categoría Personalizada'))
        self.categoria_libre.connect('clicked', self._categoria_personalizada_cb)
        self.bienvenida = gtk.Label(_('Bienvenido a \"Sin Diente\"'))
        self.bienvenida.modify_font(self.modificar_text)

        #agregando elementos de menú
        self.contenedor_nivel_h = gtk.HBox()
        self.contenedor_nivel.pack_start(self.bienvenida, False, padding = 15)
        self.contenedor_nivel.pack_start(self.imagen_menu, False, padding = 15)
        self.contenedor_nivel.pack_start(self.contenedor_nivel_h)
        self.contenedor_nivel_h.pack_start(self.contenedor_nivel_1, padding = 20)
        self.contenedor_nivel_h.pack_start(self.contenedor_nivel_2, padding = 20)
        self.contenedor_nivel_1.pack_start(self.nivel_1, False, padding = 10)
        self.contenedor_nivel_1.pack_start(self.nivel_2, False, padding = 10)
        self.contenedor_nivel_1.pack_start(self.nivel_3, False, padding = 10)
        self.contenedor_nivel_1.pack_start(self.nivel_4, False, padding = 10)
        self.contenedor_nivel_1.pack_start(self.cambiar_personaje_btn, False, padding = 10)
        self.contenedor_nivel_1.pack_start(self.instrucciones, False, padding = 10)
        self.contenedor_nivel_2.pack_start(self.nivel_5, False, padding = 10)
        self.contenedor_nivel_2.pack_start(self.nivel_6, False, padding = 10)
        self.contenedor_nivel_2.pack_start(self.nivel_7, False, padding = 10)
        self.contenedor_nivel_2.pack_start(self.nuevapalabra_btn, False, padding = 10)
        self.contenedor_nivel_2.pack_start(self.importar_btn, False, padding = 10)
        self.contenedor_nivel_2.pack_start(self.categoria_libre, False, padding = 10)
        self.contenedor_nivel.show_all()
        
        #interface juego
        self.imagen = gtk.Image()
        self.instrucciones_label = gtk.Label()
        #self.instrucciones_label.set_justify(gtk.JUSTIFY_FILL)
        self.instrucciones_label.modify_font(self.modificar_text)
        #self.aciertos_label = gtk.Label(_('Puntaje: 0'))
        self.errores_label = gtk.Label()
        self.errores_label_2 = gtk.Label()
        self.errores_label_2.modify_font(self.modificar_text)
        self.palabra_label = gtk.Label()
        self.definicion_label = gtk.Label()
        self.definicion_label.modify_font(self.modificar_text)
        self.definicion = gtk.Label()
        self.definicion.set_line_wrap(True)
        self.pista_label = gtk.Label()
        self.pista_label.modify_font(self.modificar_text)
        self.pista = gtk.Label()
        self.pista.set_line_wrap(True)
        #self.pista.set_max_width_chars(0)
        self.letrasusadas_label = gtk.Label()
        self.letrasusadas_label_2 = gtk.Label()
        self.letrasusadas_label_2.modify_font(self.modificar_text)
        self.palabra_entry = gtk.Entry()
        self.ok_btn = gtk.Button(_('Ingresar'))
        self.ok_btn.connect('clicked', self._ok_btn_clicked_cb, None)
        self.nuevojuego_btn = gtk.Button(_('Nuevo Juego'))
        self.nuevojuego_btn.connect('clicked', self._nuevojuego_btn_clicked_cb, None)
        self.atras_btn = gtk.Button(_('Atrás'))
        self.atras_btn.connect('clicked', self._atras_cb)
        self.aciertos = 0 #Cuenta los aciertos de letras en la palabra secreta

        #agregando elementos juego
        self.marco = gtk.Frame(_("Instrucciones"))
        self.marco.set_size_request(350, -1)
        self.contenedor_superior.pack_start(self.imagen)
        self.contenedor_superior.pack_start(self.marco)
     
        self.subcontenedor.pack_start(self.instrucciones_label)
        self.subcontenedor.pack_start(self.definicion_label, False, padding = 5)
        self.subcontenedor.pack_start(self.definicion, False, padding = 5)
        self.subcontenedor.pack_start(self.pista_label, False, padding = 5)
        self.subcontenedor.pack_start(self.pista, False, padding = 5)
        #self.subcontenedor.pack_start(self.aciertos_label)
        self.subcontenedor.pack_start(self.errores_label_2, False, padding = 5)
        self.subcontenedor.pack_start(self.errores_label, False, padding = 5)
        self.subcontenedor.pack_start(self.letrasusadas_label_2, False)
        self.subcontenedor.pack_start(self.letrasusadas_label, False)
        self.subcontenedor.pack_start(self.palabra_label)
        self.marco.add(self.subcontenedor)

        self.contenedor_inferior.pack_start(self.atras_btn, False, padding = 6)
        self.contenedor_inferior.pack_start(self.palabra_entry, padding = 1)
        self.contenedor_inferior.pack_start(self.ok_btn, False, padding = 1)
        self.contenedor_inferior.pack_start(self.nuevojuego_btn, False, padding = 1)
               
        #interface instrucciones
        self.area_instruc = gtk.ScrolledWindow()
        self.area_instruc.set_shadow_type(gtk.SHADOW_OUT)
        self.area_instruc.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.imagen_1 = gtk.Image()
        self.imagen_1.set_from_file('resources/sindiente1.png')
        self.imagen_2 = gtk.Image()
        self.imagen_2.set_from_file('resources/sindiente2.png')
        self.imagen_3 = gtk.Image()
        self.imagen_3.set_from_file('resources/sindiente3.png')
        self.imagen_4 = gtk.Image()
        self.imagen_4.set_from_file('resources/sindiente4.png')
        
        self.instruc = gtk.Label(_('Instrucciones'))
        self.instruc.modify_font(self.modificar_text)
        self.instruc_1 = gtk.Label(_('Oprime el botón “Nuevo Juego” para empezar a \njugar.'))
        self.instruc_2 = gtk.Label(_('La lineas representan las letras de las palabras \nque están ocultas. Cuenta las letras se compone \nla palabra.'))
        self.instruc_3 = gtk.Label(_('Ingresa una letra en el espacio en blanco y oprime \nel botón “Ingresar”. Si descubres una letra esta \naparecerá sobre la linea y ganarás un punto.\nPero si fallas, tu amigo perderá un diente.'))
        self.instruc_4 = gtk.Label(_('Las letras que ya han sido ingresadas no podrán ser \nusada de nuevo y aparecerán en el área de "Letras Usadas"'))
        self.atras_btn_1 = gtk.Button(_('Atrás'))
        self.atras_btn_1.connect('clicked', self._atras_cb)

        #agregando elementos de instrucciones
        self.contenedor_instruc_1.pack_start(self.instruc_1)
        self.contenedor_instruc_1.pack_start(self.imagen_1)
        self.contenedor_instruc_2.pack_start(self.imagen_2)
        self.contenedor_instruc_2.pack_start(self.instruc_2)
        self.contenedor_instruc_3.pack_start(self.instruc_3)
        self.contenedor_instruc_3.pack_start(self.imagen_3)
        self.contenedor_instruc_4.pack_start(self.imagen_4)
        self.contenedor_instruc_4.pack_start(self.instruc_4)
        self.contenedor_instruc.pack_start(self.instruc, padding=25)
        self.contenedor_instruc.pack_start(self.contenedor_instruc_1, padding=50)
        self.contenedor_instruc.pack_start(self.contenedor_instruc_2, padding=50)
        self.contenedor_instruc.pack_start(self.contenedor_instruc_3, padding=50)
        self.contenedor_instruc.pack_start(self.contenedor_instruc_4, padding=15)
        self.contenedor_instruc.pack_start(self.atras_btn_1)
        self.area_instruc.add_with_viewport(self.contenedor_instruc)

        #interface nueva palabra
        self.nueva_palabra_label = gtk.Label(_('Ingresa una palabra para jugar'))
        self.nueva_palabra_label.modify_font(self.modificar_text)
        self.n_palabra_label = gtk.Label(_('Palabra'))
        self.nuevo_significado_label = gtk.Label(_('Significado'))
        self.nueva_pista_label = gtk.Label(_('Pista'))
        self.nueva_palabra = gtk.Entry()
        self.nuevo_significado = gtk.Entry()
        self.nueva_pista = gtk.Entry()
        self.boton_np = gtk.Button(_('Ingresar palabra'))
        self.boton_np.connect('clicked', self._nueva_p_cb)
        self.atras_imp = gtk.Button(_('Atrás'))
        self.atras_imp.connect('clicked', self._atras_cb)

        #agregando elementos de nueva palabra
        self.contenedor_np_v.pack_start(self.nueva_palabra_label, False, padding=80)
        self.contenedor_np_v.pack_start(self.n_palabra_label, False)
        self.contenedor_np_v.pack_start(self.nueva_palabra, False, padding=15)
        self.contenedor_np_v.pack_start(self.nueva_pista_label, False)
        self.contenedor_np_v.pack_start(self.nueva_pista, False, padding=15)
        self.contenedor_np_v.pack_start(self.nuevo_significado_label, False)
        self.contenedor_np_v.pack_start(self.nuevo_significado, False, padding=15)
        self.contenedor_np_v.pack_start(self.contenedor_np_1, False, False, 100)
        self.contenedor_np_1.pack_start(self.atras_imp, True, False)
        self.contenedor_np_1.pack_start(self.boton_np, True, False)
        self.contenedor_np_2.pack_start(self.contenedor_np_v, padding=100)

        #interface importar
        self.combo = self.combo = gtk.combo_box_new_text()
        self.combo.set_size_request(180, -1)
        self.combo.append_text(_('Animales'))
        self.combo.append_text(_('Plantas'))
        self.combo.append_text(_('Países'))
        self.combo.append_text(_('Sustantivos'))
        self.combo.append_text(_('Verbos'))
        self.combo.append_text(_('Cosas'))
        self.combo.append_text(_('Valores morales'))
        self.combo.append_text(_('Categoría Personalizada'))
        self.combo.set_active(0)
        self.atras_btn_imp = gtk.Button(_('Atrás'))
        self.atras_btn_imp.connect('clicked', self._atras_cb)
        self.boton_importar = gtk.Button(_('Importar'))
        self.boton_importar.connect('clicked', self._importar_archivo_cb)
        self.archivo = gtk.FileChooserWidget()
        self.archivo.set_current_folder('/media')
        self.niveles = gtk.Label(_('Categorías'))
        self.importar = gtk.HBox()
        self.importar.pack_start(self.atras_btn_imp, False, padding=5)
        self.importar.pack_start(self.niveles, False, padding=10)
        self.importar.pack_start(self.combo, False)
        self.importar.pack_start(self.boton_importar)
        self.archivo.set_extra_widget(self.importar)

        #interface categoria personalizada NONE
        self.sin_importar = gtk.Label(_('No se ha importado ninguna lista de palabras para crear una categoría personalizada'))
         
        self.show()

    def _archivo_sugar(self):
        '''copia los archivos'''
        ruta = self.sugar_data + 'nivel1.palabra'
        if not os.path.exists(ruta): #ningun archivo copiado aún
            for i in range(1,8):
                ruta = self.sugar_data + 'nivel%s.palabra' %i
                _logger.debug(ruta)
                ruta_origen = 'resources/nivel%s.palabra' %i
                _logger.debug(ruta_origen)
                origen = open(ruta_origen, 'r')
                contenido = origen.read()
                destino = open(ruta, 'w')
                destino.write(contenido)
                destino.close()
                origen.close()
        else:
            pass

    def _crear_interfaz_normal(self):
        '''crea la interfaz de juego'''
        self.ok_btn.set_sensitive(False)
        self.palabra_entry.set_sensitive(False)
        self._cambiar_imagen(0)
        if self.comprobar_interfaz:
            self.contenedor_inferior.remove(self.nuevojuego_imp)
            self.contenedor_inferior.pack_start(self.nuevojuego_btn, False, padding = 1)
            self.comprobar_interfaz = False

    def _crear_interfaz_personalidad(self):
        '''crea la interfaz cuando se quire ingresar una palabra personalizada'''
        if self.comprobar_interfaz is not True:
            self._cambiar_imagen(0)
            self.nuevojuego_imp = gtk.Button(_('Nuevo juego'))
            self.nuevojuego_imp.connect('clicked', self._nuevo_juegoimp_cb)
            self.contenedor_inferior.remove(self.nuevojuego_btn)
            self.contenedor_inferior.pack_start(self.nuevojuego_imp, False, padding = 1)
        self.comprobar_interfaz = True

    def _creacion(self, nuevo=True, custom=False):
        '''Crea las variables necesarias para el comienzo del juego'''
        if nuevo:
            if custom:
                self.palabra = self.nueva_palabra.get_text()
                self.texto_pista = self.nueva_pista.get_text()
                self.significado = self.nuevo_significado.get_text()
            else:
                contenido = utils.palabra_aleatoria(self.sugar_data, self.nivel)
                _logger.warning(contenido)
                self.palabra = unicode(contenido[0], "utf-8")
                self.texto_pista = contenido[1]
                self.significado = contenido[2]

            self.l_aciertos = []
            self.l_errores= []
            self.errores = 0
            self._cambiar_imagen(0)
        else:
            self._cambiar_imagen(self.errores)
        
        self._actualizar_labels(_('El juego ha empezado'))
        self._pintar_palabra()
    
    def _limpiar(self):
        '''limpia pantalla'''
        self.palabra_entry.set_sensitive(False)
        self.ok_btn.set_sensitive(False) 
        self.pista_label.set_text('')
        self.pista.set_text('')
        self.definicion_label.set_text('')
        self.definicion.set_text('')
        self.instrucciones_label.set_text('')
        self.palabra_label.set_text('')
        self.errores_label.set_text('')
        self.errores_label_2.set_text('')
        self.letrasusadas_label.set_text('')
        self.letrasusadas_label_2.set_text('')
        self._cambiar_imagen(0)

    #callbacks

    def _btn_nino_1_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '1/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _btn_nino_2_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '2/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _btn_nino_3_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '3/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)
    
    def _btn_nina_1_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '4/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)
    
    def _btn_nina_2_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '5/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)
        
    def _btn_nina_3_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '6/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _atras_cb(self, widget, data=None):
        self.set_canvas(self.contenedor_nivel)
        self._limpiar()

    def _nivel_uno_cb(self, widget, data=None):
        self.nivel = 1
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_dos_cb(self, widget, data=None):
        self.nivel = 2
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_tres_cb(self, widget, data=None):
        self.nivel = 3
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)
    
    def _nivel_cuatro_cb(self, widget, data=None):
        self.nivel = 4
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_cinco_cb(self, widget, data=None):
        self.nivel = 5
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)
    
    def _nivel_seis_cb(self, widget, data=None):
        self.nivel = 6
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)
    
    def _nivel_siete_cb(self, widget, data=None):
        self.nivel = 7
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)
    
    def _categoria_personalizada_cb(self, widget, data=None):
        self.nivel = utils.categoria_personalizada(self.sugar_data)
        if self.nivel:
            self._crear_interfaz_normal()
            self.contenedor.show_all()
            self.set_canvas(self.contenedor)
        else:
            self.sin_importar.show_all()
            self.set_canvas(self.sin_importar)
            #pass #mostrar mensaje

    def _cambiar_personaje_cb(self, widget, data=None):
        self.set_canvas(self.elegir_personaje_v)

    def _instrucciones_cb(self, widget, data=None):
        self.area_instruc.show_all()
        self.set_canvas(self.area_instruc)

    def _importar_cb(self, widget, data=None):
        '''callback del menu'''
        self.archivo.show_all()
        self.set_canvas(self.archivo)

    def _importar_archivo_cb(self, widget, data=None):
        '''importa una nueva lista de palabras'''
        self.modelocombo = self.combo.get_model()
        self.nivel = self.combo.get_active()
        self.uri = self.archivo.get_uri()
        self.uri = self.uri[7:]
        utils.importar_lista_p(self.sugar_data, self.uri, self.nivel)

    def _nuevapalabra_cb(self, widget, data=None):
        '''callback del menu'''
        self.contenedor_np_2.show_all()
        self.set_canvas(self.contenedor_np_2)
    
    def _nueva_p_cb(self, widget, data=None):
        '''ingresar nueva palabra'''
        self._crear_interfaz_personalidad()
        self._creacion(custom=True)
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)
        self.palabra_entry.set_sensitive(True)
        self.ok_btn.set_sensitive(True)
        self.nuevojuego_btn.set_sensitive(True)
        self.nueva_palabra.set_text('')
        self.nuevo_significado.set_text('')
        self.nueva_pista.set_text('')
    
    def _nuevo_juegoimp_cb(self, widget, data=None):
        '''nuevo juego en la interfaz de juego personalizado'''
        self.contenedor_np_2.show_all()
        self.set_canvas(self.contenedor_np_2)
    
    def _ok_btn_clicked_cb(self, widget, data=None):
        self._actualizar_palabra()

    def _nuevojuego_btn_clicked_cb(self, widget, data=None):
        self.palabra_entry.set_sensitive(True) #Activa la caja de texto
        self.ok_btn.set_sensitive(True) #Activa el botón ok
        self.aciertos = 0
        self._creacion()
        
    def _cambiar_imagen(self, level):
        ruta =  self.ruta_imagen + '%s.png' % level
        self.imagen.set_from_file(ruta)

    def _key_press_cb(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == "KP_Enter":
            
            self._actualizar_palabra()
        return False

    def _actualizar_palabra(self):

        #Convierte la letra a minuscula
        letra_actual = self.palabra_entry.get_text().lower()
        letra_actual = unicode(letra_actual, "utf-8")
        #Divive en dos palabras
        if ' ' in self.palabra:
            longitud_palabra = len(self.palabra) - 1
        else:
            longitud_palabra = len(self.palabra)

        _logger.debug(letra_actual)
        #Evalua si se escribio mas de 1 letra o esta vacio
        if (len(letra_actual) is not 1 or letra_actual == " "): 
            self.palabra_entry.set_text('')
            self.instrucciones_label.set_text(_("Introduzca solo una letra!"))
        
        #Evalua si letra esta dentro de palabra
        elif (letra_actual in self.palabra and letra_actual not in self.l_aciertos):
            self.l_aciertos.append(letra_actual)
            for i in range(len(self.palabra)):
                if letra_actual == self.palabra[i] and self.palabra[i] != ' ':
                    self.aciertos += 1
                    _logger.debug(self.aciertos)
            
            self._actualizar_labels("Letra dentro de palabra secreta!")
            
            #Evalua si se acerto la palabra y temina el juego
            if self.aciertos == longitud_palabra: 
                self.instrucciones_label.set_text(_('FELICIDADES!\nAcertastes la palabra secreta'))
                self.definicion_label.set_text(_('Significado:'))
                self.definicion.set_text(_(self.significado))
                self.palabra_entry.set_sensitive(False)
                self.ok_btn.set_sensitive(False)
                self.aciertos = 0
                #self.nuevojuego_btn.show() # muestra el boton para comenzar el juego

        #Evalua si letra es repetida y esta dentro de palabra
        elif (letra_actual in self.palabra and letra_actual in self.l_aciertos): 
            self._actualizar_labels("Letra repetida y dentro de palabra secreta!")

        #Evalua si letra no esta dentro de palabra
        elif (letra_actual not in self.palabra and letra_actual not in self.l_errores):
            self.l_errores.append(letra_actual)
            self.errores += 1
            self._cambiar_imagen(self.errores)
            self._actualizar_labels("Letra fuera de palabra secreta!")
            
            #Evalua si se completo el ahorcado y temina el juego            
            if (self.errores >= 8):
                self.instrucciones_label.set_text(_('Fin de Juego\nLa palabra secreta era %s' % self.palabra))
                self.definicion_label.set_text(_('Significado:'))
                self.definicion.set_text(_(self.significado))
                self.aciertos = 0
                self.palabra_entry.set_sensitive(False) #Activa la caja de texto
                self.ok_btn.set_sensitive(False) #Inactiva el botón ok una vez que pierde
                

        #Evalua si letra es repetida y no dentro de palabra
        elif (letra_actual not in self.palabra and letra_actual in self.l_errores): 
            self._actualizar_labels("Letra repetida y fuera de palabra secreta!")

        self._pintar_palabra()
        
    def _actualizar_labels(self, instrucciones):
        '''Actualiza labels segun instrucciones'''
        self.palabra_entry.set_text('')
        self.pista_label.set_text(_('Pista:'))
        self.pista.set_text(self.texto_pista)
        self.definicion_label.set_text('')
        self.definicion.set_text('')
        self.instrucciones_label.set_text(_(instrucciones))
        #self.aciertos_label.set_text(_('Puntaje: %s' % self.aciertos))
        letras = ', '.join(letra for letra in self.l_aciertos)
        letras2 = ', '.join(letra for letra in self.l_errores)
        self.letrasusadas_label_2.set_text(_('Letras usadas:'))
        self.letrasusadas_label.set_text('%s %s' % (letras,letras2))
        self.errores_label_2.set_text(_('Errores:'))
        self.errores_label.set_text('%s' % self.errores)

    def _pintar_palabra(self):
        '''Pinta las lineas de la palabra'''
        pista = ''
        for letra in self.palabra:
            if letra in self.l_aciertos:
                pista += '%s ' % letra
            elif letra != ' ': #no pintar espacios
                pista += '_ '
            else:
                pista += ' '
        self.palabra_label.set_text(pista)

    def read_file(self, filepath):
        pass

    def write_file(self, filepath):
        pass

    def close(self, skip_save=False):
        '''override the close to jump the journal'''
        activity.Activity.close(self, True)
