# Topology File Generator

#### Generating the Topology File Generator script
The source code for this topology file generator follows the following pattern:

```
version 16.3
 
setwindow pcb
trapsize 32
topology template
setwindow form.fpsxtopocpy
FORM fpsxtopocpy selectroutedint YES

# Repeat the code in between the here for every net
# ----------------------------------------
FORM fpsxtopocpy selectxnets <NET_NAME1>
FORM fpsxtopocpy selectsaveas
fillin "<directory>/<NET_NAME1>.top"
# ----------------------------------------

# ...

FORM fpsxtopocpy done

setwindow pcb # end of script
```

Where ```<NET_NAME1>``` is the name for whatever net you want to extract a topology file for, and ```<directory>``` is wherever the user would like to store them in.
To generate a script with all of the nets you would like to extract, navigate to the ```data/``` folder and open the excel file called ```ProbeCard_netlist.xlsx```. If this file does not exist, then create one with the same name. This excel file follows the following pattern:

| Net Name  | Extra_Column |
| --------- |:------------:|
| NET_NAME1 | foo          |
| NET_NAME2 | bar          |
| ...       | baz          |
| NET_NAME3 | baz          |

The ```Net Name``` column is used by the script generator to know what net names to include in the script. The position of this column is not important, but the column header must match ```Net Name``` exactly.


If there are too many net names to enter into the excel file manually, you can generate a list of all nets on the PCB inside of Allegro. In the Allegro PCB Editor, navigate in the toolbar to ```Tools``` > ```Quick Report``` > ```Net List Report```

This will generate an HTML file that contains all of the nets on the PCB. Select the contents of the entire file using Ctrl+a and pasting it into the ```ProbeCard_netlist.xlsx``` excel file. Delete the first few lines that have the unnecessary metadata about the quick report.

Once the netlist has been created in the ```data/ProbeCard_netlist.xlsx``` excel file, run the ```generate_topolino_topgen.py``` python script. This python script will create two Cadence Allegro script called ```top_gen_ProbeCard.scr```, and ```top_gen_ProbeCard_xnet.scr```  that will generate topology files for all nets and xnets (respectively) included in your netlist.

#### Using the Topology Generator Scripts
Once the Allegro scripts have been generated, copy both the ```top_gen.bat```, ```configure_constraint_manager.scr``` and the two generated Allegro scripts into the working directory of the ProbeCard project (wherever the .brd) file is located.

First, run the ```top_gen.bat``` batch file. This will prepare two directories called **top_files** and **top_files_xnet** where all of the generated topology files will be deposited for nets and xnets, respectively. Next, it will launch the ProbeCard board file in the Allegro PCB Editor.

To generate all of the topology files for the nets first, navigate to ```File``` > ```Script```, browse for the ```top_gen_ProbeCard.scr``` script, and click **Replay**. This script will take a while.

To generate all of the topology files for the **Xnets** in you netlist, run the ```configure_constraint_manager.scr``` script. This will configure the constraint manager to make all of the Xnets visible that were designated by the TI engineers in the schematic, and also make all of the nets within those Xnets visible. Next, run the ```top_gen_ProbeCard_xnet.scr``` script. This will generate topology files for all of the Xnets in the design that are now visible in the design because the Constraint Manager settings have been configured.
