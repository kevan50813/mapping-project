This folder contains static readings from the William Bragg building, so further testing can be done while the building itself is closed.

These readings are all .csv files in the format MAC,Quality,RSSI,Distance,SSID

The Distance value of these are calculated using the current algorithms, and may be very wrong. 
The MAC, SSID and Quality are all read directly from the device's wireless card, so are accurate. 
RSSI should be accurate, but a better Quality -> RSSI algorithm may be found at some point.

The files are in the format \<vauge room name>_r\<reading number>.csv

studyroom is one of the small tutorial rooms next to the 24h learning lab (2.13)