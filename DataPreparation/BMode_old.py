import os,re
import numpy as np
import cv2
import gc
import subprocess
import scipy.io as spio
import pickle
def sort_files(fnames):
    #sorting the prostate files based on the serial number
    sortedfiles = {}
#    with os.scandir(path) as entries:
    for filename in fnames:
#            filename = entry.name
            if "Bmode" in filename:
                pos1=[pos for pos, char in enumerate(filename) if char == '_']
#                choppedfile = filename[6:]
#                pos1 = choppedfile.find('_')
#                realpos1 = pos1 + 6
                pos2 = filename.find('.')
                serial = int(filename[pos1[-1] + 1 :pos2])
                #filename = filename[:realpos1 +1 ]
                sortedfiles[serial] = filename
    sortedfiles =sorted(sortedfiles.items() , key=lambda sortedfiles: sortedfiles[0])
    return sortedfiles
class ROI:
    def __init__(self,array):
        self.data=array
class core:
    def __init__(self, NC,nx=0,ny=0,nT=0):
        self.NofCores = int(NC)
        if NC == 8:
            self.CoreLabels = ['RB', 'RML', 'RMM', 'RA', 'LB', 'LML', 'LMM', 'LA']
        else:
            if NC == 10:
                self.CoreLabels = ['RBL', 'RBM', 'RML', 'RMM', 'RA', 'LBL', 'LBM', 'LML', 'LMM', 'LA']
            else:
                self.CoreLabels = ['RBL', 'RBM', 'RML', 'RMM', 'RAL', 'RAM', 'LBL', 'LBM', 'LML', 'LMM', 'LAL', 'LAM']
        N = 80  # length
        array=np.zeros([nx,ny,nT])
        self.Core_Data = [ROI(array) for _ in range(N)]
#<SmallVolume>RB,RML,RMM,RA,LB,LML,LMM,LA</SmallVolume>
#<MediumVolume>RBL,RBM,RML,RMM,RA,LBL,LBM,LML,LMM,LA</MediumVolume>
#<LargVolume>RBL,RBM,RML,RMM,RAL,RAM,LBL,LBM,LML,LMM,LAL,LAM</LargVolume>
class Patient(core):
    def __init__(self, NC):
        core.__init__(self, NC)
        self.NofCores = int(NC)
        self.Data = [core(NC) for _ in range(NC)]
class BMode(core):
    Width = 756
    Height = 616
    Maxfilenum =20
    MaxBMnum = 1
    def __init__(self, dir, Ncores):
        core.__init__(self, Ncores)
        self.NofBM_Af_BPSY = np.zeros([self.NofCores, 1])
        self.dir = dir
        f=[]
        for (dirpath, dirnames, filenames) in os.walk(self.dir):
            f.extend(filenames)
            break
        f=sort_files(f)
        self.imagepath = np.empty([self.NofCores,10],dtype=object)
        self.BMfiles=f
#        for files in f:
#            if "Bmode" in files:
#                self.BMfiles.append(files)
        self.BMode_Bf_Bpsy = []
        for i in range(self.NofCores):
            self.BMode_Bf_Bpsy.append([])
        for files in self.BMfiles:
            for i in range(self.NofCores):
                if self.CoreLabels[i] in files[1]:
                    self.BMode_Bf_Bpsy[i].append(files[1])
        self.BMode_Af_Bpsy = []
        for i in range(self.NofCores):
            self.BMode_Af_Bpsy.append([])
            self.MaxBMnum=max(self.MaxBMnum,len(self.BMode_Bf_Bpsy[i]))
        for files in self.BMfiles:
            for i in range(self.NofCores):
                if 'A'+str(i)+'_' in files[1]:
                    if not files[1] in self.BMode_Bf_Bpsy[i]:
                        self.BMode_Af_Bpsy[i].append(files[1])
                        self.NofBM_Af_BPSY[i]+=1
        #self.Maxfilenum=int(min(20,max(self.NofBM_Af_BPSY)))#int(min(20,min(self.NofBM_Af_BPSY)))
        #self.BM_Frames = np.empty([self.NofCores,616,756,self.Maxfilenum*25])
        self.BM_Data = np.empty([self.NofCores,616,756,self.MaxBMnum*25])
        self.NeedleFrame = np.empty(self.NofCores)
    def BM_reader(self):
        for i in range(self.NofCores):
            for j in range(len(self.BMode_Bf_Bpsy[i])):
                data = np.fromfile(self.dir+'\\'+self.BMode_Bf_Bpsy[i][j], dtype='uint8')
                l = data.shape
                N = l[0] / (self.Width * self.Height)
                Frames = np.reshape(data, [self.Width, self.Height, int(N)], order='F')
                EachfileFrames=np.rot90(Frames, k=-1, axes=(0, 1))
                self.BM_Data[i, :, :, (j * 25):(25 * (j + 1))] = EachfileFrames
    def BM_Movie_Maker(self):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,50)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        if not os.path.exists(self.dir+'\BMode'):
            os.makedirs(self.dir+'\BMode')
        if not os.path.exists(self.dir + '\BMode\movie'):
            os.makedirs(self.dir + '\BMode\movie')
        for i in range(self.NofCores):
#self.Maxfilenum
            nframes=int(min(30,self.NofBM_Af_BPSY[i]))
            BM_Frames = np.empty([616,756,nframes*25])
            for j in range(nframes):
                data = np.fromfile(self.dir+"\\"+self.BMode_Af_Bpsy[i][j], dtype='uint8')
                if not data.size:
                    continue
                l = data.shape
                N = l[0] / (self.Width * self.Height)
                Frames=np.reshape(data,[self.Width, self.Height, int(N)],order='F')
                EachfileFrames=np.rot90(Frames, k=-1, axes=(0, 1))
                BM_Frames[:,:,(j*25):(25*(j+1))]= EachfileFrames
            BM_Frames = BM_Frames.astype(np.uint8)
            for inx in range(nframes*25): #(img_array.shape[2]):
                img=np.squeeze(BM_Frames[:,:,inx])
                imge = np.array(img,dtype=np.uint8)
                cv2.putText(imge,str(inx),
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)
                cv2.imwrite(self.dir+'\\BMode\\frame'+str(inx)+'.jpg', imge)
            # write BMode images in a video. It is used for background removal
            fnm="ffmpeg -r 5 -i ddd -vcodec mpeg4 -y movie.mp4"
            a=self.dir+"\\BMode\\frame%d.jpg"
            b=self.dir+"\BMode\movie\movie"+str(i)+".mp4"
            fnm=fnm.replace('ddd',a)
            fnm=fnm.replace('movie.mp4',b)
            os.system(fnm)
            folder=self.dir+'\\BMode\\'
            for f in os.listdir(folder):
                pathfile=os.path.join(folder, f)
                if os.path.isfile(pathfile):
                    os.remove(os.path.join(pathfile))
            del BM_Frames
            gc.collect()
    def NeedleDetection(self):
        for i in range(self.NofCores):
            b = self.dir + "\movie\movie" + str(i) + ".mp4"
            cap = cv2.VideoCapture(b)
            #initialization
            larr = []
            #background removal
            fgbg1 = cv2.bgsegm.createBackgroundSubtractorMOG()
            # Check if camera opened successfully
            if (cap.isOpened() == False):
                print("Error opening video stream or file")
            frameno = 0
            while (True):
                ret, frame = cap.read()
                frameno =frameno + 1;
                if ret == True:
                    fgmask = fgbg1.apply(frame)
                   #compute l0 norm for each frame foreground
                    nz = np.count_nonzero(fgmask)
                    larr = np.append(larr, nz)
                # Break the loop
                else:
                    break
            cap.release()
            diffarr=np.diff(larr)
            needleframe = np.argmax(diffarr)
            self.NeedleFrame[i]= needleframe
            if not os.path.exists(self.dir+'\BMode\AroundNeedle'):
                os.makedirs(self.dir+'\BMode\AroundNeedle')
            for k in range(10):
                imge = self.BM_Frames[i][:, :, needleframe - 1 + k]
                impath = self.dir + "\BMode\AroundNeedle\Frame_Af_BPSY_A" + str(i) + "_" + str(k) + ".jpg"
                self.imagepath[i][k]=impath
                cv2.imwrite(impath, imge)
    def Find_Needle(self,CoreID,needleframe):
        #Show Video of CoreID
        if needleframe==-1:
            dirp= self.dir + "\BMode\movie"
            videopath="movie" + str(CoreID) + ".mp4"
            os.chdir(dirp)
            if not os.path.isfile(videopath):
                return False
            p = subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe",videopath])
            #User should detect the frame number with the needle
            text = input("Enter the frame number: ")
            needleframe = int(text)
        self.NeedleFrame[CoreID] = needleframe
        #save 10 BMode files arround the needle
        number_of_packets_start=int(needleframe/25)
        number_of_packets_end=int((needleframe+10)/25)
        if not os.path.exists(self.dir+'\BMode\AroundNeedle'):
                os.makedirs(self.dir+'\BMode\AroundNeedle')
        BM_Af_Bpsy_path=[self.dir+"\\"+self.BMode_Af_Bpsy[CoreID][number_of_packets_start]]
        BM_Frames = np.empty([616,756,25])
        if number_of_packets_start!=number_of_packets_end:
                BM_Af_Bpsy_path.append(self.dir+"\\"+self.BMode_Af_Bpsy[CoreID][number_of_packets_end])
                BM_Frames = np.empty([616,756,2*25])
        for j in range(len(BM_Af_Bpsy_path)):
                data = np.fromfile(self.dir+"\\"+self.BMode_Af_Bpsy[CoreID][number_of_packets_start+j], dtype='uint8')
                l = data.shape
                N = l[0] / (self.Width * self.Height)
                Frames=np.reshape(data,[self.Width, self.Height, int(N)],order='F')
                EachfileFrames= np.rot90(Frames, k=-1, axes=(0, 1))
                BM_Frames[:,:,(j*25):(25*(j+1))]= EachfileFrames
        start_frame=needleframe % 25
        if start_frame==0:
            start_frame=1
        for k in range(10):
                imge = BM_Frames[:, :, start_frame - 1 + k]
                impath = self.dir + "\BMode\AroundNeedle\Frame_Af_BPSY_A" + str(CoreID) + "_" + str(k) + ".jpg"
                self.imagepath[CoreID][k]=impath
#                imge=cv2.flip(imge, 0) #Patient 59 is special case
                cv2.imwrite(impath, imge)
        del BM_Frames
        return True
    def FreeMemory(self):
        del self.NofBM_Af_BPSY
        del self.dir
        del self.imagepath
        del self.BMfiles
        del self.BMode_Bf_Bpsy
        del self.BMode_Af_Bpsy
        del self.BM_Data
        del self.NeedleFrame
        gc.collect()
    def BM_Seg_input(self,CoreID):
        [img_rows, img_cols] = [128, 128]
        All_BM_Frames = []
        nframes=len(self.BMode_Bf_Bpsy[CoreID])
        Frames=np.squeeze(self.BM_Data[CoreID,:,:,0:(25*nframes)])
        for k in range(nframes*25):
            data_paired = cv2.resize(Frames[:,:,k], (img_rows, img_cols))
            data_paired=np.rot90(data_paired, k=-1, axes=(0, 1))
            All_BM_Frames.append(data_paired)
        return All_BM_Frames
class RF(core):
    def __init__(self, dir, Ncores,RFWidth,RFHeight):
        core.__init__(self, Ncores)
        self.dir=dir
        self.RFHeight=RFHeight
        self.RFWidth=RFWidth
        self.RF_Frames = np.zeros([self.NofCores,self.RFWidth,self.RFHeight,200])
    def RF_reader(self,invert):
        for i in range(self.NofCores):
            for f in os.listdir(self.dir):
                if re.match("RF_A"+str(i), f):
                        files=f
            data = np.fromfile(self.dir+"\\"+files, dtype=np.int16)
            DataLen = data.shape[0]
            N = DataLen / (self.RFWidth * self.RFHeight)
            Frames=np.reshape(data,[self.RFWidth, self.RFHeight, int(N)],order='F')
            self.RF_Frames[i,:,:,:]= Frames
#            spio.savemat('test'+str(i)+'.mat',{'frames':Frames})
            #spio.savemat('test.mat',Frames)
#            if invert[i][0]!=0:
#                self.RF_Frames[i,:,:,:]= Frames
#                spio.savemat('test'+str(i)+'.mat',{'frames':Frames})
#            else:
#                self.RF_Frames[i,:,:,:]= np.flip(Frames,1)
#                spio.savemat('test'+str(i)+'.mat',{'frames':np.flip(Frames,1)})