import cv2 as cv
import tensorflow as tf
import numpy as np
import os.path
import uuid
from ShadowAiDjango.settings import MEDIA_ROOT,STATIC_URL,BASE_DIR

class ShadowAiModel():
    def __init__(self):
        self.model=tf.keras.models.load_model(os.path.join(BASE_DIR+STATIC_URL+'AnimeColorizationModelv7.h5'))
        self.images=None
    
    def load_image(self, filelist):
        image_set=[]
        for f in filelist:
            raw_img=cv.imread(f)
            resize_img=cv.resize(cv.cvtColor(raw_img,cv.COLOR_BGR2RGB),(256,256))
            image_set.append(np.asarray(resize_img,dtype=int))
        image_set_array=np.asarray(image_set)

        #print(image_set_array[0].shape,image_set_array.shape)
        #plt.imshow(image_set[0])
        #plt.show()

        image_set_array=image_set_array/127.5 -1
        self.images=image_set_array
        
    def predict(self, fileFormat, fileSizes,shadow):
        dst=[]
        prefix=MEDIA_ROOT+'/processed/'
        if not os.path.exists(prefix):
            os.mkdir(prefix)

        if self.images is None:
            print('no image set')
            return
        prediction=self.model.predict(self.images[:])
        for i in range(len(prediction)):
            np.clip(prediction[i],0,1,prediction[i])    #clip to value [0..1]
            ui8_data=( prediction[i] * 255/ (np.max( prediction[i] ))).astype('uint8') #float32 to uint8
            
            '''if shadow!='#FFAC73':
                src=(self.images[i]*255/ (np.max(self.images[i]))).astype('uint8')
                whitespace=np.ones((256,256,1),dtype=np.uint8)*255
                gray_src=cv.cvtColor(src,cv.COLOR_RGB2GRAY)
                new_r_value=255-int(shadow[1:3],16)
                new_g_value=255-int(shadow[3:5],16)
                new_b_value=255-int(shadow[5:7],16)
                shadowArea=src-ui8_data
                r=shadowArea[:,:,0]
                g=shadowArea[:,:,1]
                b=shadowArea[:,:,2]
                shadowArea=cv.cvtColor(shadowArea,cv.COLOR_RGB2BGR)
                cv.imwrite('r.png',r)
                cv.imwrite('g.png',g)
                cv.imwrite('b.png',b)
                new_r=gray_src-r
                new_g=gray_src-g
                new_b=gray_src-b
                new_r[new_r>new_r_value]=new_r_value
                new_g[new_g>new_g_value]=new_g_value
                new_b[new_b>new_b_value]=new_b_value
                
                cv.imwrite('new_r.png',new_r)
                cv.imwrite('new_g.png',new_g)
                cv.imwrite('new_b.png',new_b)
                #cv.imwrite('org.png',cv.cvtColor(src,cv.COLOR_BGR2RGB))
                cv.imwrite('shadow.png',shadowArea)
                cv.imwrite('off.png',cv.merge((new_b,new_g,new_r)))'''
            
            ui8_data=cv.cvtColor(ui8_data,cv.COLOR_BGR2RGB)   #initial ui8_data is considered to RGB, but
                                                #cv2 imwrite function read byte as BGR then save to RGB
            
            resized=cv.resize(ui8_data,fileSizes[i])
            name=str( uuid.uuid4() ) + fileFormat
            cv.imwrite(prefix + name,resized)
            
            dst.append(name)
        
        return dst

    