from dearpygui.core import *
from dearpygui.simple import *
from logicgates import from_boolean_expression


def delete_tab(sender, data):
    delete_item(get_value('tabs'))

def make_table(sender,data):
    delete_item('Submit')
    try:
        set_value('##truth_table_text','')
        set_value('##status','trying (variables past p take forever to fill)')
        truth_table, truth_data = from_boolean_expression(get_value('##expression')).truth_table()

        tab_id = truth_data[0][len(truth_data[0])-1]
        add_tab(tab_id,parent='tabs')
        tab_id_text = '( '+tab_id + ' )text'
        tab_id_table = '( '+tab_id + ' )table'
        tab_bar = tab_id+'tab_bar'
        add_tab_bar(tab_bar, parent=tab_id)
        add_tab(tab_id_text,parent=tab_bar)
        truth_table_text = '##( '+tab_id_text+' )text'
        add_text(truth_table_text)
        set_value(truth_table_text,truth_table)
        end()
        add_tab(tab_id_table,parent=tab_bar,before=tab_id_text)

        table_id = f'##truth_table_{tab_id}'
        add_table(table_id, truth_data[0], height=3000)

        set_value('##status','filling table')
        for row in truth_data[1:]:
            add_row(table_id, row)

        end()
        set_value('##status','')
    except:
        set_value('##status','failed')

    add_button('Submit',before='##expression',parent='header_group',callback=make_table)

with window('window1'):
    add_group('header_group',horizontal=True)
    add_button('Submit',parent='header_group',callback=make_table)
    add_input_text('##expression',parent='header_group')
    end()
    add_button('delete tab',callback=delete_tab)
    add_label_text('##status')
    add_tab_bar('tabs')
    end()




THEMES='''Classic, Light, Grey, Dark Grey, Dark, Dark 2, Cherry, Purple, Gold, Red'''.split(', ')
set_theme(THEMES[1]) # 5
add_additional_font("mono.ttf", 16)
set_main_window_title('Boolean Algebra Truth Tables')
set_primary_window('window1',True)
start_dearpygui()
