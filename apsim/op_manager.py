#!/usr/bin/env Python

import xml.etree.ElementTree
from xml.etree.ElementTree import ElementTree, Element, SubElement

###
def Init_New_Op( date ):
    op_elem = Element( 'operation' )
    op_elem.set( 'condition', 'start_of_day' )
    date_elem = SubElement( op_elem, 'date' )
    date_elem.text = date

    return op_elem

###
def Add_Till_Op( ops_xml, date, type, f_incorp = None, tillage_depth = None ):
    op_elem = Init_New_Op( date )
    if type == 'user_defined':
        action = ( 'SurfaceOrganicMatter tillage type = user_defined, ' +
            'f_incorp = {} (0-1), tillage_depth = {} (mm)' ).format(
            str( f_incorp ), str( tillage_depth ) )
    else:
        action = 'SurfaceOrganicMatter tillage type = ' + type
    act_elem = SubElement( op_elem, 'action' )
    act_elem.text = action
    ops_xml.append( op_elem )

    return

###
def Add_Fertilizer_Op( ops_xml, date, value, depth, type ):
    op_elem = Init_New_Op( date )
    action = ( 'Fertiliser apply ' +
        'amount = {} (kg/ha), depth = {} (mm), type = {} ()').format(
        str( value ), str( depth ), type )
    act_elem = SubElement( op_elem, 'action' )
    act_elem.text = action
    ops_xml.append( op_elem )

    return

###
def Add_Manure_Op( ops_xml, date, type, name, mass, cnr, cpr ):
    op_elem = Init_New_Op( date )
    action = (
        'SurfaceOrganicMatter add_surfaceom ' +
        'type = {}, name = {}, mass = {} (kg/ha), cnr = {}, cpr = {}' ).format(
        type, name, str( mass ), str( cnr ), str( cpr ) )
    act_elem = SubElement( op_elem, 'action' )
    act_elem.text = action
    ops_xml.append( op_elem )

    return

###
def Add_Planting_Op( ops_xml, date, crop, density, depth, cultivar, spacing ):
    op_elem = Init_New_Op( date )
    action = ( '{} sow plants = {} (plants/m2), sowing_depth = {} (mm), ' +
        'cultivar = {}, row_spacing = {} (mm), crop_class = plant' ).format(
        crop, str( density ), str( depth ), cultivar, str( spacing ) )
    act_elem = SubElement( op_elem, 'action' )
    act_elem.text = action
    ops_xml.append( op_elem )

    return

###
def Add_Harvest_Op( ops_xml, date, crop ):
    op_elem = Init_New_Op( date )
    action = ( '{} end_crop' ).format( crop )
    act_elem = SubElement( op_elem, 'action' )
    act_elem.text = action
    ops_xml.append( op_elem )

    return

###
def Add_Management_Oprns( calender ):
    man_xml = Element( 'folder' )
    man_xml.set( 'name', 'Manager folder' )
    oprns = SubElement( man_xml, 'operations' )
    oprns.set( 'name', 'Operations Schedule' )

    return man_xml

#Add empty manager with bu/ac for corn/soy and the gradient for SWIM to work.
def Add_Empty_Manager( bbc_potential = [ 200, 100 ] ):
    """
    Creates an empty APSIM 'Manager' folder to hold bu/ac calculationg and
    SWIM bbc_potential = profile depth - tile/water table depth
    without the gradient set.

    Returns:
        [xml] -- [XML for an empty manager]
    """
    empty_man = Element( 'manager' )
    empty_man.set( 'name', 'Empty manager' )
    init_script = SubElement( empty_man, 'script' )
    init_script_text = SubElement( init_script, 'text' )
    init_event = SubElement( init_script, 'event' ).text = 'init'

    gradient_script = SubElement( empty_man, 'script' )
    gradient_script_txt = SubElement( gradient_script, 'text' )

    #!!!!IMPORTANT!!!!!
    #subsurface_drain and subsurface_drain_no3 won't work unless bbc_potential is se
    #!!!!!!!!!!!!!!!!!!

    gradient_script_txt.text = """corn_buac   = maize.yield * 0.0159/0.85  ! corn yield in bushels/acre@15% moisture
!soy_buac   = soybean.yield * 0.0149/0.87  !  soybean yield in bushels/acre

!bbc_gradient = -1
bbc_potential = {} - {}
""".format(bbc_potential[0],bbc_potential[1])
    gradient_event = SubElement( gradient_script, 'event' ).text = 'start_of_day'

    end_script = SubElement( empty_man, 'script' )
    end_script_text = SubElement( end_script, 'text' )
    end_event = SubElement( end_script, 'event' ).text = 'end_of_day'

    return empty_man
#
# Add_Till_Op( '13/4/2007', 'user_defined', 0.0, 50.0 )
# Add_Fertilizer_Op( '14/4/2007', 25.0, 10.0, 'urea_no3' )
# Add_Planting_Op( '15/4/2007', 'maize', 8, 50.0, 'B_115', 762.0 )
# Add_Harvest_Op( '20/10/2010', 'maize' )
# Add_Manure_Op( '20/10/2010', 'manure', 'manure_app', 10000.0, 20.0, 50.0 )
