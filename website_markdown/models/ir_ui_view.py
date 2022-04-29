from odoo import models, fields, api, _
import bs4
import markdown

MD_TAG = "markdown"


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    markdown = fields.Text()

    def _render_template(self, template, values=None, engine='ir.qweb'):
        res = super()._render_template(template, values, engine)

        html = res.decode("utf-8")
        soup = bs4.BeautifulSoup(html, 'html.parser')
        if soup.find(MD_TAG):
            for x in soup.find_all(MD_TAG):
                md = markdown.markdown(x.text)
                soup2 = bs4.BeautifulSoup(md, 'html.parser')
                x.replace_with(soup2)
            return str(soup).encode()
        return res
