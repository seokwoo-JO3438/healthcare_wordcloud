# -*- coding: utf-8 -*-
from konlpy.tag import Okt
from PIL import Image
import numpy as np
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def get_tags(text, ntags=50):
    # konlpy의 Twitter객체
    spliter = Okt()
    stop_words = "등 개 주 것 스케 헬 및 수 재 이 기자 위 고 를 말 무단 배포 통해 의 그 며"
    stop_words = stop_words.split(' ')
    word_tokens = spliter.nouns(text)
    result = []
    for w in word_tokens:
        if w not in stop_words:
            result.append(w)
   
    nouns = result
    # nouns 함수를 통해서 text에서 명사만 분리/추출
    count = Counter(nouns)
    # Counter객체를 생성하고 참조변수 nouns할당
    return_list = []  # 명사 빈도수 저장할 변수
    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c}
        return_list.append(temp)
    # most_common 메소드는 정수를 입력받아 객체 안의 명사중 빈도수
    # 큰 명사부터 순서대로 입력받은 정수 갯수만큼 저장되어있는 객체 반환
    # 명사와 사용된 갯수를 return_list에 저장합니다.
    return return_list

def main():
    text_file_name = "./news_data2/content.txt"
    output_file_name = "count.txt"
    # 분석할 파일
    noun_count = 70
    # 최대 많은 빈도수 부터 20개 명사 추출
    # count.txt 에 저장
    open_text_file = open(text_file_name, 'r',-1,"utf-8")
    open_output_file = open(output_file_name, 'w',-1,"utf-8")
    # 분석할 파일을 open
    text = open_text_file.read() #파일을 읽습니다.
    tags = get_tags(text, noun_count) # get_tags 함수 실행
    open_text_file.close()   #파일 close
    # 결과로 쓰일 count.txt 열기
    pro={}
    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))
        pro[noun] = count
    open_output_file.close()
    print(pro)
    mask = np.array(Image.open('./cross.png'))
    wordcloud = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf', background_color='white',mask=mask, width=2000,height=1800).generate_from_frequencies(pro)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
if __name__ == '__main__':
    main()




