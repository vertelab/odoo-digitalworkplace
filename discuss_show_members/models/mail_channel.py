# mail.channel was renamed discuss.channel in 18.0, and the OWL client this
# module patched (the legacy `odoo.define` components) was replaced. The
# module's own manifest says so: it is Odoo-17 code that crashes on a fresh
# install. There is nothing to inherit from in 19.0 and 20.0, so the module
# carries no model — see `installable` in __manifest__.p.py.
