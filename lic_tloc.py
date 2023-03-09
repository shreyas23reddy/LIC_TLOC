import requests
import json
import yaml
import re
import time
import csv
import argparse
import os.path


from auth_header import Authentication as auth
from operations import Operation
from license_class_tloc import getData
from license_class_tloc import postData
from license_class_tloc import findTlocExt
from license_class_tloc import Tier_Allocation
from query import queryPayload






if __name__=='__main__':

    while True:

        """ Adding cli via Arg parse """

        parser = argparse.ArgumentParser()

        parser.add_argument("-a","--address", help="vManage IP address")
        parser.add_argument("-p","--port", default=8443, help="vManage port")
        parser.add_argument("-u","--username", help="vManage username")
        parser.add_argument("-pw","--password", help="vManage password")



        subparser = parser.add_subparsers(dest='command',help="'sid' - run script on a specific site id's")

        """'sid' will pull the detials from a specific site-id's in the overlay """


        sid = subparser.add_parser('sid')


        sid.add_argument('-id', nargs = '+', required=True, help= "-id 10 20 30")
        sid.add_argument('-tlocext',choices=["yes","no"],default="no",help = "will identify TLOC EXT interface only when the interface is directly connected. 'yes/no'")
        sid.add_argument('-filename', nargs = '+',required=True, help= "path/filename same filename for multiple itearation")

        args = parser.parse_args()

        vmanage_host = args.address
        vmanage_port = args.port
        username = args.username
        password = args.password



        """ GET the TOKEN from Authnetication call"""
        header= auth.get_header(vmanage_host, vmanage_port,username, password)

        """ data collection Dict """
        report_data ={}



        for site_id in args.id:


            """
            To get the details of a specific Site-ID  '/dataservice/device?site-id='+site_id
            """

            deviceInfo = getData.getDeviceIP(vmanage_host,vmanage_port,header,site_id)

            if deviceInfo == []:
                print(f"""
                please verify if the site-id {site_id} is valid
                """)

            else:

                """
                Iterating the rx'ed data if there is more than 1 edge device in the site
                """

                for iter_deviceInfo in deviceInfo:

                    print(f""" Getting info related to SITE-ID {site_id}""")


                    """
                    Dumping the data into a DIC report_data
                    """

                    if (iter_deviceInfo["site-id"],iter_deviceInfo["system-ip"]) not in report_data:
                        report_data[(iter_deviceInfo["site-id"],iter_deviceInfo["system-ip"])] = {
                        "host-name":iter_deviceInfo["host-name"],
                        "uuid":iter_deviceInfo["uuid"],
                        "reachability":iter_deviceInfo["reachability"],
                        "validity":iter_deviceInfo["validity"],
                        "wanIFName-stats":{},
                        "TlocEXT-IfName":[],
                        "BW-Agg-Site-Mbps":0,
                        "License-Tier":None
                        }



                    """
                    try to Pull WAN interface name if the device is reachable and valid
                    """

                    if iter_deviceInfo["reachability"] == "reachable" and iter_deviceInfo["validity"] == "valid":

                        print(f""" Getting WAN Parent interface info from {iter_deviceInfo["system-ip"]}""")

                        wanIFName = getData.getWANIfName(vmanage_host,vmanage_port,header,iter_deviceInfo["system-ip"])



                        """
                        Iterate the rx'ed WAN interface if the device has more than one WAN interface
                        Interface stats are pulled only from parent interface. So we are eliminating the Sub-interface tag
                        don't worry of the duplicate's if we have 2 wan interface on a single parent interface
                        Dic "wanIFName-stats":{} will handle it
                        """

                        for iter_wanIFName in wanIFName:
                            TransportIfName = re.split(r"\.", iter_wanIFName["interface"])[0]

                            if TransportIfName not in report_data[(iter_deviceInfo["site-id"],iter_deviceInfo["system-ip"])]["wanIFName-stats"]:
                                report_data[(iter_deviceInfo["site-id"],iter_deviceInfo["system-ip"])]["wanIFName-stats"][TransportIfName]=[]

                    else:

                        print(f""" UUID - {iter_deviceInfo["uuid"]}  System-IP - {iter_deviceInfo["system-ip"]}  is either Unreachable or in Invalid/Staging Mode """)




                """
                Determining if the site has 2 edge devices. If so determaine if we have TLOC ext between them.
                Also device needs to reachable and vaild.
                Assigning System_IP to systemIPlst
                """

                numberOfEdgeDevices = 0
                systemIPlst = []

                for key in (list(report_data.keys())):
                    if key[0] == site_id and report_data[key]["reachability"] == "reachable" and report_data[key]["validity"] == "valid" :
                        numberOfEdgeDevices += 1
                        systemIPlst.append(key[1])


                if numberOfEdgeDevices == 2 and args.tlocext == "yes":

                    print(f""" determine if the TLOC EXT is present""")
                    report_data = findTlocExt.findIfTlocext(vmanage_host,vmanage_port,header,report_data,site_id,systemIPlst)

                """
                Assigning a temp list to store interface stats to calculate peak cumulative score
                """

                BW_Site =[]



                for iterSystemIP in systemIPlst:


                    if (report_data[(str(site_id),iterSystemIP)]['reachability'] == 'reachable') and (report_data[(str(site_id),iterSystemIP)]['validity'] == 'valid'):
                        for iterTransportIfName in report_data[(str(site_id),iterSystemIP)]["wanIFName-stats"]:



                            """
                            data = queryPayload.statsIFAgg(iterSystemIP , iterTransportIfName, duration = "2", interval = 30)
                            create a query payload to pull the interface stats
                            duration is in hours, interval is in minutes
                            """

                            data = queryPayload.statsIFAgg(iterSystemIP , iterTransportIfName, duration = "2", interval = 30)

                            time.sleep(1)


                            print(f"pulling the interface stats of Site-ID {site_id} -- System-IP {iterSystemIP} -- TLOC parent Interface {iterTransportIfName}")

                            interfaceStats = postData.getInterfaceStats(vmanage_host,vmanage_port,header,data)

                            report_data[(str(site_id),iterSystemIP)]["wanIFName-stats"][iterTransportIfName]=interfaceStats



                            if (iterTransportIfName not in report_data[(str(site_id),iterSystemIP)]["TlocEXT-IfName"]):

                                if  BW_Site == []:
                                    for iter_interfaceStats in interfaceStats:
                                        BW_Site.append(iter_interfaceStats['tx_kbps']+iter_interfaceStats['rx_kbps'])

                                elif len(BW_Site) >= len(interfaceStats):
                                    for index,iter_interfaceStats in enumerate(interfaceStats):
                                        BW_Site[index] += (iter_interfaceStats['tx_kbps']+iter_interfaceStats['rx_kbps'])

                                else:
                                    for index in range(len(BW_Site)):
                                        BW_Site[index] += (interfaceStats[index]['tx_kbps']+interfaceStats[index]['rx_kbps'])





                """
                calcualting the peak cumulative BW and convert kbps to Mbps
                Associate a LIC tier based of the peak cumulative BW
                """

                if BW_Site != []:
                    AggMbps = (max(BW_Site))/1000

                    for iterSystemIP in systemIPlst:
                        report_data[(str(site_id),iterSystemIP)]["BW-Agg-Site-Mbps"] = AggMbps
                        report_data[(str(site_id),iterSystemIP)]["License-Tier"] = Tier_Allocation.Tier_Allocation(AggMbps)


        """
        Dumping report_data dic to csv file
        need to add encryption
        """

        print(report_data)

        filename =  args.filename[0]
        fields = [ "Site_ID-System_IP", "host-name", "uuid", "reachability", "validity", "BW-Agg-Site-Mbps","License-Tier" ]
        fileEmpty = not(os.path.isfile(filename))

        print(f"Report Generated {filename}")


        with open(filename,'a') as f:
            w = csv.DictWriter(f,fields)
            if fileEmpty:
                w.writeheader()
            for k in report_data:
                w.writerow({field: report_data[k].get(field) or k for field in fields})


        exit()
