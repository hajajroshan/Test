from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "sale.order"
    # print(commitment_date)
    commitment_date = fields.Date()


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for pick in self:
            warehouse_id = pick.picking_type_id.warehouse_id
            if warehouse_id and warehouse_id.delivery_steps:
                for move in pick.move_ids_without_package:
                    if move.product_uom_qty != move.quantity_done:
                        sale_order = self.env[
                            'sale.order'].search([])
                        for sl_order in sale_order:
                            if sl_order.name == pick.origin:
                                sale_order = sl_order
                                responsible_person = sale_order.user_id.name
                                break
                        display_msg = """ Dear """ + responsible_person + """,
                                       <br/>
                                       Please find the delivery deviation from 
                                       the """ + sale_order.name + """
                                       <br/>
                                       <b>Missing Products:</b>
                                       <br/>
                                   """
                        for prod in move:
                            if prod.quantity_done == 0:
                                prod_id = self.env[
                                    'product.product'].browse(
                                    prod['product_id'])
                                display_msg += """ - """
                                display_msg += str(prod_id.id.name)
                                display_msg += """ <br/> """
                        sale_order.message_post(body=display_msg)
        return res
