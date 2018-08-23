# coding:utf8
from urllib import parse as up
import requests
from func.mymysql import mymysqlclass,myconfig

class GaoDeClass(object):

    url = "https://www.amap.com/service/poiTipslite?&city={0}&geoobj=114.201412%7C30.516057%7C114.505596%7C30.658512&words={1}"

    def __init__(self):
        pass

    @classmethod
    def GetLocationByName(cls,city,word):
        '''
        高德拾取坐标系统，根据输入的地址关键字获取经纬度信息等。。。
        :param city:
        :param word:
        :return:
        '''
        url = cls.url.format(city, up.quote(word))
        resp = requests.get(url).json()
        result = dict()
        result["name"] = resp.get("data").get("tip_list")[0].get("tip").get("name")
        result["district"] = resp.get("data").get("tip_list")[0].get("tip").get("district")
        result["category"] = resp.get("data").get("tip_list")[0].get("tip").get("category")
        result["address"] = resp.get("data").get("tip_list")[0].get("tip").get("address")
        result["pointX"] = resp.get("data").get("tip_list")[0].get("tip").get("x")
        result["pointY"] = resp.get("data").get("tip_list")[0].get("tip").get("y")
        return result


if __name__== "__main__":
    columns = [
        "poi名称（必填）",
        "poi详细地址（必填，推荐为高德地图对应的地址）",
        "poi类型（如为自定义信息类型可由客户自己定义且必填；如为我的店铺中的信息类型可不填）",
        "poi一级类目（非必填，名称由客户定义）",
        "poi二级类目（非必填，名称由客户定义）",
        "社区类型",
        "店铺类型",
        "店龄"]
    import xlwt
    wb = xlwt.Workbook()
    st = wb.add_sheet("sheet1")
    line = 0
    for i,val in enumerate(columns):
        st.write(line,i,val)
    line+=1
    with mymysqlclass(myconfig) as my:
        shops = my.select("select store_code,store_name,store_address,business_district_level1_name,store_type,store_age from dw.dim_stores_info where left(store_code,3)=117")
    for code,name,address,communate,type,age in shops:
        try:
            result = GaoDeClass().GetLocationByName(420100, "Today今天24小时便利店({0})".format(name))
        except Exception as err:
            print(name,err)
        else:
            try:
                address =result.get("district") + result.get("address")
            except:
                print(name)
                address = None
        if bool(address)==False:
            continue
        st.write(line,0,name)
        st.write(line,1,address)
        st.write(line,5,communate)
        st.write(line,6,type)
        st.write(line,7,age)
        line+=1
        # with mymysqlclass(myconfig) as my:
        #     my.dochange(sql)
    wb.save(r"C:\Users\xwtoday\Desktop\ReactDjango\t1.xls")