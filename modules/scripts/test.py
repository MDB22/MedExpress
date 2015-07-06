from pubsub import pub
import logger
import lidar
import command

log = logger.Logger()
log.start()

lid = lidar.Lidar()
lid.start()

com = command.Command()
com.start()
