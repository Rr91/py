# SecurityBaseOperator v.0.3.1
import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import sleep as wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests

def main():
    codes_list = []

    def clear_tab1():
        fam_ent.delete(0,END)
        nam_ent.delete(0,END)
        otch_ent.delete(0,END)
        dbirth_ent.delete(0,END)
        mbirth_ent.delete(0,END)
        ybirth_ent.delete(0,END)
        spas_ent.delete(0,END)
        npas_ent.delete(0,END)
        dcode_ent.delete(0,END)
        pcode_ent.delete(0,END)

    def update_tab2():
        dcode  = dcode_ent.get()
        pcode  = pcode_ent.get()

        with open('Data\codes.csv', 'r', encoding = "utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file,)

            for line in csv_reader:
                if dcode+'-'+pcode in line['code']:
                    codes_list.append(line['place'])

        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='Список подразделений по коду '+dcode+'-'+pcode+':')
        Label(tab2, text = "").grid(column=0,row=0,columnspan=2)
        if codes_list == []:
            Label(tab2, text = 'Место выдачи паспорта не найдено').grid(column=0, row=0,columnspan=2,padx = 5)
        else:
            for code in range(len(codes_list)):
                Label(tab2, text = codes_list[code]).grid(column=0,row=1+code,columnspan=2,padx = 5)
        def clear_tab2():
            tab2.destroy()
            autoclicker_start()
        Label(tab2, text = "").grid(column=0,row=len(codes_list)+2,columnspan=2)
        Button(tab2, text = "Закрыть окно", bg = "#cf9999", command = tab2.destroy).grid(column=0,row=len(codes_list)+3)
        Button(tab2, text = "Запустить проверку", command = clear_tab2).grid(column=1,row=len(codes_list)+3)
        codes_list.clear()
        tab_control.select(tab2)


    def update_tab3():
        global email
        email = email_ent.get()
        messagebox.showinfo('SBOv.0.3 - E-mail Указан', 'Письма будут отправлены на '+email)
        tab3.destroy()

    def update_tab5():

        fam_ent.delete(0, END)
        nam_ent.delete(0, END)
        otch_ent.delete(0, END)
        dbirth_ent.delete(0, END)
        mbirth_ent.delete(0, END)
        ybirth_ent.delete(0, END)
        spas_ent.delete(0, END)
        npas_ent.delete(0, END)
        dcode_ent.delete(0, END)
        pcode_ent.delete(0, END)

        order_id = order_ent.get()
        rdata = get_input_data(order_id)
        print(rdata)
        if not rdata :
            print('error on server data')
        else:
            if 'fam' in rdata and rdata['fam']:
                fam_ent.insert(0, rdata['fam'])
            if 'nam' in rdata and rdata['nam']:
                nam_ent.insert(0, rdata['nam'])
            if 'otch' in rdata and rdata['otch']:
                otch_ent.insert(0, rdata['otch'])
            if 'dbirth' in rdata and rdata['dbirth']:
                dbirth_ent.insert(0, rdata['dbirth'])
            if 'mbirth' in rdata and rdata['mbirth']:
                mbirth_ent.insert(0, rdata['mbirth'])
            if 'ybirth' in rdata and rdata['ybirth']:
                ybirth_ent.insert(0, rdata['ybirth'])
            if 'spas' in rdata and rdata['spas']:
                spas_ent.insert(0, rdata['spas'])
            if 'npas' in rdata and rdata['npas']:
                npas_ent.insert(0, rdata['npas'])
            if 'dcode' in rdata and rdata['dcode']:
                dcode_ent.insert(0, rdata['dcode'])
            if 'pcode' in rdata and rdata['pcode']:
                pcode_ent.insert(0, rdata['pcode'])
        tab_control.select(tab1);


    def autoclicker_start():
        fam    = fam_ent.get()
        nam    = nam_ent.get()
        otch   = otch_ent.get()
        dbirth = dbirth_ent.get()
        mbirth = mbirth_ent.get()
        ybirth = ybirth_ent.get()
        spas   = spas_ent.get()
        npas   = npas_ent.get()
        birth = dbirth+'.'+mbirth+'.'+ybirth
        links = ['https://gosnalogi.ru/',
                 'https://peney.net/',
                 'https://service.nalog.ru/static/personal-data.html?svc=inn&from=%2Finn.html',
                 'https://fssprus.ru/iss/ip/',
                 'https://fssprus.ru/iss/suspect_info/',
                 'https://xn--b1aew.xn--p1ai/wanted',
                 'http://xn--b1afk4ade4e.xn--b1ab2a0a.xn--b1aew.xn--p1ai/info-service.htm?sid=2000']
        error_list = []

        driver_path = 'Driver\chromedriver.exe'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome((ChromeDriverManager().install()), options=chrome_options)

        for link in links:
            control_string = "window.open('{0}')".format(link)
            driver.execute_script(control_string)
        driver_is_loaded = True

        if driver_is_loaded == True:
            try:
                driver.switch_to.window(driver.window_handles[1])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "form_DOC_SERIE")))
                driver.find_element_by_id("form_DOC_SERIE").send_keys(spas)
                driver.find_element_by_id("form_DOC_NUMBER").send_keys(npas)
            except:
                pass

            try:
                driver.switch_to.window(driver.window_handles[2])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "s_family")))
                driver.find_element_by_name("s_family").send_keys(fam)
                driver.find_element_by_name("fio").send_keys(nam)
                driver.find_element_by_name("s_patr").send_keys(otch)
                driver.find_element_by_name("email").send_keys(email)
                driver.find_element_by_class_name("select2").click()
                driver.find_element_by_class_name("select2-search__field").send_keys(ybirth+Keys.ENTER)
            except:
                pass

            try:
                driver.switch_to.window(driver.window_handles[3])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input01")))
                driver.find_element_by_id("input01").send_keys(fam+' '+nam+' '+otch)
            except:
                pass

            try:
                driver.switch_to.window(driver.window_handles[4])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input01")))
                driver.find_element_by_id("input01").send_keys(fam)
                driver.find_element_by_id("input02").send_keys(nam)
                driver.find_element_by_id("input05").send_keys(otch)
                vfssp_birth = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input06")))
                driver.execute_script("document.getElementById('input06').click()")
                driver.execute_script("arguments[0].setAttribute('value', '" + birth +"')", vfssp_birth);
            except:
                pass

            try:
                driver.switch_to.window(driver.window_handles[5])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "unichk_0")))
                inn_check   = driver.find_element_by_id("unichk_0")
                driver.execute_script("arguments[0].click();", inn_check)
                inn_cntbtn  = driver.find_element_by_id("btnContinue")
                driver.execute_script("arguments[0].click();", inn_cntbtn)

                def innprint(where,letters):
                    for letter in range(len(letters)):
                        where.send_keys(letters[letter])
                inn_loaded2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fam")))
                inn_fam     = driver.find_element_by_name("fam")
                innprint(inn_fam,fam)
                inn_nam     = driver.find_element_by_name("nam")
                innprint(inn_nam,nam)
                inn_otch    = driver.find_element_by_name("otch")
                innprint(inn_otch,otch)
                driver.find_element_by_name("bdate").send_keys(birth)
                inn_docno = driver.find_element_by_name("docno")
                innprint(inn_docno,spas+npas)
                inn_send    = driver.find_element_by_id("btn_send")
                driver.execute_script("arguments[0].click();", inn_send)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "resultInn")))
                inn = driver.find_element_by_id("resultInn").text
            except:
                pass

            try:
                driver.switch_to.window(driver.window_handles[6])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inn")))
                driver.find_element_by_name("inn").send_keys(inn)
                driver.find_element_by_name("email").send_keys(email)
                driver.find_element_by_id("searchnalogsubmit").click()
            except:
                pass

            try:
                driver.switch_to.window(driver.window_handles[7])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "paramNumber")))
                driver.find_element_by_name("paramNumber").send_keys(inn)
                driver.find_element_by_class_name("btn.btn-success.btn-lg").click()
            except:
                pass

            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    
    def get_input_data(order_id):
        res = requests.get('https://pauri.ru/pythonpasspost/', params={'oid': order_id})
        return res.json()


    window = Tk()
    window.title("SecurityBaseOperator v.0.3")
    # window.wm_iconbitmap('Data\sboicon.ico')
    tab_control = ttk.Notebook(window)

   

    tab1 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab5 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='Паспорт')
    tab_control.add(tab3, text='Почта')
    tab_control.add(tab5, text='Заказ')

    ## tab1

    Label(tab1, text = "Фамилия").grid(column=0, row=0, padx = 5)
    fam_ent = Entry(tab1, width = 20)
    fam_ent.grid(column=1, row=0, padx = 5)

    Label(tab1, text = "Имя").grid(column=0, row=1, padx = 5)
    nam_ent = Entry(tab1, width = 20)
    nam_ent.grid(column=1, row=1, padx = 5)
    
    Label(tab1, text = "Отчество").grid(column=0, row=2, padx = 5)
    otch_ent = Entry(tab1, width = 20)
    otch_ent.grid(column=1, row=2, padx = 5)
    
    Label(tab1, text = "Дата рождения (дд)").grid(column=0, row=3, padx = 5)
    dbirth_ent = Entry(tab1, width = 20)
    dbirth_ent.grid(column=1, row=3, padx = 5)
    
    Label(tab1, text = "Дата рождения (мм)").grid(column=0, row=4, padx = 5)
    mbirth_ent = Entry(tab1, width = 20)
    mbirth_ent.grid(column=1, row=4, padx = 5)
    
    Label(tab1, text = "Дата рождения (гггг)").grid(column=0, row=5, padx = 5)
    ybirth_ent = Entry(tab1, width = 20)
    ybirth_ent.grid(column=1, row=5, padx = 5)
    
    Label(tab1, text = "Паспорт (серия)").grid(column=0, row=6, padx = 5)
    spas_ent = Entry(tab1, width = 20)
    spas_ent.grid(column=1, row=6, padx = 5)
    
    Label(tab1, text = "Паспорт (номер)").grid(column=0, row=7, padx = 5)
    npas_ent = Entry(tab1, width = 20)
    npas_ent.grid(column=1, row=7, padx = 5)
    
    Label(tab1, text = "Код подразделения (до черты)").grid(column=0, row=8, padx = 5)
    dcode_ent = Entry(tab1, width = 20)
    dcode_ent.grid(column=1, row=8, padx = 5)
    
    Label(tab1, text = "Код подразделения (после черты)").grid(column=0, row=9, padx = 5)
    pcode_ent = Entry(tab1, width = 20)
    pcode_ent.grid(column=1, row=9, padx = 5)
    
    Button(tab1, text = "Отчистить данные", bg = "#cf9999", command = clear_tab1).grid(column=0, row=10, padx = 5, pady = 5)
    Button(tab1, text = "Загрузить данные", command = update_tab2).grid(column=1, row=10, padx = 5, pady = 5)


    ## tab3
    Label(tab3, text='').grid(column = 0, row = 0)
    Label(tab3, text='Укажите E-mail, куда должны приходить письма от "Розыск"').grid(column = 0, row = 1, padx = 5, pady = 5)
    email_ent = Entry(tab3, width = 30)
    email_ent.grid(column=0, row=2, padx = 5, pady = 5)
    Button(tab3, text='Указать', command=update_tab3).grid(column=0, row=3, padx = 5, pady = 5)
    tab_control.pack(expand=1, fill='both')
    tab_control.select(tab3)

    ## tab5
    Label(tab5, text='').grid(column = 0, row = 0)
    Label(tab5, text='Укажите Номер заказа, для получения данных клиента').grid(column = 0, row = 1, padx = 5, pady = 5)
    order_ent = Entry(tab5, width = 30)
    order_ent.grid(column=0, row=2, padx = 5, pady = 5)
    Button(tab5, text='Указать', command=update_tab5).grid(column=0, row=3, padx = 5, pady = 5)
    

    window.mainloop()

if __name__ == '__main__':
        main()
