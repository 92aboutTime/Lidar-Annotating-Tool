import os
import shutil
from tqdm import tqdm
import pandas as pd


def tracking_id_check(folder):
    try:
        label_list = sorted(os.listdir(os.path.join(folder,'lidar','lidar_label')))
    except:
        print(folder)
        return
    
    result = {}
    
    for i in label_list:
        with open(os.path.join(folder,'lidar','lidar_label', i), mode ='rt', encoding = 'utf-8') as label:
            line = None
            tracking_list = []
            
            while line != '':
                line = label.readline()
                tracking_list.append(line.split(' ')[0])
            
            count_result = []
            
            for tracking_id in tracking_list:
                if tracking_list.count(tracking_id) > 1:
                    count_result.append(tracking_id)
            
            if len(count_result) > 0:
                count_result = list(set(count_result))
                # i에서 중복이 있는지 없는지 확인한 결과가 count_result
                
                
                result[i] = count_result
    if len(result) > 0 :
        print(folder)
        
        for key, value in result.items():
            print("{}  :  {}".format(key, value))
        
        print("\n")
    return result


def check_tracking_id_volume1(): 
    U_dan_path = '/volume1/가공완료데이터/dan'
    U_jeon_path = '/volume1/가공완료데이터/jeon'

    df_dan = pd.DataFrame(columns = ['폴더', 'label_번호', '중복_tracking_id'])
    j = 0

    for folder_a in tqdm(os.listdir(U_dan_path)):
        result = tracking_id_check(os.path.join(U_dan_path, folder_a))
        
        for i in range(len(result)):
            popitem = result.popitem()
            df_dan.loc[j] = [folder_a, popitem[0], popitem[1]]
            j = j+1
                
    df_dan.to_csv('C:\\Users\\wq_ysw\\Desktop\\Lidar\\tracking_id_중복_단방향.csv', mode='w', index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    # df_dan.to_csv('C:\\Users\\wq_ysw\\Desktop\\Lidar\\tracking_id_중복_단방향.csv', mode='w', index=False, encoding='utf-8-sig') 변경 필요함.
    # check_tracking_id_volume1()