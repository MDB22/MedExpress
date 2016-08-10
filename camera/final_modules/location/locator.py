import math



def get_distance_from_pixel(image_shape, pixel_addr, altitude):
    # this method takes in an image altitude, and address and
    # attempts to determine the straight line distance and ground distance and
    # heading adjustments for use in the GPS coordinates function
    # from a drone to an object

    #unpack the inputs
    img_px_h = image_shape[0]
    img_px_w = image_shape[1]
    px_addr_v = pixel_addr[1]
    px_addr_h = pixel_addr[0]

    #determine the verticle angle
    px_fraction_v = float(px_addr_v)/float(img_px_h)
    angle_v = (10 + 40 * (px_fraction_v))*(math.pi/180) # DEAL WITH THE MAGIC NUMBERS
    dist_v = altitude/math.sin(angle_v)

    #determine the horizontal angle
    center_to_edge = dist_v*math.tan(25.6*(math.pi/180))
    #readdress the horizontal pixel from he center
    c_px_addr_w = int(px_addr_h - (img_px_w/2))
    abs_hor_dist = math.fabs(c_px_addr_w)
    hor_dist_fraction = float(abs_hor_dist)/(float(img_px_w)/2)
    hor_dist_fraction_signed = float(c_px_addr_w)/(float(img_px_w)/2)
    #find the distance from center out
    #from the ratio of the total distance 
    dist_from_center = center_to_edge*hor_dist_fraction
    # the angle from the heading
    target_bearing = hor_dist_fraction_signed * 26.5 #magic number from raspi camera fov

    # straight line distance
    sl_distance = math.sqrt(dist_from_center**2 + dist_v**2)
    # ground distance
    gn_distance = math.sqrt(sl_distance**2 - altitude**2)
    
    return (target_bearing, gn_distance, sl_distance)
