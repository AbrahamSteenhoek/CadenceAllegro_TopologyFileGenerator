from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import pandas as pd
import sys
import os
import shutil
from os import path
from openpyxl import Workbook

# add tkinter
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
print( os.getcwd() )
netlist_fname = askopenfilename( initialdir = f'{os.getcwd()}/data', title = 'Select Netlist File') # show an "Open" dialog box and return the path to the selected file
print('filename: ' + netlist_fname)
if not netlist_fname: # quit if no file was selected
    print( 'No file selected. Quitting...')
    quit()

output_folder = 'generated_scripts'
if os.path.isdir( output_folder ):
    shutil.rmtree( output_folder )
os.mkdir( output_folder )

top_gen_net_fname = f'{output_folder}/top_gen_PROBE_CARD.scr'
top_gen_xnet_fname = f'{output_folder}/top_gen_PROBE_CARD_xnet.scr'
top_gen_batch_file = f'{output_folder}/top_gen_batch.bat'

with open( top_gen_net_fname, 'w+' ) as top_gen, open( top_gen_xnet_fname, 'w+' ) as top_gen_xnet, open( top_gen_batch_file, 'w+' ) as top_gen_batch:
    preamble_str = '''\
# Allegro script
#    file: top_gen.scr
version 16.3

setwindow pcb
trapsize 32
topology template
setwindow form.fpsxtopocpy
FORM fpsxtopocpy selectroutedint YES
'''
    top_gen.write( preamble_str )
    top_gen_xnet.write( preamble_str )

    print('reading excel file...')
    if not path.exists( netlist_fname ):
        print('Netlist file: \"PROBE_CARD_netlist.xlsx\" not found')
        sys.exit()
        
    netlist_df = pd.read_excel( netlist_fname )

    netlist = netlist_df['Net Name']
    for net_name in netlist:
        save_topology_cmd_str = f'''
# ----------------------------------------
FORM fpsxtopocpy selectxnets {net_name}
FORM fpsxtopocpy selectsaveas
fillin "top_files_net/{net_name}.top"
# ----------------------------------------
'''
        top_gen.write( save_topology_cmd_str )

        save_topology_cmd_str_xnet = f'''
# ----------------------------------------
FORM fpsxtopocpy selectxnets {net_name}
FORM fpsxtopocpy selectsaveas
fillin "top_files_xnet/xnet_{net_name}.top"
# ----------------------------------------
'''
        top_gen_xnet.write( save_topology_cmd_str_xnet )
        # print(save_topology_cmd_str)

    postlude_str = '''
FORM fpsxtopocpy done

setwindow pcb
### quit
'''

    top_gen.write( postlude_str )
    top_gen_xnet.write( postlude_str )

    top_gen_batch.write(
'''
if exist top_files_net rmdir top_files_net/q /s
if exist top_files_xnet rmdir top_files_xnet /q /s
MKDIR top_files_net
MKDIR top_files_xnet
start /MIN allegro -product Allegro_performance PROBE_CARD_PRODUCT_ID.brd
'''
    )

    print('scripts generated!')