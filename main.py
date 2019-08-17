#!/usr/bin/python
# -*- coding: utf-8 -*-
from traceback import print_exc
from exchange_api import juhe_exchange
from data_other import other_exchange
from data_juhe import result_to_str_juhe
from data_other import result_to_str_other
from Tkinter import *
import Tkinter as tk


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.frm_L = Frame(self)
        self.frm_R = Frame(self)

    def get_current_exchange_huhe(self):
        huilv_test = juhe_exchange()
        self.text_l.delete("1.0", "end")
        self.text_l.insert(INSERT, huilv_test)

    def get_current_exchange_other(self):
        huilv_test = other_exchange()
        self.text_l.delete("1.0", "end")
        self.text_l.insert(INSERT, huilv_test)

    def callback(self):
        asset_id = self.e.get()
        try:
            xxx = result_to_str_other(asset_id)
        except Exception:
            print print_exc()
            xxx = u'输入错误或者饰品id不存在'
            pass
        self.text_2.config(yscrollcommand=self.scroll12.set)
        self.text_2.delete("1.0", "end")
        self.text_2.insert(INSERT, xxx)

    def createWidgets(self):
        frm_R = Frame(self,)
        # Label(frm_R, text='输入要查询的钥匙id', compound= 'right',
        #       width=15, height=2).pack()

        self.text_2 = tk.Text(frm_R, width='30', height='20')
        self.text_2.pack(side=tk.BOTTOM, fill=tk.Y)
        self.scroll12 = Scrollbar(frm_R)
        self.scroll12.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll12.config(command=self.text_2)


        sv = StringVar()
        # sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
        self.e = Entry(frm_R, textvariable=sv)
        # e.bind('<Key>', self.callback(sv))
        self.e.pack({"side": "bottom"})
        self.xx = Button(frm_R,  width=20, height=20)
        self.xx["text"] = "输入要查询的钥匙id,点击",
        self.xx["command"] = self.callback
        self.xx.pack({"side": "top"})

        frm_R.pack(side=RIGHT, )


        frm_L = Frame(self,)
        self.hi_there = Button(frm_L)
        self.hi_there["text"] = "获取当前汇率(1$)",
        self.hi_there["command"] = self.get_current_exchange_other
        self.hi_there.pack({"side": "top"})

        self.text_l = tk.Text(frm_L, width='30', height='20')
        self.text_l.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll1 = Scrollbar(frm_L)
        self.scroll1.config(command=self.text_l)
        self.text_l.config(yscrollcommand=self.scroll1.set)
        self.scroll1.pack(side=tk.RIGHT, fill=tk.Y)
        frm_L.pack(side=LEFT,padx=10,fill=BOTH)
        #self.pack()



root = Tk()
root.title('steam 饰品价格监控v1.0')
root.geometry('500x300+500+200')
root.resizable(width=False, height=False)
app = Application(master=root)
app.mainloop()
root.destroy()