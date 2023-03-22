import mysql.connector as mys
import home

host_password = home.give_password()

'''
The edit part for the user_ration_info
updating the user_ration_info based on what the person has entered'''


# these three are fine for now
def check_info_sql(admin_id='', admin_password='', ration_number='', user_password=''):
    mc = mys.connect(host="127.0.0.1", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    torf = False
    if admin_id != '':
        c.execute("Select*from admin_info")
        data = c.fetchall()
        for row in data:
            # print(row)

            if row[1] == admin_password and row[0] == admin_id:
                torf = True

    if ration_number != '':
        ration_number = int(ration_number)
        c.execute("Select*from userinfo")
        data = c.fetchall()
        for row in data:  # doesnt make sense
            if row[0] == ration_number and row[1] == user_password:
                # print('Entered if statement')
                torf = True
        # print(torf)
    mc.close()
    return torf


def in_use_sql(aadhaar_no='', ration_no=''):
    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    try:
        c.execute("Select*from userinfo")
    except:
        print('the execute line has the error')
    data = c.fetchall()
    if aadhaar_no != '':
        for row in data:
            if row[2] == aadhaar_no:
                return True
            else:
                return False
    c.execute("Select*from userinfo")
    data = c.fetchall()
    if ration_no != '':
        for row in data:
            if row[2] == int(ration_no):
                return True
            else:
                return False
    mc.close()


def delete_record_sql(ration_no):
    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    c.execute("Select*from userinfo")
    data = c.fetchall()
    for row in data:
        if row[0] == int(ration_no):
            c.execute("DELETE FROM userinfo WHERE ration_number=%s" % (ration_no,))
            c.execute("DELETE FROM user_ration_info WHERE ration_number=%s" % (ration_no,))
    mc.commit()
    mc.close()


def register_records_sql(lst):
    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    # print(lst)
    l = []
    for i in lst:
        l.extend(i)
    tup = tuple(l)
    # print(tup)

    c.execute(
        "Insert into ration1.userinfo(ration_number,passwd,name,AadharCard,totalincome,familymember,card_type) "
        "VALUES({},'{}', '{}', {}, {},'{}','{}')".format(
            tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    mc.commit()
    mc.close()


def edit_records_sql(lst):
    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()

    l = []
    for i in lst:
        l.extend(i)
    # print(l)
    c.execute("DELETE FROM userinfo WHERE ration_number=%s" % (int(l[0]),))
    c.execute(
        "Insert into ration1.userinfo(ration_number,passwd,name,AadharCard,totalincome,familymember,card_type)VALUES"
        " ({},'{}', '{}', {}, {},{},'{}')".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6]))
    mc.commit()
    mc.close()


def register_user_info(ration_no, card_type):
    # importing date class from datetime module
    from datetime import date

    # creating the date object of today's date
    # currentTimeDate = date.today()
    currentDate = date.today().strftime('%Y-%m-%d')
    cDate = currentDate
    currentDate = str(currentDate[0:7])

    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()

    # initialise the ration quantities upon registration of ration number
    # takes it from the static table and puts it into the user_ration_info table to initialise the user's ration
    if (ration_no and card_type):
        c.execute(
            "SELECT MAX((CASE WHEN a.commodity_code = 'RCE' THEN a.bpl_max_weight ELSE 0 END)) AS RCE_BPL_WEIGHT,"
            "MAX((CASE WHEN a.commodity_code = 'RCE' THEN a.apl_max_weight ELSE 0 END)) AS RCE_APL_WEIGHT,"
            "MAX((CASE WHEN a.commodity_code = 'WHT' THEN a.bpl_max_weight ELSE 0 END)) AS WHT_BPL_WEIGHT,"
            "MAX((CASE WHEN a.commodity_code = 'WHT' THEN a.apl_max_weight ELSE 0 END)) AS WHT_APL_WEIGHT,"
            "MAX((CASE WHEN a.commodity_code = 'LNT' THEN a.bpl_max_weight ELSE 0 END)) AS LNT_BPL_WEIGHT,"
            "MAX((CASE WHEN a.commodity_code = 'LNT' THEN a.apl_max_weight ELSE 0 END)) AS LNT_APL_WEIGHT "
            "FROM (SELECT commodity_code, bpl_max_weight, apl_max_weight from Stockinfo) a")
        data = c.fetchone()

        rce_bpl_weight = data[0]
        rce_apl_weight = data[1]
        wht_bpl_weight = data[2]
        wht_apl_weight = data[3]
        lnt_bpl_weight = data[4]
        lnt_apl_weight = data[5]

        s1 = "INSERT INTO user_ration_info (ration_number,card_type,wheat_bal,rice_bal,lentils_bal,trans_date) VALUES" \
             "({}, '{}', " \
             "(CASE WHEN '{}' = 'BPL' THEN {} ELSE {} END)," \
             "(CASE WHEN '{}' = 'BPL' THEN {} ELSE {} END)," \
             "(CASE WHEN '{}' = 'BPL' THEN {} ELSE {} END), " \
             "'{}'" \
             ")".format(ration_no, card_type, card_type, wht_bpl_weight, wht_apl_weight, card_type, rce_bpl_weight,
                        rce_apl_weight, card_type, lnt_bpl_weight, lnt_apl_weight, cDate)

        # print(s1)
        c.execute(s1)

    mc.commit()
    mc.close()


def edit_user_ration_sql(ration_no, card_type):
    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    c.execute("DELETE FROM user_ration_info WHERE ration_number={}".format(ration_no, ))
    mc.commit()
    mc.close()
    register_user_info(ration_no, card_type)


def get_user_records_sql(ration_no):
    l = []

    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    c.execute("Select*from user_ration_info")
    data = c.fetchall()
    c.execute("Select*from userinfo")
    data1 = c.fetchall()
    c.execute("Select*from stockinfo")
    data2 = c.fetchall()
    cost = list()
    name = card = ''
    w = r = l = 0
    ration_no = int(ration_no)

    for row in data1:
        # print(row)
        if row[0] == ration_no:
            # nonlocal name, card
            # print('\n\nEntered row in data 1\n\n')
            name = row[2]
            card = row[6]

    # print('From user_ration_info')
    for row in data:  # user_ration_info
        # print(row)
        if row[0] == ration_no and row[1] == card:
            # nonlocal w, r, l
            # print('\n\nEntered row in data\n\n')
            w = row[2]
            r = row[3]
            l = row[4]
    for row in data2:
        if card == "BPL":
            cost.append(row[2])  # order lentil rice wheat bpl cost
        else:
            cost.append(row[4])  # order lentil rice wheat apl cost

    mc.close()
    # in order(ration_number,card_type,wheat_bal,rice_bal,lentils_bal,date)
    return name, card, ['Lentils', 'Rice', 'Wheat'], [cost[0], cost[1], cost[2]], [l, r, w]


def update_user_info_date(ration_no):
    # importing date class from datetime module
    from datetime import date

    # creating the date object of today's date

    currentDate = date.today().strftime('%Y-%m-%d')
    cDate = currentDate
    currentDate = str(currentDate[0:7])

    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    ration_no = int(ration_no)
    if ration_no:
        c.execute("select CONCAT(SUBSTRING(replace(FORMAT(trans_date, 'yyyy'),',',''), 1,4), '-',"
                  " SUBSTRING(replace(FORMAT(trans_date, 'yyyy'),',',''), 5,2)) FROM user_ration_info "
                  "WHERE ration_number={}".format(ration_no))
        trans_date_str = str(c.fetchone()[0])
        trans_date_str = trans_date_str.replace(",", "")

        # print(trans_date_str)
        # print(currentDate)

        if trans_date_str != currentDate:
            c.execute("SELECT MAX((CASE WHEN a.commodity_code = 'RCE' THEN a.bpl_max_weight ELSE 0 END)) "
                      "AS RCE_BPL_WEIGHT,MAX((CASE WHEN a.commodity_code = 'RCE' THEN a.apl_max_weight ELSE 0 END)) "
                      "AS RCE_APL_WEIGHT,MAX((CASE WHEN a.commodity_code = 'WHT' THEN a.bpl_max_weight ELSE 0 END)) "
                      "AS WHT_BPL_WEIGHT,MAX((CASE WHEN a.commodity_code = 'WHT' THEN a.apl_max_weight ELSE 0 END)) "
                      "AS WHT_APL_WEIGHT,MAX((CASE WHEN a.commodity_code = 'LNT' THEN a.bpl_max_weight ELSE 0 END)) "
                      "AS LNT_BPL_WEIGHT,MAX((CASE WHEN a.commodity_code = 'LNT' THEN a.apl_max_weight ELSE 0 END)) "
                      "AS LNT_APL_WEIGHT FROM (SELECT commodity_code, bpl_max_weight, apl_max_weight from Stockinfo) a")
            data = c.fetchone()

            rce_bpl_weight = data[0]
            rce_apl_weight = data[1]
            wht_bpl_weight = data[2]
            wht_apl_weight = data[3]
            lnt_bpl_weight = data[4]
            lnt_apl_weight = data[5]

            c.execute(
                "UPDATE user_ration_info SET wheat_bal = (CASE WHEN card_Type = 'BPL' THEN {} ELSE {} END),rice_bal "
                "= (CASE WHEN card_Type = 'BPL' THEN {} ELSE {} END),lentils_bal = (CASE WHEN card_Type = 'BPL' "
                "THEN {} ELSE {} END), trans_date = '{}' WHERE ration_number = {}".format(
                    wht_bpl_weight, wht_apl_weight, rce_bpl_weight, rce_apl_weight, lnt_bpl_weight, lnt_apl_weight,
                    cDate, ration_no))
            mc.commit()
    mc.close()


def update_user_info_ration(lst, ration_no):
    from datetime import date
    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c_date = date.today().strftime('%Y-%m-%d')

    c = mc.cursor()

    s = "Update user_ration_info set wheat_bal={},rice_bal={},lentils_bal={}, trans_date='{}' where ration_number ={} " \
        .format(lst[2], lst[1], lst[0], c_date, ration_no)
    # print(s, 'update user info ration line 279 ')
    c.execute(s)
    mc.commit()
    mc.close()


'''
def fill_entry_for_edit(ration_no):
    mc = mys.connect(host="localhost", user="root", passwd=host_password, database="ration1")
    c = mc.cursor()
    c.execute("Select*from userinfo where ration_number = {}".format(ration_no))
    data = c.fetchone()
    print(data, ration_no, 'line 100 sql')
    mc.commit()
    mc.close()
    return data
'''
