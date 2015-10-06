# EDITED by Fotis Mathioudakis

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Tutorial (object):

  def __init__ (self, connection):

    self.connection = connection
    connection.addListeners(self)
    # KEYS: Mac    VALUE: port
    self.mac_to_port = {}


  def resend_packet (self, packet_in, out_port):

    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)


  def act_like_hub (self, packet, packet_in):
    srcMac=packet.src
    dstMac=packet.dst
    print("source: ")
    print(srcMac)
    print("destination: ")
    print(dstMac)
    self.resend_packet(packet_in, of.OFPP_ALL)
    

  def _handle_PacketIn (self, event):

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.

    # Comment out the following line and uncomment the one after
    # when starting the exercise.
    self.act_like_hub(packet, packet_in)
    #self.act_like_switch(packet, packet_in)



def launch ():

  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
