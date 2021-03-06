from fileOI import filename_script_pair_tolist
import script_manipulate
from tqdm import tqdm
import fileOI
import random

def merge_script_like_libris(file_list, divider=' ', encoding='utf8'):
    dataset = []
    # step 01 : 파일리스트를 통해서 스크립트 읽기
    for file in file_list:
        temp = filename_script_pair_tolist(file, encoding)
        # step 01 -01 : u/ 이 삽입된 문장은 삭제
        if script_manipulate.is_remove_line(temp[1]):
            break
        temp[1] = remove_options(temp[1])
        dataset.append(temp)
        print(temp)
    return dataset


def remove_options(line):
    # step 02 : 잡음 제거하기
    line = script_manipulate.remove_noise_id(line, 'b/', 'i/', 'o/', 'n/', 'l/')
    # step 03 : 구두점 제거하기
    line = script_manipulate.remove_punctuation_rules(line, '.', ',', '?', '!', '+', '*')
    # step 04 : 이중전사 처리하기
    line = script_manipulate.change_number_to_pron(line)
    # step 05 : 이중전사 처리하기 (철자전사, 발음전사)
    line = script_manipulate.change_pron_to_dic(line)
    # step 06 : 자주 등장하는 영어 알파벳 한글화
    line = script_manipulate.replace_alphabet(line)
    return line


def merge_script_like_clova_call(file_list, encoding='utf8'):
    dataset = []
    # step 01 : 파일리스트를 통해서 스크립트 읽기
    for file in tqdm(file_list):
        temp = filename_script_pair_tolist(file, encoding)
        # step 01 -01 : u/ 이 삽입된 문장은 삭제
        if not script_manipulate.is_remove_line(temp[1]):
            temp[1] = remove_options(temp[1])
            filename = temp[0]
            text = temp[1]
            speaker_id = 0
            dic_temp = {'wav': '{}.wav'.format(filename), 'text': text, 'speaker_id': speaker_id}
            dataset.append(dic_temp)
    return dataset


def split_train_test_dataset_with_json(dataset, split_rate=0.2, encoding='utf8'):
    json_data = dataset
    random.shuffle(json_data)
    json_length = len(json_data)
    test_length = int(json_length*split_rate)
    testset = json_data[0:test_length]
    trainset = json_data[test_length:]
    return trainset, testset


def create_small_json(dataset, count=100):
    json_data = dataset[:count]
    fileOI.write_json_file(json_data, './output_test_small.json')


