#update the up-pool in this file
"""
Maintenance instructions
1. dic -- add dictionary element  "pool name": order
2. getnum -- add elif..., return what I called item_num
3. uparms -- up_arm_pool only,  return fivestar_up arms
4. decoding -- similar to others
5. strdata -- add names of new items
6. add decoding function, include decoding table
7. add options in ui_mainwindow (main_ui.py)
8. add picture in res,  including new char/arms ,background 
"""

dic = {
    "常驻池":0,
    "宵宫池":1,
    "凌华池":2,
    "甘雨池":3,
    "雷神池":4,
    "心海池":5,

    "雾切池":-1
}


def judge_up(choice):
    return dic[choice]

def getnum(choice):
    '''
    返回的tuple
    (四星up数,五星up数,三星武器数,四星角色数,四星武器数,五星角色数,五星武器数)
    '''

    if dic[choice] == 0:
        return (0,0,13,20,18,5,10)
    elif dic[choice] == 1:
        return (3,1,13,13,18,5,0)
    elif dic[choice] == 2:
        return (3,1,13,12,18,5,0)
    elif dic[choice] == 3:
        return (3,1,13,10,18,5,0)
    elif dic[choice] == 4:
        return (3,1,13,14,18,5,0)
    elif dic[choice] == 5:
        return (3,1,13,14,18,5,0)

    elif dic[choice] == -1:
        return (5,2,13,15,13,0,9)
    

def up_arms(order):
    if order == -1:
        return ["雾切之回光","天空之脊"]
    else:
        print("error")


def decoding(result,pool):
    if pool == 0:
        return result
    elif pool == 1:
        return xiaogongpool(result)       #宵宫池
    elif pool == 2:
        return linghuapool(result)        #凌华池
    elif pool == 3: 
        return ganyupool(result)          #甘雨池
    elif pool == 4:
        return leishenpool(result)        #雷神池
    elif pool == 5: 
        return xinhaipool(result)         #心海池

    elif pool == -1:
        return wuqiepool(result)          #雾切池


def strdata():
    threestar_char = []
    threestar_arms = ["弹弓",'鸦羽弓','讨龙英杰谭','黑缨枪','沐浴龙血的剑','飞天御剑','冷刃','神射手之誓','翡玉法球','魔导绪论','以理服人','铁影阔剑','黎明神剑']
    fourstar_char = ['辛焱','砂糖','迪奥娜','重云','诺艾尔','班尼特','菲谢尔','凝光','行秋','北斗','香菱','安柏','雷泽','凯亚','芭芭拉','丽莎','罗莎莉亚','烟绯','早柚','九条裟罗']
    fourstar_arms = ['弓藏','祭礼弓','绝弦','西风猎弓','昭心','祭礼残章','流浪乐章','西风秘典','西风长枪','匣里灭辰','雨裁','祭礼大剑','钟剑','西风大剑','匣里龙吟','祭礼剑','笛剑','西风剑']
    fivestar_char = ['刻晴','莫娜','七七','迪卢克','琴','宵宫','神里凌华','甘雨','雷电将军','珊瑚宫心海']
    fivestar_arms = ['阿莫斯之弓','天空之翼','四风原典','天空之卷','和璞鸢','天空之脊','狼的末路','天空之傲','天空之刃','风鹰剑','雾切之回光','飞雷之弦振']
    threestar = [threestar_char,threestar_arms]
    fourstar = [fourstar_char,fourstar_arms]
    fivestar = [fivestar_char,fivestar_arms]
    anystar = [threestar,fourstar,fivestar]
    return anystar

def get_newres(result,fc,fa,fs):
    '''
    decoding
    '''
    r2 = result[2]
    if result[0] == 4:
        if result[1] == 0:
            r2= fc[result[2]]
        elif result[1] == 1:
            r2 = fa[result[2]]
    elif result[0] == 5:
        r2 = fs[result[2]]
    new_result = [result[0],result[1],r2]
    return new_result


#常驻池
def usualpool():
    orderdic_fourchar = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18,19:19,20:20
    }
    orderdic_fourarms = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18
    }
    orderdic_fivestar = {
        1:1,2:2,3:3,4:4,5:5
    }
    orderdic_fivestararms = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10
    }

#宵宫池
def xiaogongpool(result):
    '''
    decoding table
    '''
    orderdic_fourchar = {
        1:2,2:4,3:5,4:6,5:7,6:8,7:9,8:10,9:11,10:13,11:15,12:17,13:18,-1:1,-2:3,-3:19
    }
    orderdic_fourarms = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18
    }
    orderdic_fivestar = {
        1:1,2:2,3:3,4:4,5:5,-1:6
    }
    return get_newres(result,orderdic_fourchar,orderdic_fourarms,orderdic_fivestar)

#凌华池
def linghuapool(result):
    '''
    decoding table
    '''
    orderdic_fourchar = {
        1:1,2:2,3:3,4:5,5:6,6:7,7:9,8:10,9:11,10:13,11:15,12:17,-1:4,-2:8,-3:18
    }
    orderdic_fourarms = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18
    }
    orderdic_fivestar = {
        1:1,2:2,3:3,4:4,5:5,-1:7
    }
    return get_newres(result,orderdic_fourchar,orderdic_fourarms,orderdic_fivestar)

#甘雨池
def ganyupool(result):
    '''
    decoding table
    '''
    orderdic_fourchar = {
        1:1,2:2,3:3,4:4,5:6,6:7,7:8,8:10,9:13,10:15,-1:5,-2:9,-3:11
    }
    orderdic_fourarms = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18
    }
    orderdic_fivestar = {
        1:1,2:2,3:3,4:4,5:5,-1:8
    }
    return get_newres(result,orderdic_fourchar,orderdic_fourarms,orderdic_fivestar)

#雾切池
def wuqiepool(result):
    '''
    decoding table
    '''
    orderdic_fourchar = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:13,13:15,14:17,15:18
    }
    orderdic_fourarms = {
        1:1,2:2,3:4,4:5,5:6,6:7,7:10,8:11,9:13,10:14,11:15,12:16,13:17,-1:3,-2:8,-3:9,-4:12,-5:18
    }
    orderdic_fivestar = {
        1:1,2:2,3:3,4:4,5:5,6:7,7:8,8:9,9:10,-1:11,-2:6
    }
    return get_newres(result,orderdic_fourchar,orderdic_fourarms,orderdic_fivestar)

#雷神池
def leishenpool(result):
    '''
    decoing table
    '''
    orderdic_fourchar = {
        1:1,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:13,11:15,12:17,13:18,14:19,-1:2,-2:11,-3:20
    }
    orderdic_fourarms = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18
    }
    orderdic_fivestar = {
        1:1,2:2,3:3,4:4,5:5,-1:9
    }
    return get_newres(result,orderdic_fourchar,orderdic_fourarms,orderdic_fivestar)

#心海池
def xinhaipool(result):
    '''
    decoding
    '''
    orderdic_fourchar = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:11,10:13,11:15,12:18,13:19,14:20,-1:9,-2:10,-3:17
    }
    orderdic_fourarms = {
        1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18
    }
    orderdic_fivestar = {
        1:1,2:2,3:3,4:4,5:5,-1:10
    }
    return get_newres(result,orderdic_fourchar,orderdic_fourarms,orderdic_fivestar)