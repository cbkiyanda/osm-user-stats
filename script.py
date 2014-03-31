import urllib
import sys
import time
from xml.dom import minidom

if __name__ == "__main__":
    #Pre-defined locations (bbox)
    locations = {'RN' : [48.2242, -79.0138, 48.2382, -78.9858]}
    
    #construct call to overpass api to get all nodes inside bbox
    call = "http://overpass-api.de/api/interpreter?data=node("
    try:
        location = locations[sys.argv[1]]
    except:
        print("Location doesn't exist")
        print("Call is 'python script.py [location]'")
        print("Using default RN test location")
    else:
        print("Fetching nodes for "+sys.argv[1])
        #create output node file name
        filename = "./nodes_"+sys.argv[1]+".xml"
        #construct bbox string from location data
        for i in range(3):
            call = call + str(location[i]) + ","
        call = call + str(location[3])
        call = call + ");out;"
        #fetching actual data
        urllib.urlretrieve(call, filename=filename)

        #open node file xml
        xmldoc = minidom.parse(filename)
        #find all node objects inside the xml tree
        nodelist = xmldoc.getElementsByTagName('node')
        print("Location "+sys.argv[1]+" contains "+ str(len(nodelist)) + " nodes")
        
        try:
            if (sys.argv[2] == "--production") :
                imax = len(nodelist)
        except:
            imax = 10
        else:
            i = 0
            user_counts = {}
            for s in nodelist : #loop through all nodes
                if (i<imax) :  #for --production call
                    #get id, lat, and lon
                    id  = str(s.attributes['id'].value)
                    lat = str(s.attributes['lat'].value)
                    lon = str(s.attributes['lon'].value)
                    print("Node " + id + ": " + lat + ", " + lon)
                    
                    #initialize urllib to recover node history
                    opener = urllib.FancyURLopener({})
                    #fetch node history through openstreetmap api
                    call = "http://api.openstreetmap.org/api/0.6/node/" + str(id) + "/history"
                    f = opener.open(call)
                    time.sleep(1.0) #sleep for 1 second to not overload the openstreetmap api
                    data = f.read()
                    opener.close()
                    
                    #parse node history xml
                    s_hist_doc  = minidom.parseString(data)
                    #fetch all node objects (there is one node object per node version)
                    s_hist_list = s_hist_doc.getElementsByTagName('node')
                    for v in s_hist_list : #loop through the node versions
                        version = str(v.attributes['version'].value) #fetch version
                        user    = str(v.attributes['user'].value)    #fetch user
                        print("version " + version + " : " + user)
                        if (user_counts.has_key(user)) :  #increase count for that user
                            user_counts[user]+=1
                        else :
                            user_counts[user] = 1
                    i = i + 1
            print(user_counts) #output user counts
