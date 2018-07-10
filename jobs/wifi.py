#coding: utf8
import pywifi
from pywifi import const
import time

class wifi:
    def __init__(self,ssid):
        self.ssid = ssid

    def pojie(self):
        wf = pywifi.PyWiFi()

        iface = wf.interfaces()[0]

        iface.disconnect()
        time.sleep(1)
        assert iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]


        profile = pywifi.Profile()
        profile.ssid = self.ssid

        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)

        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = "today36524"

        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        iface.connect(tmp_profile)

        print(iface.status())

if __name__ == "__main__":
    wifi("Today-Office").pojie()