import cv2
import numpy as np
from PIL import Image,ImageTk
import tkinter as tk
import tkinter.messagebox as tkMessageBox
import pymysql
from BMode import *
import scipy.io as spio
import os
import gc
import multiprocessing as mp
from functools import partial
from scipy import interpolate

def click_and_crop(event, x, y, flags, image):
    # grab references to the global variables
    global refPt,cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

        # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        #image = cv2.imread(imgaddr)
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)


def ROIselection(cur):
    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(image_list[cur])
    # Select ROI
    r = cv2.selectROI("Image", image, False, False)

    refPt[0][0]=int(r[0])
    refPt[1][0]=int(r[0]+r[2])
    refPt[0][1]=int(r[1])
    refPt[1][1]=int(r[1]+r[3])
    
    # Crop image
#    imCrop = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    
#    clone = image.copy()
#    cv2.namedWindow("image")
#    cv2.setMouseCallback("image", click_and_crop, image)
#
#    # keep looping until the 'q' key is pressed
#    while True:
#        # display the image and wait for a keypress
#        cv2.imshow("image", image)
#        key = cv2.waitKey(1) & 0xFF
#
#        # if the 'r' key is pressed, reset the cropping region
#        if key == ord("r"):
#            image = clone.copy()
#
#        # if the 'c' key is pressed, break from the loop
#        elif key == ord("c"):
#            break
#
    print(refPt)
# 
#    # if there are two reference points, then crop the region of interest
#    # from teh image and display it
#    if len(refPt) == 2:
#        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
#        cv2.imshow("ROI", roi)
#        cv2.waitKey(0)
    # Display cropped image
#    cv2.imshow("Image", imCrop)
#    cv2.waitKey(0)

    # close all open windows
    cv2.destroyAllWindows()

def move(delta):
    #Move between frames to find the best one
    global current, image_list
    if not (0 <= current + delta < len(image_list)):
        tkMessageBox.showinfo('End', 'No more image.')
        return
    current += delta
    image = Image.open(image_list[current])
    
    image = ImageTk.PhotoImage(image)

    
    label['text'] = text_list[current]
    label['image'] = image
    label.photo = image


# Function to parallelize
def BM_RF_ROI(k,BMData,RFData,YY,XX, pr, rc, dep, ddx, ddr, ddt,dirData,cid):
            #Save ROI from BMode data and its related RF data
            print("I am working: ",k)
            kk=int(k)
            i=int(kk/4)
            j=kk % 4
            BM_dict={"indx": np.array([2,2]), "data": np.array([YY[i+1]-YY[i],XX[j+1]-XX[j]])}

            BMode_ROI = np.zeros([616, 756])
            BMode_ROI[YY[i]:YY[i+1],XX[j]:XX[j+1]]=255

            temp=BMData[YY[i]:YY[i+1],XX[j]:XX[j+1],:]
            BM_dict["indx"]=[[YY[i],YY[i+1]],[XX[j],XX[j+1]]]
            BM_dict["data"]=temp

            both_img = cv2.flip(BMode_ROI, 0)
            
            q = BMtoRF(both_img, pr, rc, dep, [ddx, ddx, ddr, ddt])
            cv2.imwrite('RFTest.jpg', q)
            
            where_are_NaNs = np.isnan(q)
            q[where_are_NaNs] = 0
            
            maxRF=max(map(max, q))
            RF_ind = np.nonzero(q>(0.1*maxRF))

            RF_ROI_Data=RFData[RF_ind[0],RF_ind[1],:]
            RF_dict={"indx": [RF_ind[0],RF_ind[1]], "data": RF_ROI_Data}
            
            RF_dict["data"]=RF_ROI_Data
            
            spio.savemat(dirData+'\BMode\ROI_Data'+'\BM_ROI_Data_'+str(cid).zfill(2)+'_'+str(k).zfill(3)+'.mat',{'BMROI':BM_dict})
            spio.savemat(dirData+'\BMode\ROI_Data'+'\RF_ROI_Data_'+str(cid).zfill(2)+'_'+str(k).zfill(3)+'.mat',{'RFROI':RF_dict})

            del BMode_ROI
            del temp
            del both_img
            del q
            del where_are_NaNs
            del RF_ind
            del RF_ROI_Data
            del BM_dict
            del RF_dict
            gc.collect()

            return 'Done'
def BMtoRF(p, prb_radius, arc, depth, resol):
    px_r = resol[2]
    px_th = resol[3]

    min_r = prb_radius
    max_r = prb_radius+depth

    max_y = prb_radius + depth
    nY = p.shape[0]
    nX = p.shape[1]
    maxX = nX/2 * resol[0]
    minX = -maxX



    max_theta = arc / prb_radius / 2
    min_theta = -max_theta

    rc = np.arange(min_r,max_r,px_r)
    thc = np.arange(min_theta, max_theta, px_th)


    min_y = prb_radius * np.cos(max_theta)

    x = np.arange(minX, maxX, resol[0])
    y = np.linspace(min_y, max_y, nY)
   
    xSR,ySR=np.meshgrid(x, y)


    rSR, tSR = np.meshgrid(rc,thc)

    sin = np.sin(tSR)
    cos = np.cos(tSR)
    px = rSR * sin
    py = rSR * cos

    new_grid = interpolate.griddata((xSR.flatten(),ySR.flatten()), p.flatten(), (px, py), method='cubic')
    q = new_grid.transpose()

    return q
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Transfer ROI from BMode  to RF@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Extract Params From Database@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def RFROISave(PatientNo):           
    global text_list,label,refPt


#    PatientNo = 59
    refPt = np.zeros([2,2])
    cropping = False
    
    
    folderp = 'Z:\\shared\\images\\ProstateVGH-2\\Data\\Patient' + str(PatientNo) + '\\'
    subfolders = os.listdir(folderp)
    Data_Path = folderp + subfolders[0]
    
    config = {
            'host': '137.82.56.208',
            'user': 'samareh',
            'password': 'samareh',
            'database' : "prostate"
            }
    
    cnx = pymysql.connect(**config)
    
    cur = cnx.cursor()
    
    sql_select_Query = "select NumberOfCores FROM patient WHERE ID="+str(PatientNo)
    cur.execute(sql_select_Query)
    NCores = cur.fetchall()
    
    BM = BMode(Data_Path,NCores[0][0])
    BM.BM_reader()
       
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Read Specifications from Database
    
    queryRFWidth = "SELECT RFWidth FROM patient WHERE ID="+str(PatientNo)
    cur.execute(queryRFWidth)
    RFWidth = cur.fetchall()
    nBlocks= 2*RFWidth[0][0]
    
    queryRFHight = "SELECT RFHight FROM patient WHERE ID="+str(PatientNo)
    cur.execute(queryRFHight)
    RFHight = cur.fetchall()
    nLines = RFHight[0][0]
    
    queryDepth = "SELECT Depth FROM patient WHERE ID="+str(PatientNo)
    cur.execute(queryDepth)
    depth = cur.fetchall()
    RF_depth = float(depth[0][0])*0.01
    
    querydX = "SELECT dX FROM patient WHERE ID="+str(PatientNo)
    cur.execute(querydX)
    dx = cur.fetchall()
    #dX is in cm
    dX = dx[0][0]*0.01  
    
    queryInv = "SELECT Revert FROM core WHERE PatientId="+str(PatientNo)
    cur.execute(queryInv)
    inversion = cur.fetchall()
     
    prb_width =0.0221;
    prb_radius = 0.01186;
    arc = np.arcsin(prb_width/2/prb_radius)*2* prb_radius;
    dR = RF_depth/nBlocks;
    dT = arc/nLines/prb_radius;
    
    sqlquary = "UPDATE patient SET dR = "+str(dR)+", dT = "+ str(dT)+" WHERE ID = " + str(PatientNo)
    cur.execute(sqlquary)
    
        
    #P=Patient(BM.NofCores)
    RF_Data=RF(BM.dir, BM.NofCores, nBlocks, nLines)
    RF_Data.RF_reader(inversion)
    
    if not os.path.exists(BM.dir+"\BMode\ROI_Data"):
        os.makedirs(BM.dir+"\BMode\ROI_Data")
        
    if not os.path.exists(BM.dir+"\BMode\ROI_Data\TestImages"):
        os.makedirs(BM.dir+"\BMode\ROI_Data\TestImages")
       
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Whole Prostate Path
    Data_Path_w = Data_Path+'\\BMode\\ROI_Data\\WholeProstate\\'  
    f=[]
    for (filenames) in os.walk(Data_Path_w):
        f.extend(filenames)
        break

    try:
        path=BM.dir+'\BMode\ROI_Data\OutProstate'
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
        
    global current, image_list, root
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ROI Selection
#int(BM.NofCores/2),
    for CoreID in range(BM.NofCores):
        
            NeedleFrame=-1
            queryInv = "SELECT NeedleFrame FROM core WHERE (PatientId="+str(PatientNo)+" AND CoreId="+str(CoreID)+')'
            cur.execute(queryInv)
            tmp = cur.fetchall()
            NeedleFrame=tmp[0][0]
            
            
            if NeedleFrame==0:
                continue 
            NDLE_Flag=BM.Find_Needle(CoreID,NeedleFrame)
            if not NDLE_Flag:
                continue    # continue here
            current = 0
            text_list=[]
            image_list=[]
            needleframe = int(BM.NeedleFrame[CoreID])
            for i in range(10):
                image_list.append(BM.imagepath[CoreID][i])
                text_list.append(str(needleframe-1+i))


            root = tk.Tk()
            label = tk.Label(root, compound=tk.TOP)
            label.pack()

            tk.Button(root, text='Previous picture', command=lambda: move(-1)).pack(side=tk.LEFT)
            tk.Button(root, text='Next picture', command=lambda: move(+1)).pack(side=tk.LEFT)
            tk.Button(root, text='Quit', command=root.destroy).pack(side=tk.LEFT)
            tk.Button(root, text='SelectROI', command=lambda: ROIselection(current)).pack(side=tk.LEFT)
            #tk.Button(root, text='Find Needle', command=lambda: BM.Find_Needle(CoreID)).pack(side=tk.LEFT)

            move(0)
           
            root.mainloop()


    



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Transfer ROI from BMode  to RF@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

            ndlcenter = (refPt[0][0]+refPt[1][0])/2
            nx = 0.002/dX
            ny = 0.018/dX
            Ndl_Offset = int(0.005/dX)
            L = int(np.ceil(ndlcenter-nx/2))
            R = int(np.ceil(ndlcenter+nx/2))
            T = int(refPt[0][1]) +Ndl_Offset#616-int(refPt[0][1]) +Ndl_Offset
            B = T+int(ny)
            rem= (L-R) % 4
            L=L+int(rem/2)
            R=R-(rem-int(rem/2))
            rem= (B-T) % 36
            B=B+36-rem
            XW=range(L,R+1,int((R-L)/4))
            YW=range(T,B+1,int((B-T)/36))
          
            XPixels= int((R-L)/4)
            YPixels= int((B-T)/36)
    
#            BMode_ROI_test = np.zeros([616, 756,3])
#            BMode_ROI_test[refPt[0][1]:refPt[1][1],refPt[0][0]:refPt[1][0],:]=10
#            RF_ROI_test = np.zeros([nBlocks,nLines,3])            
            BMD=BM.BM_Data[CoreID,]
            RFD=RF_Data.RF_Frames[CoreID,]
            dirD=BM.dir
            
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Save Around needle ROI (2mm X 18mm)
            BM_dict={"indx": np.array([2,2]), "data": np.array([B-T,R-L])}

            BMode_ROI = np.zeros([616, 756])
            BMode_ROI[T:B,L:R]=255
            
            if inversion[CoreID][0]==0:
                both_img = cv2.flip(BMode_ROI, -1)
            else:
                both_img = cv2.flip(BMode_ROI, 0)
                
            img=np.squeeze(np.asarray(BMD[:,:,0]))
            
            
                        
            image=cv2.cvtColor(np.uint8(img), cv2.COLOR_GRAY2RGB)
           	
            overlay = image.copy()
            output = image.copy()
 
        	# draw a red rectangle surrounding Adrian in the image
        	# along with the text "PyImageSearch" at the top-left
        	# corner
            cv2.rectangle(overlay, (L, T), (R,B),(0, 0, 255), -1)
            # apply the overlay
            alpha=0.5
            cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
#            cv2.imshow("Output", output)
#            cv2.waitKey(0)
            cv2.imwrite(BM.dir+'\BMode\ROI_Data\TestImages'+"\BMROI_mask_"+str(CoreID)+".bmp",BMode_ROI)
            cv2.imwrite(BM.dir+'\BMode\ROI_Data\TestImages'+"\BMROI_test_"+str(CoreID)+".bmp",overlay)
            
           
            temp=BMD[T:B,L:R,:]
            BM_dict["indx"]=[T,B,L,R]
            BM_dict["data"]=temp
            

         
            RF_ROI = BMtoRF(both_img, prb_radius, arc, RF_depth, [dX, dX, dR, dT])
            RF_ROI = RF_ROI[:,0:nLines]
            
            where_are_NaNs = np.isnan(RF_ROI)
            RF_ROI[where_are_NaNs] = 0
#            cv2.imwrite(BM.dir+'\BMode\ROI_Data'+"\RFROI_test"+str(CoreID)+".jpg",RF_ROI)
            
            #Read Prostate Mask
            for files in f[2]:
               if ('PR_mask_A'+str(CoreID)) in files:
                        mask=files
            Prostate_mask = cv2.imread(Data_Path_w+mask)             

            #save RF without applying prostate mask
            RF_ROI_18=RF_ROI
            maxRF=max(map(max, RF_ROI_18))
            RF_ROI_18[RF_ROI_18<(0.1*maxRF)]=0;
                        
            RF_ROI_18_Data=RFD[RF_ROI_18>0,:]
            RF_dict_18={"indx": np.where(RF_ROI_18), "data": RF_ROI_18_Data}
            spio.savemat(BM.dir+'\BMode\ROI_Data\OutProstate'+'\RF_ROI_Data_'+str(CoreID).zfill(2)+'.mat',{'RFROI':RF_dict_18})    
            spio.savemat(BM.dir+'\BMode\ROI_Data\OutProstate'+'\BM_ROI_Data_'+str(CoreID).zfill(2)+'.mat',{'BMROI':BM_dict})
            
            #save RF after applying prostate mask
            RF_ROI=np.multiply(RF_ROI,Prostate_mask[:,:,0])
            cv2.imwrite(BM.dir+'\BMode\ROI_Data\TestImages'+"\RFROI_mask_"+str(CoreID)+".bmp",RF_ROI)
            
            maxRF=max(map(max, RF_ROI))
            RF_ROI[RF_ROI<(0.1*maxRF)]=0;
                        
            RF_ROI_Data=RFD[RF_ROI>0,:]

            img=np.squeeze(np.asarray(RFD[:,:,0]))
            img=np.log10(1+np.abs(img));
            img=img*255/np.max(img)
            image=cv2.cvtColor(np.uint8(img), cv2.COLOR_GRAY2RGB)
           	
            overlay = image.copy()
            output = image.copy()
 
        	# draw a red rectangle surrounding Adrian in the image
        	# along with the text "PyImageSearch" at the top-left
        	# corner
            overlay[RF_ROI>0,0]=255
            overlay[RF_ROI>0,1]=0
            overlay[RF_ROI>0,2]=0
            
            cv2.imwrite(BM.dir+'\BMode\ROI_Data\TestImages'+"\RFROI_test_"+str(CoreID)+".bmp",overlay)
            
            RF_dict={"indx": np.where(RF_ROI), "data": RF_ROI_Data}
            
            RF_dict["data"]=RF_ROI_Data
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ROI saving BMode and RF
            

            spio.savemat(BM.dir+'\BMode\ROI_Data'+'\RF_ROI_Data_'+str(CoreID).zfill(2)+'.mat',{'RFROI':RF_dict})



            
            del BMD
            del RFD
            gc.collect()
            
       
    cnx.commit()
    cnx.close()

    BM.FreeMemory()