from odoo import models, fields, api, _
import logging
import markdown
import odoorpc

conn = odoorpc.ODOO()
_logger = logging.getLogger(__name__+' Kriss')


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    markdown = fields.Text()

    def _render_template(self, template, values=None, engine='ir.qweb'):
        _logger.error(f"{self=}")
        _logger.error(f"{template=}")
        _logger.error(f"{engine=}")
        _logger.error(f"{values=}")
        res = super()._render_template(template, values, engine)

        md = res.decode("utf-8")
        # if "##" in md:
        #     return markdown.markdown(md).encode(encoding='UTF-8')
        #     _logger.error(f"{new_md=}")

        return res

class IrQweb(models.AbstractModel):
    _inherit = 'ir.qweb'

    @api.model 
    def _render(self, id_or_xml_id, values=None, **options):
        # _logger.error(f"{self=}")
        # _logger.error(f"{id_or_xml_id=}")
        # _logger.error(f"{options=}")
        # _logger.error(f"{values=}")
        res = super()._render(id_or_xml_id, values, **options)
        #_logger.error(f"{res=}")
        return res


    #     In [34]: for x in html2: 
    # ...:     if '<' not in x: 
    # ...:         print(markdown.markdown(x.strip())) 
    # ...:     else : 
    # ...:         print (x)
    #  
    #     In [49]: for x in soup2: 
    # ...:     print (markdown.markdown(x.text.strip()))
