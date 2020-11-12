import os
import pymysql
import pydicom

def dicom2dbs(Patient):              
    config = {
         'host': '137.82.56.208',
         'user': 'samareh',
         'password': 'samareh',
         'database' : "prostate"
    }
    
    cnx = pymysql.connect(**config)
    

    print(Patient)
    folderp='Z:\\shared\\images\\ProstateVGH-2\\Data\\Patient'+str(Patient)+'\\'
    subfolders=os.listdir(folderp)
    DICOM_Path=folderp+subfolders[0]+'\\Images\\DICOM'
    folders = []
    for r, d, f in os.walk(DICOM_Path):
        for dcmf in f:
            folders.append(os.path.join(DICOM_Path,dcmf))

    mypath=folders[0]
    info = pydicom.dcmread(mypath)  # plan dataset

#    Width=info.Rows
#    Height=info.Columns
    cinfo=info.SequenceOfUltrasoundRegions

    dXc=cinfo.__getitem__(0).__getitem__([0x0018, 0x602c])
    dX=dXc.value
#    dYc=cinfo.__getitem__(0).__getitem__([0x0018, 0x602e])
#    dY=dYc.value
    RP_X0_c=cinfo.__getitem__(0).__getitem__([0x0018, 0x6020])
    RP_X0=RP_X0_c.value
    RP_Y0_c=cinfo.__getitem__(0).__getitem__([0x0018, 0x6022])
    RP_Y0=RP_Y0_c.value

#    nBlocks = Height;
#    nLines =Width;
#    Rt               = 0.01186;
#    Probe_width      =0.0221;
#    dR               = RF_depth/nBlocks;                                   
#    arc              = np.arcsin(Probe_width/2/Rt)*2* Rt;
#    dT               = arc/nLines/Rt;   

   
    cur = cnx.cursor()
    query_str = "UPDATE patient SET dX ="+ str(dX)+" WHERE ID = " + str(Patient)
    cur.execute(query_str)
    query_str = "UPDATE patient SET referenceX =" + str(RP_X0)+ " WHERE ID = " + str(Patient)
    cur.execute(query_str)
    query_str = "UPDATE patient SET referenceY =" + str(RP_Y0) +" WHERE ID = " + str(Patient)
    cur.execute(query_str)
    cur.close()
    cnx.commit()
        
    
    
    cnx.close()


# In[ ]:




