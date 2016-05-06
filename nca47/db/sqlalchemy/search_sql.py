get_zones_sql = "select * from dual where 1=1"
req_zones = ""


def put_sql(str_sql, lik_dic, search_dic):
    sql_ = ""
    for lik in lik_dic:
        sql_ = sql_ + " and " + lik + " like '%" + lik_dic[lik] + "%'"
    for sea in search_dic:
        sql_ = sql_ + " and " + sea + " = '" + lik_dic[lik] + "'"
    return str_sql + sql_
