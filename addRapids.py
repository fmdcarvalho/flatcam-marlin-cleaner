import re

def addFeed(l):
    if re.search("G(0)1 Z-", l):
        return l + " F" + str(plungingFeed)
    if "G00" in l:
        return l + " F" + str(rapidsFeed)
    if "G01" in l:
        return l + " F" + str(cuttingFeed)
    return l

def trimLineBreaks(l):
    if re.search("(\\r|)\\n$", l):
        l = re.sub("(\\r|)\\n$", "", l)
    return l

def checkFeed(l):
    return re.search("F\d*.\d*", l)


## TODO: pass paths as params
f = open("../top.gcode", "r")
out  = open("../top.out.gcode", "w")

## TODO: pass feeds as params
rapidsFeed = 300
cuttingFeed = 40
plungingFeed = 10
zeroed = False
# M211 S0 disable end stops
## TODO: disable end stops by param
out.write("M211 S0\n")

for i,l in enumerate(f):
    # trim \r or \rn
    l = trimLineBreaks(l);
    # remove empty lines
    if len(l) == 0 :
        continue;
    # check for G92 units by minute feed
    # for my future self: flatcam sets
    #   G21 metric/ G20 imperial
    #   G90 absolute coordinates
    #   G94 mm per minute/ and I assume G95 is possible too
    # lets use this as a reference to when to zero all axis
    ## TODO: check in args what axis to zero. none, z, xy, xyz,
    if not zeroed and ("G94" in l or "G95" in l):
        l = l + "\nG92 X0Y0Z0"
        zeroed = True
    # check if line sets the feed
    if checkFeed(l):
        # flatcam sets the feed after G94 on the next line with F00.00
        # since marlin cant read that lets change this line to G0 F00.00
        if "G00" not in l:
            l = "G00 " + l
        else:
            print("Error! Found a rapid with the feed set :" + str(i))
            exit(1)
    else:
        l = addFeed(l)
    out.write(l+"\n")
