import json
import os

iconsDir = os.path.join("UI","icons")

def getIcon(name,iconsDir = iconsDir,  OS='linux'):
    """function used to get path of icons based on each OS.
    and the give the path of the icon to the caller function.
    
    Arguments:
        name {[string]} -- [name of the icon category, it can take values:
                        `mainIcon`]
    
    Keyword Arguments:
        iconsDir {string} -- [directory containing the icons] (default: {iconsDir})
        os {string} -- [type of OS to load specific icons fromat] (default: {linux})
    
    Returns:
        [type] -- [description]
    """

    if(OS == 'linux'):
        iconName = name  + ".png"
        iconPath = os.path.join(iconsDir, iconName )
    elif(OS == 'win32'):
        iconName = name + ".ico"
        iconPath = os.path.join(iconsDir, iconName )
    return iconPath
