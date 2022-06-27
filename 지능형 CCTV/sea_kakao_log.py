from kafka import KafkaProducer
from email.policy import default
import os
from pickle import TRUE
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ['KMP_DUPLICATE_LIB_OK']= "1"
import sys
sys.path.insert(0, './yolov5')
import re
import json
import argparse
from datetime import datetime
import os
import platform
import shutil
import time
from pathlib import Path
import numpy as np
import cv2
import torch
import pandas as pd
import torch.backends.cudnn as cudnn
from datetime import timedelta
from datetime import datetime
from yolov5.models.experimental import attempt_load
from yolov5.utils.downloads import attempt_download
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.datasets import LoadImages, LoadStreams, VID_FORMATS
from yolov5.utils.general import (LOGGER, check_img_size, non_max_suppression, scale_coords,
                                  check_imshow, xyxy2xywh, increment_path, strip_optimizer, colorstr)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors, save_one_box
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
from cleantext import clean_text, list_to_delete, strip_text
from kakaotalk import sendToMeMessage
from shapely.geometry import Polygon,MultiPoint
from pymongo import MongoClient
import mysql.connector
from collections import Counter
client=MongoClient('mongodb://127.0.0.1:27017/')
db = client['admin']
collection = db['cctv2']
producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 deepsort root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
## 이상탐지 행동시 필요한 빈 리스트 생성
ppoint=[] # 설정 구역 좌표를 받기위한 리스트
#file = open("points.txt", "r")  #설정 구역에 대한 좌표값 호출 (1/3)
cctvid='1'
#info='1'
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   passwd="1234",
   database="loitering_log2"
)
mycursor = mydb.cursor(buffered=TRUE)

ppoint1 = []
ppoint2 = []
sql1 = "select points from cctv_info where info = 'loitering';"
sql2 = "select points from cctv_info_sea where info = 'invasion';"
#mycursor.execute(sql1)
#data1 = mycursor.fetchall()
#data1 = strip_text(clean_text(str(data1)),ppoint1)
#mydb.commit()
mycursor.execute(sql2)
data2 = mycursor.fetchall()
data2 = strip_text(clean_text(str(data2)),ppoint2)
mydb.commit()

list_res = []
list_list=[] # 침입 알람 설정시 필요한 리스트
xlist_list=[] # 배회 알람 설정시 필요한 리스트
alist_list=[] # 쓰러짐 알람 설정시 필요한 리스트


    
def detect(opt):
    out, source, yolo_model, deep_sort_model, show_vid, save_vid, save_txt, imgsz, evaluate, half, \
        project, exist_ok, update, save_crop = \
        opt.output, opt.source, opt.yolo_model, opt.deep_sort_model, opt.show_vid, opt.save_vid, \
        opt.save_txt, opt.imgsz, opt.evaluate, opt.half, opt.project, opt.exist_ok, opt.update, opt.save_crop
    webcam = source == '0' or source.startswith(
        'rtsp') or source.startswith('http') or source.endswith('.txt')

    # Initialize
    device = select_device(opt.device)
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # The MOT16 evaluation runs multiple inference streams in parallel, each one writing to
    # its own .txt file. Hence, in that case, the output folder is not restored
    if not evaluate:
        if os.path.exists(out):
            pass
            shutil.rmtree(out)  # delete output folder
        os.makedirs(out)  # make new output folder

    # Directories
    if type(yolo_model) is str:  # single yolo model
        exp_name = yolo_model.split(".")[0]
    elif type(yolo_model) is list and len(yolo_model) == 1:  # single models after --yolo_model
        exp_name = yolo_model[0].split(".")[0]
    else:  # multiple models after --yolo_model
        exp_name = "ensemble"
    exp_name = exp_name + "_" + deep_sort_model.split('/')[-1].split('.')[0]
    save_dir = increment_path(Path(project) / exp_name, exist_ok=exist_ok)  # increment run if project name exists
    (save_dir / 'tracks' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    model = DetectMultiBackend(yolo_model, device=device, dnn=opt.dnn)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Half
    half &= pt and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
    if pt:
        model.model.half() if half else model.model.float()

    # Set Dataloader
    vid_path, vid_writer = None, None
    # Check if environment supports image displays
    if show_vid:
        show_vid = check_imshow()

    # Dataloader
    if webcam:
        show_vid = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        nr_sources = len(dataset)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        nr_sources = 1
    vid_path, vid_writer, txt_path = [None] * nr_sources, [None] * nr_sources, [None] * nr_sources
    
    # initialize deepsort
    cfg = get_config()
    cfg.merge_from_file(opt.config_deepsort)

    # Create as many trackers as there are video sources
    deepsort_list = []
    for i in range(nr_sources):
        deepsort_list.append(
            DeepSort(
                deep_sort_model,
                device,
                max_dist=cfg.DEEPSORT.MAX_DIST,
                max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
            )
        )
    outputs = [None] * nr_sources

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names

    # Run tracking
    model.warmup(imgsz=(1 if pt else nr_sources, 3, *imgsz))  # warmup
    dt, seen = [0.0, 0.0, 0.0, 0.0], 0
    for frame_idx, (path, im, im0s, vid_cap, s) in enumerate(dataset):
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255.0  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        visualize = increment_path(save_dir / Path(path[0]).stem, mkdir=True) if opt.visualize else False
        pred = model(im, augment=opt.augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, opt.classes, opt.agnostic_nms, max_det=opt.max_det)
        dt[2] += time_sync() - t3
        # Process detections
        for i, det in enumerate(pred):  # detections per image
            seen += 1
            if webcam:  # nr_sources >= 1
                p, im0, _ = path[i], im0s[i].copy(), dataset.count
                p = Path(p)  # to Path
                s += f'{i}: '
                txt_file_name = p.name
                save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
            else:
                p, im0, _ = path, im0s.copy(), getattr(dataset, 'frame', 0)
                p = Path(p)  # to Path
                # video file
                if source.endswith(VID_FORMATS):
                    txt_file_name = p.stem
                    save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
                # folder with imgs
                else:
                    txt_file_name = p.parent.name  # get folder name containing current img
                    save_path = str(save_dir / p.parent.name)  # im.jpg, vid.mp4, ...

            txt_path = str(save_dir / 'tracks' / txt_file_name)  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            imc = im0.copy() if save_crop else im0  # for save_crop

            annotator = Annotator(im0, line_width=2, pil=not ascii)

            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                    
                xywhs = xyxy2xywh(det[:, 0:4])
                confs = det[:, 4] #np.array 고유 ID
                clss = det[:, 5]
                #print(clss)
                # pass detections to deepsort
                t4 = time_sync()
                outputs[i] = deepsort_list[i].update(xywhs.cpu(), confs.cpu(), clss.cpu(), im0)
                t5 = time_sync()
                dt[3] += t5 - t4
                print('----------------------------------')                  
                # 객체 탐지 후 BBOX를 그림
                if len(outputs[i]) > 0: # 만약 객체가 탐지되었을 경우
                    for j, (output, conf) in enumerate(zip(outputs[i], confs)): 
                        bboxes = output[0:4] # 왼쪽의 x값(xmin),상단의 y값(ymin),오른쪽의 x값(xmax), 하단의 y값(ymax) 
                        asd = output[4:-1]
                        yf = asd.tolist()
                        id = output[4] #추적한 id
                        cls = output[5] #탐지한 class EX) 사람 : 0 , 5ybv 머리 : 1
                        x1,y1,x2,y2 = output[0],output[1],output[2],output[3]
                        multi_point = MultiPoint([(x1,y1), (x2,y1), (x1,y2), (x2,y2)])
                        x = x1+(x2-x1)/2 #탐지한 객체의 X좌표 중앙값
                        y = y1+(y2-y1)/2 #탐지한 객체의 Y좌표 중앙값
                         #탐지한 객체의 중앙값 // <데이터 타입:Point>
                        #ban1 = np.array(ppoint1)#설정한 구역의 좌표를 numpy 행렬로 전환
                        ban2 = np.array(ppoint2)
                        #cv2.polylines(im0, np.int32([ban1]), True, (255, 0, 0), thickness=2) # 금지구역 눈에 보이게 그리기
                        cv2.polylines(im0, np.int32([ban2]), True, (0, 0, 255), thickness=2) # 배회구역 눈에 보이게 그리기
                        #ban_poly1 = Polygon(ppoint1) #numpy행렬로 바꾼 좌표를 다각형으로 연결
                        ban_poly2 = Polygon(ppoint2) 
                        #b = multi_point.within(ban_poly1)
                        c = multi_point.within(ban_poly2) #탐지한 객체의 중앙값과 다각형의 내부 외부 여부를 판별 
                        dx, dy = x2 - x1, y2 - y1 # dx : 탐지한 객체 BBOX의 가로 길이, dy : 탐지한 객체의 BBOX의 세로 길이
                        difference = dy-dx # BBOX의 세로길이에서 가로 길이를 뺀 값
                        pt1 = [x2-x, y1-y]
                        pt2 = [x1-x, y1-y]
                        ang1 = np.arctan2(*pt1[::-1])     # bbox_우하단 꼭지점과 원점 사이 각 : 둘 중 큰 각 (라디안)
                        ang2 = np.arctan2(*pt2[::-1])     # bbox_우상단 꼭지점과 원점 사이 각 : 둘 중 작은 각 (라디안)       
                        res = np.rad2deg((ang1-ang2) % (2*np.pi))     # 두 각(라디안) 사이의 차로 각도를 구함
                        bc_x = x1+(x2-x1)/2 #탐지한 객체의 X좌표 중앙값
                        bc_y = y1+(y2-y1)/2 
                        pt1 = (x2-bc_x, y1-bc_y) # bbox 우상단 - bbox_center(접점)   
                        pt2 = (x1-bc_x, y1-bc_y) # bbox 좌상단 - bbox_center(접점)
                        ang1 = np.arctan2(*pt1[::-1]) #역탄젠트(x/y)는 -> 좌표값을 (y,x) 순서로 함수에 적용하므로 pt1을 (x,y) 역순으로 불러와서 씀 
                        ang2 = np.arctan2(*pt2[::-1])
                        
                        x1,y1,x2,y2 = output[0],output[1],output[2],output[3]
                        res = np.rad2deg((ang1-ang2) % 360)
                        r = res.item()     # float
                        list_res.append(r)
                        list_to_delete(list_res)
                        
                        #쓰러짐
                        for x in list_res:
                            if (y2-y1)*1.1 <= (x2-x1) and x >= 90 and y2 <= 715 and y1 >=5 :# 조건1) BBOX 세로 길이 * 1.1 <= BBOX 가로 길이 + 조건 2) 각도 계산 후 직각~둔각일 경우
                                cv2.putText(im0, 'HY_CHECK_FALLDOWN!',(30,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),5)# 쓰러짐이라는 문구를 화면에 표기
                                alist_list.append(asd) # asd는 bbox가 그려진 객체의 re-id 값
                                list_to_delete(alist_list)
                                if alist_list.count(asd[0]) == 10: # re-id 값이 10번 나올경우
                                    sendToMeMessage('{}가 쓰러졌습니다.'.format(yf[0])) #카카오톡 알람 송출
                                    sql = "INSERT INTO cctv3 (cctvid, info, person_id, time_stamp,person_count) VALUES(%s, 'falling_down', '%s',DEFAULT,%s);" % (cctvid,str(yf[0]),f"{n}")# sql에 로그데이터 전송
                                    mycursor.execute(sql) # 위에서 설정한 mycursor 실행
                                    mydb.commit() # db에 데이터 전송 + 병합
                                else :
                                    pass
                            else:
                                pass          
                        ## 침입
                        if c == 1:  # 객체가 금지구역안에 들어갔을때
                            cv2.putText(im0, 'HY_CHECK_INTRUSION!',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),5)
                             # 추적한 id를 한프레임당 한개의 리스트로 전달
                            hello=list(set(xlist_list)) #추적한 고유 id 리스트로 저장 ex) [1,1,2,3,3,4] >> [1,2,3,4] # hello 리스트 안에는 고유값이 포함됨
                            list_list.append(yf) #빈리스트 list_list 안에 침입을 측정하기 위해 프레임별 id 저장
                            list_to_delete(list_list)
                            xlist_list.extend(yf) # 빈리스트 xlist_list 안에 배회를 측정하기 위해 한꺼번에 id 저장
                            if yf not in list_list[:-1]: # 고유 id가 프레임별 id에 저장되지 않았을 경우
                                sendToMeMessage('{}가 침입중입니다.'.format(yf[0])) # 침입중이라는 문구를 화면에 표기
                                LOGGER.info('{}가 침입중입니다.'.format(yf[0]))
                                    # 이것에 대한 이유는 전 프레임에 대한 정보를 불러올 수 없어 직접 추적한 객체 리스트중 하나를 제외하고
                                    # 비교하는것임. 알람을 한번만 울리게 하기 위해서.{n} {names[int(c)]}
                                sql = "INSERT INTO cctv3 (cctvid, info, person_id, time_stamp,person_count) VALUES(%s, 'invasion', '%s',DEFAULT,%s);" % (cctvid,str(yf[0]),f"{n}")
                                mycursor.execute(sql)
                                mydb.commit()
                                print(mycursor.rowcount,"record inserted.")
                                    
                            else : 
                                pass 
                        else : 
                            pass
                        # 배회 
                        if c == 1: 
                            
                            xlist_list.extend(yf)
                            ct = Counter(xlist_list)
                            for key,valu in ct.items():
                                if yf[0] == key and valu >=300:  # 구역에 300 frame 이상 중심점이 존재할 시 배회
                                    cv2.putText(im0, 'HY_CHECK_LOITERING!',(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),5)
                                    sendToMeMessage('{}가 배회중입니다.'.format(yf[0])) # KAKAO API로 자신에게 메시지 보내기
                                    LOGGER.info('{}가 배회중입니다.'.format(yf[0]))# 배회 로그를 표기(수정필요)
                                    sql = "INSERT INTO cctv3 (cctvid, info, person_id, time_stamp,person_count) VALUES(%s, 'loitering', '%s',DEFAULT,%s);" % (cctvid,str(yf[0]),f"{n}")
                                    mycursor.execute(sql)
                                    mydb.commit()
                                else:
                                    pass
                        else : 
                            pass
                        if save_txt: #파일 실행시 --save_txt 라는 문구를 작성할 경우
                            # to MOT format
                            bbox_left = output[0] # 객체 검출 왼쪽X 좌표(xmin)
                            bbox_top = output[1] # 객체 검출 상단Y 좌표(ymin)
                            bbox_w = output[2] - output[0] # 객체의 bbox 가로 길이
                            bbox_h = output[3] - output[1] # 객체의 bbox 세로 길이
                            
                            # Write MOT compliant results to file 
                            with open(txt_path + '.txt', 'a') as f:
                                f.write(('%g ' * 10 + '\n') % (frame_idx + 1, id, bbox_left,  # MOT format
                                                               bbox_top, bbox_w, bbox_h, -1, -1, -1, i))
                            
                        if save_vid or save_crop or show_vid:  # 작업할 프레임에 bbox를 씌워서 결과물 산출 
                            c = int(cls)  # cls 를 int로 변환하여 c 변수에 넣어줌 
                            label = f'{id} {names[c]} {conf:.2f}'  
                            annotator.box_label(bboxes, label, color=colors(c, True))
                            if save_crop:
                                txt_file_name = txt_file_name if (isinstance(path, list) and len(path) > 1) else ''
                                save_one_box(bboxes, imc, file=save_dir / 'crops' / txt_file_name / names[c] / f'{id}' / f'{p.stem}.jpg', BGR=True)

                LOGGER.info(f'{s}Done. YOLO:({t3 - t2:.3f}s), DeepSort:({t5 - t4:.3f}s)') # 하나 프레임 당 클래스 번호 & 프레임 크기 & 객체 개수 & 클래스 id & Yolo 계산 시간 & Deepsort 계산 시간 표기
            else:
                deepsort_list[i].increment_ages() 
                LOGGER.info('No detections') # 객체가 탐지되지 않았을 경우 로그를 표기

            # Stream results
            im0 = annotator.result() # 캠으로 표기하였을때
            if show_vid: # 만약 --show-vid 를 표기하면
                im1 = cv2.resize(im0, (1280,720), interpolation=cv2.INTER_AREA)
                ret, buffer = cv2.imencode('.jpg',im1)
                producer.send('sea',value=buffer.tobytes())
                cv2.imshow(str(p), im0) # p : 프레임 번호, im0 프레임 값
                mydict = {datetime.now().strftime("%Y-%m-%d %H:%M:%S"):im0.tobytes()}
                collection.insert_one(mydict)
                cv2.waitKey(1)  # 1 millisecond단위로 p와 im0을 호출하여 영상 송출
                
            # Save results (image with detections)
            if save_vid: # 만약 --save_vid 를 표기하면
                if vid_path[i] != save_path:  # 만약 저장 경로가 비디오 경로와 다르다면 
                    vid_path[i] = save_path    # 저장경로와 비디오 경로를 (기준:비디오경로) 일치시킴
                    if isinstance(vid_writer[i], cv2.VideoWriter): 
                        vid_writer[i].release()  # release previous video writer
                    if vid_cap:  # 영상일 경우
                        fps = vid_cap.get(cv2.CAP_PROP_FPS) # 초당 프레임 수
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # 초당 프레임의 가로길이
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 초당 프레임의 세로길이
                    else:  # 캠일 경우
                        fps, w, h = 30, im0.shape[1], im0.shape[0] # fps w , h  값을 고정 & 객체에 대한 길이 고정
                    save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                    vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                vid_writer[i].write(im0)
               
            

    # Print results
    t = tuple(x / seen * 1E3 for x in dt)  # 이미지 처리속도
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS, %.1fms deep sort update \
        per image at shape {(1, 3, *imgsz)}' % t) # 이미지 처리 속도를 로그로 출력 
    if save_txt or save_vid: # 만약 --save-txt 나 --save-vid를 사용할 시
        s = f"\n{len(list(save_dir.glob('tracks/*.txt')))} tracks saved to {save_dir / 'tracks'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}") # 저장경로와 저장 정보를 로그로 표기
    if update: 
        strip_optimizer(yolo_model)  # update model (to fix SourceChangeWarning)


if __name__ == '__main__': # -- 를 사용하기 위해 작성
    parser = argparse.ArgumentParser()
    parser.add_argument('--yolo_model', nargs='+', type=str, default='yolov5m.pt', help='model.pt path(s)')
    parser.add_argument('--deep_sort_model', type=str, default='osnet_ibn_x1_0_MSMT17')
    parser.add_argument('--source', type=str, default='0', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--show-vid', action='store_true', help='display tracking video results')
    parser.add_argument('--save-vid', action='store_true', help='save video tracking results')
    parser.add_argument('--save-txt', action='store_true', help='save MOT compliant results to *.txt')
    # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 16 17')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--evaluate', action='store_true', help='augmented inference')
    parser.add_argument("--config_deepsort", type=str, default="deep_sort/configs/deep_sort.yaml")
    parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detection per image')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--project', default=ROOT / 'runs/track', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand

    with torch.no_grad():
        detect(opt)
