# Edited by Fotis Mathioudakis

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt #added by me
import pox.lib.addresses        #added by me 

log = core.getLogger()

class Tutorial (object):

  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)
    # KEYS: macs VALUES: ports
    self.mac_to_port = {}

  def resend_packet (self, packet_in, out_port):

    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)

  def act_like_switch (self, packet, packet_in):

    # Learn the port for the source MAC
    self.mac_to_port[packet.src] = packet.port  # update / create an entry Mac:Port
    
    if packet.dst in self.mac_to_port:
      #send to the port it has to go to
      self.resend_packet(packet_in, self.mac_to_port[packet.dst])
      
    else:
      #flood

    """
    self.mac_to_port = ... <add or update entry>
    
    if the port associated with the destination MAC of the packet is known:
      # Send packet out the associated port
      self.resend_packet(packet_in, ...)

      # Once you have the above working, try pushing a flow entry
      # instead of resending the packet (comment out the above and
      # uncomment and complete the below.)

      log.debug("Installing flow...")
      # Maybe the log statement should have source/destination/port?

      #msg = of.ofp_flow_mod()
      #
      ## Set fields to match received packet
      #msg.match = of.ofp_match.from_packet(packet)
      #
      #< Set other fields of flow_mod (timeouts? buffer_id?) >
      #
      #< Add an output action, and send -- similar to resend_packet() >

    else:
      # Flood the packet out everything but the input port
      # This part looks familiar, right?
      self.resend_packet(packet_in, of.OFPP_ALL)
      """
  def _handle_PacketIn (self, event):

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.

    # Comment out the following line and uncomment the one after
    # when starting the exercise.
    # self.act_like_hub(packet, packet_in)
    self.act_like_switch(packet, packet_in)



def launch ():

  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
