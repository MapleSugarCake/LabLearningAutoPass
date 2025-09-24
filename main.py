import requests
import json
#script by MapleCake NJUPT2025管院新生

#版本号v0.2

#废弃的登录脚本
# def loginbash():
#     print("请输入账号：")
#     account=input()
#     print("请输入密码：")
#     password=input()
#     response1 = requests.get()


#发送完成课程信息
def finish_class(id, token):
    headers = {
        'Origin': 'http://10.22.192.38:9092',
        'Pragma': 'no-cache',
        'Referer': 'http://10.22.192.38:9092/',
        'content-type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'X-Access-Token': token
    }
    json_data = {'id': id}
    responses = requests.post(url='http://10.22.192.38:9090/jeecg-boot/jcedutec/courseSource/finish',headers=headers,json=json_data)
    print(responses.text)
    return responses.status_code

#借用学长的写法，不理解为什么我的json载荷会有几率出现acquire lock fail，换学长得就行了？
#或许是它答题有顺序要求？
class questinAnswer():
    def __init__(self, questionID , videoID , options) -> None:
        self.questionID = questionID
        self.videoID = videoID
        self.options = options


def get_question(id,token):
    headers = {
        'Referer': 'http://10.22.192.38:9092/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'X-Access-Token': token
    }
    url=f'http://10.22.192.38:9090/jeecg-boot/jcedutec/courseSource/queryCourseQuestionRelaByMainId?id={id}'
    res = []
    resp = requests.get(url, headers=headers)
    print(resp.text)
    received = json.loads(resp.content.decode('utf-8'))
    questionList = received['result']
    if questionList:
        for question in questionList:
            res.append(questinAnswer(question['id'], question['courseId'],
                                     question['correctAnswer'] if len(question['correctAnswer']) == 1 else question[
                                         'correctAnswer'].split(',')))
    print(f"课程{id}问题获取成功")
    #处理得到的received
    for a in res:
        solve_question(a,id,token)

def solve_question(ans,id,token):
    headers = {
        "Referer": "http://10.22.192.38:9092",
        'X-Access-Token': token
    }
    print(headers)
    json_data = {'id': ans.videoID,
                 'option' : ans.options,
                 'questionId' : ans.questionID}
    print(json_data)
    responses=requests.post(url="http://10.22.192.38:9090/jeecg-boot/jcedutec/courseSource/submitAnswer",headers=headers,json=json_data)
    print(responses.status_code)
    if responses.status_code == 200:
        print(responses.text)


def main():
    print("本脚本尚不完善，本脚本只可完成课程学习和课程答题，考试仍需自行手动完成。")
    print("现在需要您按以下操作帮助登录:")
    print("1.请校内同学从http://10.22.192.38:9092/登录自己的用户。"
          "###校外同学无法使用该脚本###")
    print("2.任意选择一个课程打开")
    print("3.Chrome/Edge浏览器用户请右键选择检查后，再选择网络")
    print("4.在页面左上角的过滤栏里输入updatevisits（是左上角，不是下面的过滤框）")
    print("5.刷新页面，现在你可以看到网页多了两个包")
    print("6.选择类型为xhr的包，在请求标头里复制x-access-token的数据，并粘贴在本程序中")
    token=input("请输入你的X-Access-Token：")

#获取课程信息ID，（纯手打，原网页好像用js刷新列表，不好爬取）不会JavaScript是我的败笔
    urls_1 = ["1834023741387149313","1834023916826497026","1834024290224410625","1811954032592510977","1811954369810358273","1811954561884315650","1811955013145288706","1811955307090501634","1811955432076566529","1811955598116478977","1811955769445408769","1811955963645878274" ]
    urls_2 = ["1825800731916214274","1825800968487542785","1811956223315238913","1811956976448659457","1811958145694785538","1811958275193921538","1811958440843763713","1811962125846011906","1811963385324199937","1811963788984016898","1811964969227608065","1811965137477918721","1811965287961157634","1811966900587159554","1811967126412681217","1811967455128674305","1811967653565390849","1811967826320384001","1811968026720034818","1811968411023138818"]
    urls_3 = ["1822840773138358273","1811968630964051970","1811968750166171649","1811968910526996482","1811969492239212546","1811969705469239297","1811969834079182850","1811969984654696449","1811970267044601857","1811970407922884610","1811970674085027842","1811970828338946050","1811970960912506881","1811971079925882881","1811971240819384322"]
    urls_4 = ["1823160098319699970","1812001903719178241","1812002182158049282","1812002376303992833","1812002589315915777","1812002830790385666","1812003016094736386","1812003162782130177","1812003273268486146","1812003581604356098","1812003717558525954","1812003845652570113","1812003961130147841","1812004167708008450","1812004352978804737","1812004502467993602"]
    urls_5 = ["1827980030299537410","1812004623993757697","1812004749810294786","1812005014382796802"]
    urls_lists = [urls_1, urls_2, urls_3, urls_4, urls_5]

    for a in urls_lists:
        success=0
        for i in range(len(a)):
            response=finish_class(a[i], token)
            response2=get_question(a[i],token)
            if response==200:
                success+=1
        #简单检查一下是否全部完成
        if success==len(a):
            print("\n")
            print("该章节已完成学习")
            print("\n")
        else:
            print("\n")
            print("该章节存在学习失败的章节")
            print("\n")


if __name__ == "__main__":
    main()
