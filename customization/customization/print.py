import frappe
from frappe import _

@frappe.whitelist()
def create_items(items, print_settings):

    used_position_groups = []
    position_group_list = []

    sr = 0
    for itm in items:
        if itm.position_group != None:
            if itm.position_group not in used_position_groups and itm.position_group != None and itm.position_group != "":
            
                sr += 1 
                doc_pos_group = frappe.get_doc('Quotation Position Group', itm.position_group) 
                used_position_groups.append(itm.position_group)
                
                pos_group_desc = "" 
                
                if doc_pos_group.description != None:
                    pos_group_desc = '<br>' + doc_pos_group.description
                    
                description = '<b>' + itm.position_group + '</b>' + pos_group_desc 

                amount = 0
                for i in items:
                    if i.position_group == itm.position_group:
                        amount += (i.rate * i.qty)
                
                itm.pos_amount = amount
                row = { 
                    "sr": str(sr),
                    "description": description,
                    "uom": '&nbsp;',
                    "qty": '&nbsp;',
                    "price": '&nbsp;',
                    "amount": itm.get_formatted("pos_amount"),
                    "top_sr": True
                } or "" 
                
                position_group_list.append(row)
                
                
                # <!-- Unterspositionen hinzufügen -->
                sr_sub = 0
                for i in range(0, len(items)):
                    doc_item = items[i]
                    if doc_item.position_group == itm.position_group:
                        sr_sub += 1 
                        
                        #<!-- QTY -->
                        qty =  doc_item.get_formatted("qty")
                        if print_settings.print_uom_after_quantity:
                            qty =  qty + ' ' +  _(itm.uom) 
                            
                        
                        row = { 
                            "sr": str(sr) + '.' + str(sr_sub),
                            "description": '<b>' + _(doc_item.item_name) + '</b><br>' + _(doc_item.description),
                            "uom": _(doc_item.uom) if not print_settings.print_uom_after_quantity else '&nbsp;',
                            "qty": qty,
                            "price": doc_item.get_formatted("rate"),
                            "amount": '&nbsp;',
                            "top_sr": False
                        } or "" 
                        
                        if not doc_item.hide_in_pos_group:
                            position_group_list.append(row)
                        #else:
                            
                        
                        
            
        else:
            sr += 1
         
            #<!-- QTY -->
            qty =  itm.get_formatted("qty")
            if print_settings.print_uom_after_quantity:
                qty =  qty + ' ' +  _(itm.uom)

            row = { 
                "sr": str(sr),
                "description": '<b>' + _(itm.item_name) + '</b><br>' + _(itm.description),
                "uom": _(itm.uom) if not print_settings.print_uom_after_quantity else '&nbsp;',
                "qty": qty,
                "price": itm.get_formatted("rate"),
                "amount": itm.get_formatted("amount"),
                "top_sr": True
            } or "" 

            position_group_list.append(row) or ""
        
    
    return position_group_list
