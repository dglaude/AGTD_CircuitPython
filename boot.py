import usb_hid

# https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.sdk5.v13.0.0%2Fgroup__app__usbd__hid__mouse__desc.html
simple_mouse = usb_hid.Device(
    report_descriptor=bytes(
        # Simple mouse
        (0x05, 0x01)    # Usage Page (Generic Desktop)
        + (0x09, 0x02)  # Usage (Mouse)
        + (0xA1, 0x01)  # Collection (Application)
        + (0x09, 0x01)  # Usage (Pointer)
        + (0xA1, 0x00)  # Collection (Physical)
        + (0x85, 0x0B)  # Report ID  [11 is SET at RUNTIME]
        # Buttons
        + (0x05, 0x09)  # Usage Page (Button)
        + (0x19, 0x01)  # Usage Minimum (0x01)
        + (0x29, 0x05)  # Usage Maximum (0x05)
        + (0x15, 0x00)  # Logical Minimum (0)
        + (0x25, 0x01)  # Logical Maximum (1)
        + (0x95, 0x05)  # Report Count (5)
        + (0x75, 0x01)  # Report Size (1)      ??? Sometime the 0x75 line is before the 0x95 line ???
        + (0x81, 0x02)  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        + (0x75, 0x03)  # Report Size (3)
        + (0x95, 0x01)  # Report Count (1)
        + (0x81, 0x01)  # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position) ??? was 0x03 ???
        # Movement
        + (0x05, 0x01)        # Usage Page (Generic Desktop Ctrls)
        + (0x09, 0x30)        # Usage (X)
        + (0x09, 0x31)        # Usage (Y)
        # Wheel
        + (0x09, 0x38)   # Usage (Wheel)
        + (0x15, 0x81)   # Logical Minimum (-127)
        + (0x25, 0x7F)   # Logical Maximum (127)
        #+ (0x35, 0x81)   # Physical Minimum (same as logical)
        #+ (0x45, 0x7f)   # Physical Maximum (same as logical)
        + (0x75, 0x08)   # Report Size (8)
        + (0x95, 0x03)   # Report Count (1)  ??? was 0x03 ???
        + (0x81, 0x06)   # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        + (0xC0,)  #   End Collection
        + (0xC0,) # End Collection
    ),
    usage_page=1,
    usage=2,
    in_report_lengths=(4,), # Number of bytes in the send report = 1 byte for buttons, 1 byte for x, 1 byte for y, 1 byte for wheel
    out_report_lengths=(0,),
    report_ids=(11,),
)

usb_hid.enable((usb_hid.Device.KEYBOARD,), boot_device=1)
usb_hid.enable((simple_mouse,), boot_device=0)
