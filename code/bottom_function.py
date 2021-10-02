import random
import time

random.seed = "Genshin"

#取随机数并对随机数取模
def get_rand(mod):
    rd = random.randint(0,999999)
    return rd%mod

#抽卡
def getcards(total,part,up,nums):
    if up[0]>=0:                        #根据当前卡池，选择 常驻/角色up池   或   武器up池
        return getcards_char(total,part,up,nums)     
    else:
        return getcards_arms(total,part,up,nums)


#常驻池或角色up池
def  getcards_char(total,part,up,nums):
    '''
    ifup： a tuple  (ifup, if_next_up_four, if_next_up_five)   all bool
    nums: a tuple   (fourup ,fiveup, three_arms, four_char,four_arms,five_char,five_arms)   int
    '''
    rd = get_rand(10000)
    if total<=72:         #72抽前不触发软保底
        if part<=9:        #1-9抽不触发四星保底
            if 0<=rd<60:
                return get_anystar(5,up,nums)
            elif 60<=rd<510+60:
                return get_anystar(4,up,nums)
            else:
                return get_anystar(3,up,nums)

        else:             #第10抽触发十抽保底，必出四星或以上
            if 0<=rd<60:
                return get_anystar(5,up,nums)
            else:
                return get_anystar(4,up,nums)

    elif 72<total<=89:     #72-89抽触发九十抽软保底，提升五星概率，算法为每抽递增
        mod_five = 60 + (total-72)*565
        if part<=9:
            if 0<=rd<mod_five:
                return get_anystar(5,up,nums)
            elif mod_five<rd<mod_five+510:
                return get_anystar(4,up,nums)
            else:
                return get_anystar(3,up,nums)

        else:
            if 0<=rd<mod_five:
                return get_anystar(5,up,nums)
            else:
                return get_anystar(4,up,nums)

    elif total == 90:      #第90抽触发九十抽保底，必出五星
        return get_anystar(5,up,nums)

#武器up池
def getcards_arms(total,part,ifup,nums):
    '''
    ifup： a tuple  (ifup, if_next_up_four, if_next_up_five)   all bool
    nums: a tuple   (fourup ,fiveup, three_arms, four_char,four_arms,five_char,five_arms)   int
    '''
    rd = get_rand(10000)
    if total<=63:
        if part<=9:
            if 0<=rd<70:
                return get_anystar(5,ifup,nums)
            elif 70<=rd<600+70:
                return get_anystar(4,ifup,nums)
            else:
                return get_anystar(3,ifup,nums)
        else:
            if 0<=rd<70:
                return get_anystar(5,ifup,nums)
            else:
                return get_anystar(4,ifup,nums)
    elif 63<total<=79:
        mod_five = 70 + (total-63)*620.625
        if part<=9:
            if 0<=rd<mod_five:
                return get_anystar(5,ifup,nums)
            elif mod_five<rd<=mod_five+600:
                return get_anystar(4,ifup,nums)
            else:
                return get_anystar(3,ifup,nums)
        else:
            if 0<=rd<mod_five:
                return get_anystar(5,ifup,nums)
            else:
                return get_anystar(4,ifup,nums)
    elif total == 80:
        return get_anystar(5,ifup,nums)


#给星数和是否up，返回结果
def get_anystar(star,ifup,nums):
    '''
    star: the number of stars
    ifup： a tuple  (ifup: int , if_next_up_four: bool, if_next_up_five: bool, determine_track: int, track_value: int ) 

    -> result:  tuple   (the_number_of_stars, char_or_arms, random_order)
    '''
    if ifup[0]>0:
        if star == 3:
            return get_threestar(nums)
        elif star == 4:
            return get_fourstar_upchar(ifup[1],nums)     
        elif star == 5:
            return get_fivestar_upchar(ifup[2],nums)
    elif ifup[0]==0:
        if star == 3:
            return get_threestar(nums)
        elif star == 4:
            return get_fourstar(nums)
        elif star == 5:
            return get_fivestar(nums)
    elif ifup[0]<0:
        if star == 3:
            return get_threestar(nums)
        elif star == 4:
            return get_fourstar_uparms(ifup[1],nums)
        elif star == 5:
            return get_fivestar_uparms(ifup,nums)
    


#随机给出一个五星角色或武器，武器与角色概率为55开，
#返回一个tuple，tuple[0]表示星数,tuple[1]表示角色还是武器,tuple[2]表示对应的index
def get_fivestar(nums):
    rd = get_rand(2)
    if rd == 0:
        rd2 = get_rand(nums[5])
        return (5,0,rd2+1)             
    elif rd == 1:
        rd2 = get_rand(nums[6])
        return (5,1,rd2+1)
    else:
        print("Something error in get_fivestar.")


#随机给出一个四星角色或武器，武器与角色概率为55开
def get_fourstar(nums):
    rd = get_rand(2)
    if rd == 0:
        rd2 = get_rand(nums[3])   
        return (4,0,rd2+1)   #角色
    else:
        rd2 = get_rand(nums[4])
        return (4,1,rd2+1)   #武器

#随机给出一个三星武器
def get_threestar(nums):
    rd = get_rand(nums[2])
    return (3,1,rd+1)

#给一个五星角色(角色up池)
def get_fivestar_upchar(nextup_five,nums):
    '''
    nextup_five: bool
    '''
    if nextup_five:
        return (5,0,-1)
    else:
        rd = get_rand(2)
        if rd == 0:
            rd2 = get_rand(nums[5])
            return (5,0,rd2+1)
        elif rd == 1:
            return (5,0,-1)

#给一个四星物品(角色up池)
def get_fourstar_upchar(nextup_four,nums):
    '''
    nextup_four : bool
    '''
    if nextup_four:
        rd2 = get_rand(nums[0])                #获得四星保底
        return (4,0,-(rd2+1))
    else:
        rd = get_rand(2)
        if rd == 0:                     #获得up四星
            rd2 = get_rand(nums[0])
            return (4,0,-(rd2+1))

        else:                           #获得非up四星角色/武器
            rd2 = get_rand(2)
            if rd2 == 0:
                rd2 = get_rand(nums[3])      #这里的数量会变化
                return (4,0,rd2+1)
            else:
                rd2 = get_rand(nums[4])
                return (4,1,rd2+1)

#给一个五星武器(武器up池)
def get_fivestar_uparms(ifup,nums):
    if ifup[4] >= 2 and ifup[3] <0 :
        return (5,1,ifup[3])                #获得定轨武器
    else:
        if ifup[2]:
            rd = get_rand(2)                #大保底，获得up武器之一
            return (5,1,-(rd+1))            
        else:
            rd = get_rand(4)                #获得up五星概率为75%
            if rd == 3:                      
                rd2 = get_rand(nums[6])       #获得非up五星
                return (5,1,rd2+1)     
            else:
                rd2 = get_rand(2)            #获得up五星
                return (5,1,-(rd2+1))


def get_fourstar_uparms(nextup_four,nums):
    '''
    nextup_four : bool
    '''
    if nextup_four:
        rd2 = get_rand(nums[0])                #获得四星保底
        return (4,1,-(rd2+1))
    else:
        rd = get_rand(4)                #获得up四星概率为75%
        if rd == 3:                     #获得up四星
            rd2 = get_rand(nums[0])
            return (4,1,-(rd2+1))

        else:                           #获得非up四星角色/武器
            rd2 = get_rand(2)
            if rd2 == 0:
                rd2 = get_rand(nums[3])      #这里的数量会变化
                return (4,0,rd2+1)
            else:
                rd2 = get_rand(nums[4])
                return (4,1,rd2+1)

        
        



            