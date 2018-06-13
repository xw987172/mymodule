import sys
from func.mymath import mymathclass
from func.myhive import myhiveclass,config
from eprogress import LineProgress
import xlwt
class ab:

    def ac(self):

        # 由2组字典组成
        # #南宁、长沙的所有门店的日商向量数据
        dict1 = {
            '长沙1':[1,2,3,4,5,6,7],
            '长沙2':[7,6,4,5,3,2,1],
            '南宁1':[2,3,5,1,3,5,2],
        }
        # 武汉的所有门店的
        dict2 = {
            '武汉1':[4,5,6,7,8,9,10],
            '武汉2':[2,1,2,4,5,8,10],
        }
        result = [key+"-"+key2+":"+str(mymathclass.cosLike(val,val2)) for key,val in dict1.items() for key2,val2 in dict2.items()]
        return result

    @staticmethod
    def _getData(store_code,whstore_code):
        '''
        得到南宁和长沙的店铺与武汉的店铺的日商的余弦值
        :param store_code: 
        :param whstore_code: 
        :return: (store_code, whstore_code, 余弦值,)
        '''
        sql = "select concat_ws(',',substring(a.sale_date,1,10)) from bic_stores a inner join bic_stores b on a.sale_date=b.sale_date where a.store_code =%s and b.store_code=%s" %(whstore_code,store_code)

        with myhiveclass(config) as myhive:
            result = myhive.select(sql)
            result = ["\""+str(x[0])+"\"" for x in result]
            common_day = ",".join(result)

            vals1 = myhive.select("select concat_ws(',',cast(sales_amt as string)) from bic_stores where store_code =%s and sale_date in (%s)" %(whstore_code,common_day))
            vals1 = [x[0] for x in vals1]
            vals2 = myhive.select(
                "select concat_ws(',',cast(sales_amt as string)) from bic_stores where store_code =%s and sale_date in (%s)" % (
                store_code, common_day))
            vals2 = [x[0] for x in vals2]
            return (store_code,whstore_code,mymathclass.cosLike(vals1,vals2),)

    def work(self):
        '''
        执行函数
        :return: 
        '''
        dict11,dict12 = [self.getdata1(city) for city in ['"武汉"',("南宁","长沙")]]
        result = [self._getData(store_code,whstore_code) for store_code in dict11 for whstore_code in dict12]
        # result =list()
        # progress = LineProgress(title="line progress")
        # for i,store_code in enumerate(dict11):
        #     for whstore_code in dict12:
        #         result.append(self._getData(store_code,whstore_code))
        #     progress.update(i)
        wb = xlwt.Workbook()
        st = wb.add_sheet("sheet")
        for i,s in enumerate(result):
            st.write(i,0,str(s[0]))
            st.write(i,1,str(s[1]))
            st.write(i,2,str(s[2]))
        wb.save("coslike.xls")

    @staticmethod
    def getdata1(city):
        '''
        获取不同城市下的所有店铺
        :param city: 
        :return: 
        '''
        sql = "select store_code from dw.bic_stores where city in (%s)" %(str(city)) if isinstance(city,str) else "select store_code from dw.bic_stores where city in %s" %(str(city))
        with myhiveclass(config) as myhive:
            result = myhive.select(sql)
        return [store_code[0] for store_code in result]



if __name__ == "__main__":
    print(ab().work())