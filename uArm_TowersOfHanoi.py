# get a uArm robot arm with suction end to solve the Towers of Hanoi for you
import math,logging,math
import pyuarm

logging.basicConfig(format='# %(levelname)s:%(name)s: %(message)s')
logger=logging.getLogger(__name__)   # default logger level is WARNING

class TowerOfHanoi:
  def __init__(self,use_uarm=False,disc_thickness=0.1,disc_radius=12):
    """Class definition for Tower of Hanoi uArm solver program
    """
    self.use_uarm=use_uarm
    self.disc_thickness=0.1	# cm
    self.disc_radius=12		# cm
    logger.debug("Disc thickness (cm): "+str(disc_thickness))
    logger.debug("Disc radius (cm): "+str(disc_radius))
    if self.use_uarm:
      # init the uArm
      self.myuarm = pyuarm.uarm.UArm()

  def __del__(self):
    if self.use_uarm:
      # disconnect the uArm
      self.myuarm.disconnect()

  def solve(self,height=5):
    self.moveTower(height,"A","B","C")

  def moveTower(self,height,fromPos, toPos, viaPos):
    if height >= 1:
        self.moveTower(height-1,fromPos,viaPos,toPos)
        self.moveDisc(height,fromPos,toPos)
        self.moveTower(height-1,viaPos,toPos,fromPos)

  def decodePosToXYZ(self,height,pos):
    """Decode the location and height of a disc to an XYZ position for the arm
    """
    rad=220.0 
    if pos=='A':
      angle=-60*math.pi/180.0
    if pos=='B':
      angle=0.0
    if pos=='C':
      angle=60*math.pi/180.0
    x=math.sin(angle)*rad
    y=math.cos(angle)*rad
    z=10.0
    return (x,y,z)


  def moveDisc(self,height,fromPos,toPos):
    logger.info("Moving disc from "+str(fromPos)+" to "+str(toPos)+" at height "+str(height))
    if self.use_uarm:
	# move the disc
        # pump on
	logger.debug("pump on")
        # move to target
        (x,y,z) = self.decodePosToXYZ(height,fromPos)
	logger.debug("Setting XYZ to: %.1f,%.1f,%.1f" % (x,y,z) )
        self.myuarm.set_position(x,y,z,speed=50,wait=True)
        # pick it up
        # move to destination
        (x,y,z) = self.decodePosToXYZ(height,toPos)
	logger.debug("Setting XYZ to: %.1f,%.1f,%.1f" % (x,y,z) )
        self.myuarm.set_position(x,y,z,speed=50,wait=True)
        # pump off
	logger.debug("pump off")

# run in standalone mode
if __name__ == "__main__":
  logger.setLevel(logging.DEBUG)
  tower=TowerOfHanoi(use_uarm=True)
  tower.solve()

