# LIC_TLOC

~~~
(venv) shreredd@SHREREDD-M-856H LIC_TLOC % python3 lic_tloc.py -a vmanage-1.sdwan.cisco.com -p 8443 -u shreredd -pw Reddy sid -id 1201 1202 2123 2202 -tlocext yes -filename vmanage_1_sdwan_cisco_com_1.csv


 Getting info related to SITE-ID 1201
 Getting WAN Parent interface info from 1.1.1.201
 Getting info related to SITE-ID 1201
 Getting WAN Parent interface info from 1.1.1.202
 determine if the TLOC EXT is present
pulling the interface stats of Site-ID 1201 -- System-IP 1.1.1.201 -- TLOC parent Interface Cellular0/2/0
pulling the interface stats of Site-ID 1201 -- System-IP 1.1.1.201 -- TLOC parent Interface GigabitEthernet0/0/0
pulling the interface stats of Site-ID 1201 -- System-IP 1.1.1.201 -- TLOC parent Interface GigabitEthernet0/0/1
pulling the interface stats of Site-ID 1201 -- System-IP 1.1.1.202 -- TLOC parent Interface GigabitEthernet0/0/0
pulling the interface stats of Site-ID 1201 -- System-IP 1.1.1.202 -- TLOC parent Interface GigabitEthernet0/0/1


 Getting info related to SITE-ID 1202
 Getting WAN Parent interface info from 1.1.1.203
 Getting info related to SITE-ID 1202
 Getting WAN Parent interface info from 1.1.1.204
 determine if the TLOC EXT is present
pulling the interface stats of Site-ID 1202 -- System-IP 1.1.1.203 -- TLOC parent Interface GigabitEthernet0/0/0
pulling the interface stats of Site-ID 1202 -- System-IP 1.1.1.203 -- TLOC parent Interface GigabitEthernet0/0/1
pulling the interface stats of Site-ID 1202 -- System-IP 1.1.1.204 -- TLOC parent Interface GigabitEthernet0/0/0
pulling the interface stats of Site-ID 1202 -- System-IP 1.1.1.204 -- TLOC parent Interface GigabitEthernet0/0/1

 Getting info related to SITE-ID 2123
 UUID - ISR4331/K9-FDO21  System-IP - 2.2.2.123  is either Unreachable or in Invalid/Staging Mode
 Getting info related to SITE-ID 2123
 UUID - ISR4331/K9-FDO22  System-IP - 2.2.2.124  is either Unreachable or in Invalid/Staging Mode


 Getting info related to SITE-ID 2202
 UUID - C1111X-8P-FGL2317921Z  System-IP - 2.2.2.202  is either Unreachable or in Invalid/Staging Mode
 Getting info related to SITE-ID 2202
 UUID - C1111-8PLTEEA-FGL232312KX  System-IP - 2.2.2.201  is either Unreachable or in Invalid/Staging Mode


Report Generated vmanage_108330488_sdwan_cisco_com_1.csv




(venv) shreredd@SHREREDD-M-856H LIC_TLOC % more vmanage_108330488_sdwan_cisco_com_1.csv
Site_ID-System_IP,host-name,uuid,reachability,validity,BW-Agg-Site-Mbps,License-Tier
"('1201', '1.1.1.201')",Branch-1A,C1111-8PLTEEA-FCZ1,reachable,valid,0.6605,T0
"('1201', '1.1.1.202')",Branch-1B,C1111-8PLTEEA-FCZ2,reachable,valid,0.6605,T0
"('1202', '1.1.1.203')",Branch-2A,C1111-8PLTEEA-FC1,reachable,valid,0.45833333333333337,T0
"('1202', '1.1.1.204')",Branch-2B,C1111-8PLTEEA-FC2,reachable,valid,0.45833333333333337,T0
"('2123', '2.2.2.123')",PITTSBURGH1-TK,ISR4331/K9-F1,unreachable,valid,"('2123', '2.2.2.123')","('2123', '2.2.2.123')"
"('2123', '2.2.2.124')",PITTSBURGH2-TK,ISR4331/K9-F2,unreachable,valid,"('2123', '2.2.2.124')","('2123', '2.2.2.124')"
"('2202', '2.2.2.202')",PRIMARY-1111X-8P-2,C1111X-8P-FGL21,unreachable,valid,"('2202', '2.2.2.202')","('2202', '2.2.2.202')"
"('2202', '2.2.2.201')",Secondary-1111LTEEA-8P-1,C1111-8PLTEEA-FG2,unreachable,valid,"('2202', '2.2.2.201')","('2202', '2.2.2.201')"
