# Long-range (LoRa) radio sensors

[LoRa](https://en.wikipedia.org/wiki/LoRa) is a communication method based on
[chirp spread spectrum](https://en.wikipedia.org/wiki/Chirp_spread_spectrum).
It's only about 10 years old.

LoRaWAN Is the networking protocol associated with LoRa, the shared
language in which LoRa nodes communicate.
A LoRaWAN gateway listens in on LoRa activity and translates it for
use in a computer network.

LoRa has some cool properties. It is low power, so with careful power
management a sensor and transmitter can last for a decade on a single
small battery. Because of the wavelength it operates at and the way it
modulates its signal, it can be sent over long distances.
Under the right conditions, it can travel for miles. It is low bandwidth
compared to familiar radio protocols like Wi-Fi or Bluetooth.
For garden instrumentation this is just fine. Temperature and moisture
are not expected to change very fast.

[Semtech](https://en.wikipedia.org/wiki/Semtech) is the company that owns
patents on LoRa and is the founding member of the LoRa Alliance.
It's a publicly traded, 65 year old Southern California company.
With this comes the risk that it could be made restricted or changed
at any time. Not as much of a risk for small home projects, but something
to consider if you’re thinking about building a business model around it.


The Gateway description.
Connecting to a computer.

Connected via Netgear NightHawk router
192.168.1.1
as
192.168.1.90
https://192.168.1.90/dashboard/lora-network-server

Connecting a temperature sensor.

https://wiki.dragino.com/xwiki/bin/view/Main/User%20Manual%20for%20LoRaWAN%20End%20Nodes/T68DL_LoRaWAN_Temperature_Sensor_Manual

Connecting a soil moisture sensor.
Deploying soil, moisture sensor.


## Gateways

https://store.rakwireless.com/products/rak7268-8-channel-indoor-lorawan-gateway?variant=44719903178950
https://docs.rakwireless.com/product-categories/wisgate/rak7268v2/quickstart/
https://docs.rakwireless.com/product-categories/wisgate/rak7268v2/lorawan-network-server-guide/
https://docs.rakwireless.com/product-categories/wisgate/rak7268v2/datasheet/
https://192.168.230.1/dashboard/overview


how-to: https://community.home-assistant.io/t/integrating-lorawan-sensors-into-home-assistant/628322

Dragino gateway configuration
https://www.dragino.com/downloads/downloads/LoRa_Gateway/LPS8/LPS8_LoRaWAN_Gateway_User_Manual_v1.3.2.pdf

https://www.chirpstack.io/docs/chirpstack-mqtt-forwarder/install/dragino.html#configure-packet-forwarder

## Packet forwarder

[MQTT](https://en.wikipedia.org/wiki/MQTT)
[Python MQTT client](https://pypi.org/project/paho-mqtt/)


-------

https://www.dragino.com/products/lora-lorawan-end-node.html
https://www.dragino.com/products/lora/item/232-la66-usb-lorawan-adapter.html
https://www.hackster.io/sufiankaki/lora-e5-the-things-network-mqtt-655086

https://www.seeedstudio.com/blog/2021/04/27/a-gentle-introduction-to-lorawan-gateways-nodes/

temperature sensor
https://wiki.dragino.com/xwiki/bin/view/Main/User%20Manual%20for%20LoRaWAN%20End%20Nodes/T68DL_LoRaWAN_Temperature_Sensor_Manual/#H3.2SetTransmitIntervalTime
