import gettext

_ = gettext.gettext


messages = {
    "SPAPI0001E": _("Unkown parameter specified %(value)s"),
    "SPAPI0002E": _("The specified value %(value)s is not a positive number"),

    "SPRET0001E": _("Interface %(nic)s already exists"),
    "SPRET0002E": _("Interface %(nic)s does not exist"),
    "SPRET0003E": _("Specify nic, onboot and bootproto to create a Interface"),
    "SPRET0004E": _("Interface nic must be a string"),
    "SPRET0005E": _("Interface onboot must be a positive number"),
    "SPRET0006E": _("Interface bootproto must be a positive number"),
}
