# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import models, fields, api, tools, _
from io import BytesIO
import base64
import codecs
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment
from openpyxl.styles import NamedStyle, Border, Side, Font
from datetime import date, datetime
import os
import logging


class ReportHoursConsumption(models.TransientModel):
    _inherit = 'file.download.model'
    _name = "report.hours.consumption"

    contract_id = fields.Many2one(
        'project.contract',
        string=_('Project'),
        required=True,
        ondelete='set null'
    )

    def get_filename(self):
        name =\
            'Consumo de Horas'
        return name + '.xlsx'

    def _set_styles(self, wb):
        general_style = NamedStyle(name="general_style")
        general_style.font = Font(
            name='Arial', bold=False, size=8, color="000000")
        general_style.alignment = Alignment(horizontal='left')
        wb.add_named_style(general_style)

        hours_style = NamedStyle(name="hours_style")
        hours_style.font = Font(
            name='Arial', bold=False, size=8, color="000000")
        hours_style.alignment = Alignment(horizontal='right')
        wb.add_named_style(hours_style)

        bd = Side(style='thin', color="000000")
        start_table_style = NamedStyle(name="start_table_style")
        start_table_style.font = Font(
            name='Arial', bold=False, size=11, color="000000")
        start_table_style.alignment = Alignment(horizontal='left')
        start_table_style.border = Border(
                    left=bd,
                    top=bd,
                    bottom=bd)
        wb.add_named_style(start_table_style)

        mid_table_style = NamedStyle(name="mid_table_style")
        mid_table_style.font = Font(
            name='Arial', bold=False, size=11, color="000000")
        mid_table_style.alignment = Alignment(horizontal='right')
        mid_table_style.border = Border(
                    top=bd,
                    bottom=bd)
        wb.add_named_style(mid_table_style)

        end_table_style = NamedStyle(name="end_table_style")
        end_table_style.font = Font(
            name='Arial', bold=False, size=11, color="000000")
        end_table_style.alignment = Alignment(horizontal='right')
        end_table_style.border = Border(
                    right=bd,
                    top=bd,
                    bottom=bd)
        wb.add_named_style(end_table_style)

    """
        Dada una fecha de tipo datetime/date,
        retorna la fecha formateada en string
    """
    def _format_date(self, date):
        return str(date.day).zfill(2) + '/' + str(date.month).zfill(2) + '/' +\
            str(date.year).zfill(2)

    def get_content(self):
        # Creación del path para la busqueda del excel.
        ruta_excel = ''
        for ad in tools.config['addons_path'].split(','):
            if os.path.exists(ad+'/report_hours_consumption/static/template'):
                ruta_excel = ad+'/report_hours_consumption/static/template/' +\
                    'base.xlsx'
        # Se instancia el excel
        path = os.path.expanduser(ruta_excel)
        logging.info('--->>> PATH')
        logging.info(path)
        wb = load_workbook(path)
        # Instanciamos la primera pag del excel
        ws = wb.worksheets[0]
        # Total de letras excel
        list_letras = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
            'W', 'X', 'Y', 'Z'
        ]
        col_fijas = 11
        # Nos quedamos con el numero de cols que rellenaremos con el
        # proceso automatico
        list_columnas = list_letras[:col_fijas]
        linea = 5
        # ESTILOS
        self._set_styles(wb)
        # Logo company
        image_stream = BytesIO(codecs.decode(
            self.env.user.company_id.logo, 'base64'))
        image = Image(image_stream)
        baseheight = 63.87
        hpercent = (baseheight/float(image.height))
        wsize = int((float(image.width)*float(hpercent)))
        image.width = wsize
        image.height = baseheight
        ws.add_image(image, 'I2')
        # Contract name
        ws['B1'] = self.contract_id.name
        # Fecha
        ws['J1'] = self._format_date(datetime.now())
        ws['J1'].style = 'general_style'
        # CUERPO
        dict_tareas = {
            0: 'Bolsa',
            1: 'Tarea',
            2: 'Incidencia',
            3: 'Manual',
        }
        for aal in self.env['account.analytic.line'].search([
                ('contract_id', '=', self.contract_id.id),
                ]
           ).sorted(key='create_date'):
            ws.row_dimensions[linea].height = 20
            # tipo: 0.- Bolsa, 1.- Tarea, 2.- Incidencia, 3.- Manual
            tipo = None
            if aal.contract_hours:
                tipo = 0
            elif not aal.move_id and aal.task_id.project_id.name:
                if 'Issues' in aal.task_id.project_id.name:
                    tipo = 2
                else:
                    tipo = 1
            else:
                tipo = 3
            # Tipo
            col = 0
            ws[list_columnas[col]+str(linea)] = dict_tareas[tipo]
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Fecha creacion
            fecha_creacion = ''
            if tipo == 0:
                fecha_creacion = fecha_creacion =\
                    self._format_date(
                        fields.Datetime.from_string(
                            aal.move_id.invoice_id.date_invoice)
                    )
            elif tipo in (1, 2):
                fecha_creacion = self._format_date(fields.Datetime.from_string(
                    aal.task_id.create_date)
                )
            col += 1
            ws[list_columnas[col]+str(linea)] = fecha_creacion
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Contacto
            col += 1
            contacto = ''
            if tipo == 0:
                contacto = aal.move_id.invoice_id.partner_id.name or ''
            elif tipo in (1, 2):
                contacto = aal.task_id.partner_id.name
            ws[list_columnas[col]+str(linea)] = contacto
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Tarea / Incidencia / Factura
            col += 1
            origin = ''
            if tipo == 0:
                origin = aal.move_id.invoice_id.number or ''
            elif tipo in (1, 2):
                origin = aal.task_id.name
            ws[list_columnas[col]+str(linea)] = origin
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Estado
            col += 1
            state = ''
            if tipo == 0:
                state = aal.move_id.invoice_id.state or ''
            elif tipo in (1, 2):
                state = aal.task_id.stage_id.name
            ws[list_columnas[col]+str(linea)] = state
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Fecha Registro
            col += 1
            ws[list_columnas[col]+str(linea)] =\
                self._format_date(fields.Datetime.from_string(aal.create_date))
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Recurso
            col += 1
            recurso = ''
            if tipo == 0:
                recurso =\
                    aal.move_id.invoice_id.user_id.employee_ids[0].name or ''
            elif tipo in (1, 2):
                recurso = aal.employee_id.name or ''
            ws[list_columnas[col]+str(linea)] = recurso
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Descripcion
            col += 1
            ws[list_columnas[col]+str(linea)] = aal.name
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            # Horas Consumidas
            col += 1
            ws[list_columnas[col]+str(linea)] =\
                round(aal.unit_amount, 2) if tipo > 0 else 0.0
            ws[list_columnas[col]+str(linea)].style = 'hours_style'
            # Horas Compradas
            col += 1
            ws[list_columnas[col]+str(linea)] =\
                round(aal.unit_amount, 2) if tipo == 0 else 0.0
            ws[list_columnas[col]+str(linea)].style = 'hours_style'
            # Alcance
            col += 1
            scope = ''
            if tipo in (1, 2):
                if aal.task_id.beyond_scope:
                    scope = 'Si'
                else:
                    scope = 'No'
            ws[list_columnas[col]+str(linea)] = scope
            ws[list_columnas[col]+str(linea)].style = 'general_style'
            linea += 1
        ws.row_dimensions[linea].height = 30
        ws.row_dimensions[linea+2].height = 30
        ws['H'+str(linea)] = 'Total'
        ws['H'+str(linea)].style = 'start_table_style'
        ws['I'+str(linea)] = '=SUM(I%s:I%s)' % (5, str(linea-1))
        ws['I'+str(linea)].style = 'mid_table_style'
        ws['J'+str(linea)] = '=SUM(J%s:J%s)' % (5, str(linea-1))
        ws['J'+str(linea)].style = 'end_table_style'
        linea += 2
        ws['H'+str(linea)] = 'Diferencia'
        ws['H'+str(linea)].style = 'start_table_style'
        ws['I'+str(linea)] = '=SUM(J%s-I%s)' % (str(linea-2), str(linea-2))
        ws['I'+str(linea)].style = 'end_table_style'

        # Se devuelve el excel generado
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output.read()
